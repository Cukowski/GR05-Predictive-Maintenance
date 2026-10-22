"""Build Task 3 Markdown/HTML from the executed notebook's exported evidence.

Run from any directory: python scripts/build_task3_report.py
No HDF5 access or network access is needed for this presentation step.
"""
from pathlib import Path
import csv
import html
import json

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / 'reports/results'
summary_path = RESULTS / 'task3_summary.json'
if not summary_path.exists():
    raise SystemExit('Run notebooks/01-data-understanding.ipynb from top to bottom first.')
s = json.loads(summary_path.read_text())

def read_csv(name):
    with (RESULTS / name).open(newline='') as stream:
        return list(csv.DictReader(stream))

def number(value):
    return f'{int(float(value)):,}'

def md_table(headers, rows):
    return '\n'.join(['| ' + ' | '.join(headers) + ' |',
                      '| ' + ' | '.join(['---'] * len(headers)) + ' |',
                      *['| ' + ' | '.join(str(v).replace('|','/') for v in row) + ' |' for row in rows]])

def h(value):
    return html.escape(str(value))

def h_table(headers, rows):
    return '<div class="table-scroll"><table><thead><tr>' + ''.join(f'<th scope="col">{h(c)}</th>' for c in headers) + '</tr></thead><tbody>' + ''.join('<tr>' + ''.join(f'<td>{h(v)}</td>' for v in row) + '</tr>' for row in rows) + '</tbody></table></div>'

engines = read_csv('engines.csv')
stats = read_csv('statistics.csv')
dictionary = read_csv('feature_dictionary.csv')
outliers = read_csv('outlier_screen.csv')
checks = s['checks']
ov = s['overview']
t = s['totals']
summary_headers = ['Subset','Partition','Readings','Engines','Flights','Lifetime range (cycles)']
summary_rows = [[r['dataset'],r['partition'],number(r['readings']),r['engines'],r['flights'],f"{r['min_lifetime']}–{r['max_lifetime']}"] for r in ov]
engine_headers=['Subset','Split','Unit','Flight class','Readings','Flights','RUL range']
engine_rows=[[r['dataset'],r['partition'],r['unit'],int(float(r['flight_class'])),number(r['readings']),r['cycles'],f"{int(float(r['rul_min']))}–{int(float(r['rul_max']))}"] for r in engines]
feature_headers=['Block','Variable','Storage','Meaning','Unit','Attribute type','Variation','Scale','Operators','Role']
feature_rows=[[r[k] for k in ['group','feature','dtype','description','unit','attribute_type','variability','scale','operators','role']] for r in dictionary]
quality_headers=['Dimension','Coverage','Observed result','Limit']
quality_rows=[[r[k] for k in ['dimension','scope','finding','limitation']] for r in s['quality']]
manifest_rows=[[r['file'],number(r['bytes']),r['sha256']] for r in s['files']]
selected_stats=[r for r in stats if r['partition']=='dev' and r['feature'] in ['alt','Mach','TRA','T2','T48','Nc','Wf','RUL']]
stat_rows=[[r['dataset'],r['feature'],*[f"{float(r[c]):.3f}" for c in ['minimum','mean','std','maximum']]] for r in selected_stats]
outlier_top=sorted(outliers,key=lambda r:float(r['flagged_pct']),reverse=True)[:8]

report=f'''# Task 3 — Data Understanding Report

**GR05 · Industrial Analytics · WS 2026/27**<br>
**Team:** Selçuk Ata Aksoy and Denzel Gregory Pragassa<br>
**Analysis date:** {s['analysis_date']}<br>
**Status:** Executed descriptive analysis; team interpretation/review pending. No predictive model trained.

## 1. Purpose and course alignment

We need to explain the dataset before preparing features or training models. The supplied task sheet `tasks/IBS6 Industrial Analytics Project Tasks V3.0.pdf`, p. 1, requests dataset structure/features, types/distributions, missing values/anomalies, and an Exploratory Analysis Notebook with a feature description table, visualizations, summary statistics, and a data quality report. Its internal heading says V12.0; this report cites the supplied filename and 22 October 2026 date rather than assuming those version labels agree.

This work is CRISP-DM data understanding. It answers what the data contains and what limitations matter for later RUL regression. The lecturer's verbal emphasis was understanding the data; model training and extensive cleaning are intentionally deferred.

| Required element | Evidence |
|---|---|
| Structure and features | Notebook sections 2–3; `inventory.csv`; `feature_dictionary.csv` |
| Data types and distributions | Full-array statistics; operating/sensor distribution figures |
| Missing values and anomalies | Full numeric scan; sample IQR screen; six-dimension quality table |
| Exploratory notebook | [Executed guided notebook](../notebooks/01-data-understanding.ipynb) |
| Visualizations and interpretation | Seven exported figures; notebook explanations and discussion below |
| Summary statistics and quality report | Sections 5–6 below; machine-readable evidence in `reports/results/` |

## 2. Sources and provenance

The two actual local HDF5 files are `N-CMAPSS_DS01-005.h5` and `N-CMAPSS_DS02-006.h5`, supplied under `data/raw/` after a Kaggle download. Exact file identity:

{md_table(['File','Bytes','Local SHA-256'],manifest_rows)}

Combined size is {sum(r['bytes'] for r in s['files']) / 1024**3:.3f} GiB. Checksums identify local bytes; no upstream checksum comparison or Kaggle version/license verification has been completed.

The two accompanying files under `data/` are source references, not additional measurement datasets:

- `Run_to_Failure_Simulation_Under_Real_Flight_Conditions_Dataset.pdf`: seven-page preprint, 20 April 2020, focused on the DS02 nine-unit scenario. Tables 1–4 describe physical variables; pp. 3–5 discuss trajectories, flight classes, and a 1 Hz sampling rate for that scenario.
- `N-CMAPSS_Example_data_loading_and_exploration.ipynb`: example credited to Manuel Arias. Used to understand loading and metadata; its full-array concatenation pattern was replaced by read-only chunks. Its long-flight class prose contains a typo; we follow its class table and actual codes.

These are distinct from the 2021 journal article for the wider N-CMAPSS collection ([Arias Chao et al., Data 6(1), 5](https://doi.org/10.3390/data6010005)). The local older paper omits `P2` from its measured-sensor table and lists some virtual variables absent from these files. Our inventory follows actual HDF5 metadata; the `P2` interpretation/unit remains flagged for source confirmation.

## 3. Observational structure and population

{md_table(summary_headers,summary_rows)}

Together the files contain **{t['readings']:,} readings**, **{t['flights']:,} engine-flight pairs**, and **{t['engines']} dataset-scoped engine histories**. This does not establish 19 independent physical engines across subsets. Some IDs and lifetimes recur; cross-subset independence/identity is unresolved. Analyse splits within a subset and retain dataset identity.

One row is an aligned operating/sensor reading. Many readings belong to the same flight. A flight is identified by dataset + unit + cycle. A reading can be located by dataset + partition + row index; there is no explicit timestamp. There are six aligned numeric blocks, totalling **47 stored fields**: W (4), X_s (14), X_v (14), T (10), Y (1), A (4). W + X_s give **18 candidate physical predictors** for the first baseline; the other 29 fields have different roles.

The provided development/test engine IDs are disjoint within both files. DS01 uses development units 1–6 and test units 7–10. DS02 uses development units 2, 5, 10, 16, 18, 20 and test units 11, 14, 15. These are complete labelled run-to-failure histories in the local files, not the truncated test sequences one might expect from the original C-MAPSS benchmark.

{md_table(engine_headers,engine_rows)}

![Observed engine lifetimes](../reports/figures/engine_lifetimes.svg)

## 4. Feature descriptions, scales, and physical meaning

LPC/HPC mean low/high-pressure compressor; HPT/LPT mean low/high-pressure turbine. Rankine (°R) is an absolute temperature scale, psia is absolute pressure, and rpm is revolutions/minute. The lecturer's *Dataset Scales* PPTX, slides 3–4, guides the table below: nominal labels allow equality; ordinal categories add ordering; interval variables support meaningful differences; ratio variables have meaningful zero points. Discrete/continuous variation is recorded separately from measurement scale. RUL is a discrete ratio count; Rankine temperature is continuous ratio. Altitude has a reference datum and is treated as interval; cycle is an interval index, while an aggregated flight count is ratio. The classifications for throttle control position and simulator modifiers are explicit working interpretations; P2 and stall-margin zero conventions remain unconfirmed.

The supplied *Task 3 - Describe Data - Feature Description Table - Data Types.ipynb* guides our pandas inspection and `feature_description_table.csv` (188 file/partition/feature rows). It includes storage dtype, full non-null counts/ranges, sampled uniqueness, scale, valid operators, null flags, and notes. Domain-specific overrides replace generic guesses based on numeric dtype or high uniqueness; a mostly unique sensor value is not an ID. Notebook copies demonstrate int64 IDs/counts and ordered/unordered categorical types without modifying raw files.

Float64 storage does not make engine IDs continuous measurements. Flight class is ordinal (1 short, 2 medium, 3 long); health state is a categorical retrospective label. Both are metadata, not first-baseline predictors.

{md_table(feature_headers,feature_rows)}

`X_v` virtual channels and `T` health modifiers expose simulator information that may not be available in practice. Use them only for explanation unless availability is justified. The simulator's “measured sensors” are simulated responses, not observed real-world engine failures.

## 5. Descriptive findings and interpretation

### 5.1 RUL labels are a retrospective countdown

Every engine-flight checked satisfies **RUL = final observed cycle − current cycle**, constant inside each flight, ending at zero. The scan found {t['cycle_logic_flags']} combined flags across within-flight label consistency, countdown logic, cycle continuity, health-state direction, and mixed class/health checks. DS01 lifetimes range from 75 to 100 cycles; DS02 from 59 to 89. These label trajectories explain the target; they are not a model result. The final cycle uses future information and must never be used as a predictor.

![Development RUL labels](../reports/figures/rul_trajectories.svg)

### 5.2 Flight operating conditions affect sensor readings

A flight contains varying altitude, Mach, throttle, and inlet temperature. Sensor changes can reflect mission phase and engine condition together. The single-flight figure uses the first DS01 development flight and an ordered reading index. The paper's 1 Hz statement does not supply missing timestamps or prove gap-free time sampling in our copies.

![One complete flight](../reports/figures/single_flight.svg)

### 5.3 Operating-regime coverage differs across splits

**All six DS02 development engines are flight class 3; test also contains class 1 (unit 14) and class 2 (unit 15).** DS01 has all three classes in both splits. This is structural evidence of a generalization challenge, not evidence of model failure. Longer flights yield more readings, so raw-row averages weight them more heavily. Report per-engine results later instead of relying only on a row-weighted score. Test structure/labels were inspected in this EDA; document that exposure and do not adaptively tune to the test data.

![Sampled operating distributions](../reports/figures/operating_distributions.svg)

### 5.4 Full-data statistics, sampled distributions

The following statistics cover complete **development** arrays. Min/max, mean and sample standard deviation are full-scan results, not sample estimates. The full 188-row statistics export includes all 47 fields in all four file partitions.

{md_table(['Subset','Variable','Minimum','Mean','Std','Maximum'],stat_rows)}

![Sampled sensor distributions](../reports/figures/sensor_distributions.svg)

Cycle means average all readings from a given flight. Sensor trend plots standardize these means within each complete development engine for visual comparison only. That transformation uses future history and is not suitable unchanged as a deployable preprocessing step. Whole-flight averages mix operating regimes and do not isolate causal wear.

![Exploratory cycle sensor trends](../reports/figures/sensor_cycle_trends.svg)

The Pearson heatmap covers 18 candidate predictors plus RUL on the DS01 development sample. Operating regimes, engine differences, and temporal dependence can create correlations; neither predictive performance nor causality follows from them. No independent-observation significance tests are claimed.

![Sampled correlations](../reports/figures/development_correlation.svg)

## 6. Data quality — lecturer's six dimensions

{md_table(quality_headers,quality_rows)}

The complete scan covers **{t['numeric_cells']:,} numeric cells**. No NaN or infinite values were detected. No invalid auxiliary codes/indices or within-unit backward cycle transitions were found. These results do not establish physical accuracy, absence of sentinel values, or absence of missing time intervals.

Exact duplicate checks cover all **adjacent full records** and the deterministic sample of 12,000 rows per partition (48,000 rows in total). Both found zero duplicates. All possible non-adjacent pairs in 14 million readings were not exhaustively compared. Repeated engine/cycle/label values are expected; automatically deduplicating on those fields would destroy valid within-flight trajectories.

The IQR screen uses development-only samples, independently within each subset. Its most flagged dataset-variable pairs are:

{md_table(['Subset','Variable','Sample rows','Flagged','Flagged %'], [[r['dataset'],r['feature'],r['sample_rows'],r['flagged'],f"{float(r['flagged_pct']):.2f}"] for r in outlier_top])}

IQR flags are candidates for investigation, not confirmed errors. Mixed operating regimes can create long tails. No raw values were removed, imputed, clipped, resampled, or normalized for training in Task 3.

## 7. Feasible next decisions

1. Begin preparation with DS01 and candidate W + X_s variables; keep DS02 as a later robustness case. This is a proposed scope, pending team agreement.
2. Consider end-of-flight predictions with current-flight features; define the prediction point before aggregation and modeling.
3. Keep unit-grouped development validation and preserve provided test engines. Fit preprocessing on training engines only; document this notebook's test exposure.
4. Exclude RUL, final engine lifetime, future cycles, health state, and hidden simulator quantities from baseline predictors. IDs are grouping keys, not numeric predictors.
5. Confirm upstream file/version and redistribution terms, and resolve P2's source definition/unit. Investigate possible shared engine histories before combining subsets.
6. Only after preparation, establish a simple baseline and measure MAE/RMSE in flight cycles, including per-engine errors and optimistic RUL overestimation.

No trained-model performance, economic savings, real-engine failure validation, or aviation suitability is claimed.

## 8. Reproduce and explain

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m jupyterlab
# Run notebooks/01-data-understanding.ipynb top to bottom.
python scripts/build_task3_report.py
```

The notebook discovers the repository from its working directory, validates expected file paths, uses {s['configuration']['chunk_rows']:,}-row chunks, and exports CSV/JSON evidence and seven SVG figures. Distribution/IQR/duplicate samples are deterministic evenly spaced row indices, {s['configuration']['sample_rows_per_partition']:,} per partition. They are not random population samples. Raw HDF5 arrays remain local and ignored by Git.

Environment used: {', '.join(f'{k} {v}' for k,v in s['environment'].items())}. Complete installed dependency versions are recorded in `requirements-lock.txt`; primary packages are pinned in `requirements.txt`.

Use the notebook's presentation questions to practise explaining rows vs flights vs engines, label construction, storage vs scale, outliers vs errors, split shift, and leakage. Both team members should review the report and be able to reproduce its explanations.

## 9. References and disclosure

- Supplied project task sheet, p. 1: `IBS6 Industrial Analytics Project Tasks V3.0.pdf`, dated 22 October 2026; internal heading V12.0.
- Supplied *Industrial Analytics — Introduction V2.0*, pp. 10–11: descriptive, diagnostic, predictive, prescriptive categories.
- Supplied *Data Science — Introduction V1.0*, pp. 9–12: systematic process, context, overfitting.
- Supplied *IBS6 Industrial Analytics - Dataset Scales.pptx*, slides 3–4, and *Task 3 - Describe Data - Feature Description Table - Data Types.ipynb*: measurement scales, operations, dtype inspection and feature-table layout.
- Lecturer's “Verify Data Quality” screenshot supplied in the conversation: conformity, completeness, uniqueness, accuracy, timeliness, consistency. No page number asserted for this separate excerpt.
- Supplied Arias Chao et al. preprint, 20 April 2020, Tables 1–4, pp. 3–5; accompanying example notebook credited to Manuel Arias.
- Arias Chao et al. (2021), [Data 6(1), 5](https://doi.org/10.3390/data6010005); [Kaggle redistribution](https://www.kaggle.com/datasets/bishals098/nasa-cmapss-2-engine-degradation).
- AI drafting/coding assistance and pending human review: [AI use log](ai-use-log.md).

This report and `findings.html` are generated by `scripts/build_task3_report.py` from notebook exports. Edit reusable narrative there if regenerating; keep measured values tied to the exported evidence.
'''
(ROOT/'docs/05-data-understanding.md').write_text(report)

# Static HTML includes measured values and remains readable without JavaScript.
# Optional subset buttons filter the engine table only; all other figures compare both files.
file_millions={ds:sum(r['readings'] for r in ov if r['dataset']==ds)/1e6 for ds in ['DS01','DS02']}
page=f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="GR05 Task 3: verified data understanding findings from local NASA N-CMAPSS DS01 and DS02 engine histories.">
<meta name="theme-color" content="#eeede7"><title>Inside the data — GR05</title>
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="assets/site.css"><link rel="stylesheet" href="assets/findings.css">
<script src="assets/findings.js" defer></script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header wrap"><a class="wordmark" href="index.html"><span class="brand-icon" aria-hidden="true">✳</span> GR05<span class="wordmark-detail"> / RESEARCH NOTES</span></a><nav aria-label="Main navigation"><a href="index.html">Overview</a><a href="#quality">Data quality</a><a class="repo-link" href="https://github.com/Cukowski/GR05-Predictive-Maintenance">GitHub ↗</a></nav></header>
<main id="main">
<section class="findings-hero wrap" aria-labelledby="page-title"><div><p class="eyebrow"><span class="status-dot orange" aria-hidden="true"></span> TASK 03 / DATA UNDERSTANDING</p><h1 id="page-title">Inside<br>the <em>data.</em></h1><p class="hero-description">Before we predict,<br>we need to understand.</p><p class="hero-context">Two N-CMAPSS subsets. A guided investigation of engine histories, flight conditions, and what our labels actually mean.</p><div class="hero-actions"><a class="button primary" href="notebooks/01-data-understanding.ipynb" download>Get the notebook ↓</a><a class="text-link" href="https://github.com/Cukowski/GR05-Predictive-Maintenance/blob/main/notebooks/01-data-understanding.ipynb">Read on GitHub ↗</a></div></div>
<aside class="evidence-panel" aria-label="Analysis scope"><div class="evidence-label">EVIDENCE SNAPSHOT <span>{h(s['analysis_date'])}</span></div><span class="big-count">{t['readings']/1e6:.2f}<small>M</small></span><p>sensor readings inspected</p><div class="evidence-facts"><div><strong>{t['engines']}</strong><span>engine histories*</span></div><div><strong>{t['flights']:,}</strong><span>engine-flight pairs</span></div><div><strong>47</strong><span>stored fields</span></div></div><p class="evidence-footnote">*Dataset-scoped histories. Independence across subsets is unverified. Descriptive analysis only; no model results.</p><span class="evidence-line">DS01 / {file_millions['DS01']:.2f}M <span>DS02 / {file_millions['DS02']:.2f}M</span></span></aside></section>
<nav class="chapter-nav" aria-label="Findings sections"><div class="wrap"><a href="#structure">01 / Structure</a><a href="#labels">02 / Labels</a><a href="#signals">03 / Signals</a><a href="#quality">04 / Quality</a><a href="#next">05 / What’s next</a></div></nav>
<section id="structure" class="section wrap"><div class="section-label"><span>01 / KNOW THE UNIT OF ANALYSIS</span><span>READINGS ≠ FLIGHTS ≠ ENGINES</span></div><div class="section-heading"><h2>Millions of readings.<br>A small fleet.</h2><p>Repeated measurements give rich trajectories.<br>They do not create millions of independent engines.</p></div><div class="concept-flow"><article><span>01</span><h3>A reading</h3><p>One aligned operating/sensor observation. Stored row order is available; explicit timestamps are not.</p></article><article><span>02</span><h3>A flight</h3><p>Many readings with the same engine and cycle. Shared keys are expected, not duplicate errors.</p></article><article><span>03</span><h3>An engine history</h3><p>Repeated flights until simulated end-of-life. Keep engines separate when validating models.</p></article></div>
{h_table(summary_headers,summary_rows)}
<figure class="research-figure"><img src="reports/figures/engine_lifetimes.svg" alt="Bar charts of complete observed lifetimes for DS01 and DS02 engines, distinguished by development and test partition." width="1200" height="470" loading="lazy"><figcaption>Full-file counts · DS01: 75–100 cycles per engine · DS02: 59–89 cycles. Color denotes the provided split.</figcaption></figure>
<details class="data-details"><summary>Inspect all 19 engine histories</summary><div class="subset-filters" hidden><span>SHOW SUBSET</span><button type="button" data-subset="all" aria-pressed="true">Both</button><button type="button" data-subset="DS01" aria-pressed="false">DS01</button><button type="button" data-subset="DS02" aria-pressed="false">DS02</button></div><div id="engine-table">{h_table(engine_headers,engine_rows)}</div><p class="table-note">Shared unit numbers across subsets do not establish identity or independence. Filter controls affect this table only.</p></details>
</section>
<section id="labels" class="dark-section"><div class="section wrap"><div class="section-label"><span>02 / THE TARGET</span><span>RETROSPECTIVE, NOT A PREDICTION</span></div><div class="project-grid"><h2>One flight closer<br>to end-of-life.</h2><div><p class="lead">Every audited flight follows the same countdown convention.</p><div class="formula"><span>RUL</span> = <span>final cycle</span> − <span>current cycle</span></div><p class="dark-copy">A final observed cycle of 100 and a current cycle of 1 gives RUL 99. RUL stays constant within each flight and reaches zero on the final cycle.</p><p class="dark-note">The final lifetime is known retrospectively. Giving it to a model as an input would leak the answer.</p></div></div></div></section>
<section class="wrap chart-section"><figure class="research-figure"><img src="reports/figures/rul_trajectories.svg" alt="Development-engine RUL label trajectories decline by one per flight cycle and terminate at zero." width="1200" height="470" loading="lazy"><figcaption>Development labels, not fitted predictions. All engine-flight countdown checks passed in these local files.</figcaption></figure></section>
<section id="signals" class="section wrap"><div class="section-label"><span>03 / OPERATING CONDITIONS & SIGNALS</span><span>CONTEXT CHANGES THE READING</span></div><div class="section-heading"><h2>An engine doesn’t<br>fly in one condition.</h2><p>Altitude, Mach, throttle, and temperature change within a flight. Sensor changes can reflect those changes as well as degradation.</p></div><figure class="research-figure"><img src="reports/figures/single_flight.svg" alt="Four measured operating-condition profiles across the first DS01 development flight: altitude, Mach, throttle, and inlet temperature." width="1200" height="600" loading="lazy"><figcaption>First DS01 development flight · full flight, ordered sample index. The supplied DS02 preprint describes 1 Hz sampling; timestamps are not present for independent timing checks.</figcaption></figure>
<aside class="insight"><span class="eyebrow">THE GENERALIZATION QUESTION</span><h3>DS02’s test flights go beyond its development classes.</h3><p>All six development engines are long-flight class 3. The test set also includes short-flight class 1 and medium-flight class 2. This is a coverage difference to plan for, not a measured model failure.</p></aside>
<figure class="research-figure"><img src="reports/figures/operating_distributions.svg" alt="Sampled development operating-condition distributions for DS01 and DS02." width="1200" height="600" loading="lazy"><figcaption>12,000 evenly spaced development readings per subset · reading-weighted diagnostic samples, not exact population distributions.</figcaption></figure>
<div class="block-grid"><article><span>INPUT CANDIDATES</span><h3>18 physical channels</h3><p>4 operating conditions + 14 measured sensor channels. “Measured” describes the simulator channel type; engine responses are simulated.</p></article><article><span>KEEP THE ROLES CLEAR</span><h3>47 stored ≠ 47 predictors</h3><p>Virtual sensors, hidden health modifiers, labels, and metadata require different handling. The notebook documents each variable and unit.</p></article></div>
<details class="data-details"><summary>The number is not the meaning: measurement scales</summary><p class="table-note">Following the lecturer’s Dataset Scales slides 3–4 and feature-table notebook. Storage dtype and statistical meaning are separate. Discrete/continuous is also separate from measurement scale.</p>{h_table(['Variable','Meaningful scale','Why'],[['unit','Nominal','An ID, even when stored as float64'],['Fc','Ordinal','Short < medium < long; unequal category gaps'],['hs','Nominal','Healthy/degraded labels, not a physical quantity'],['cycle','Interval index · discrete','Differences count flights; index origin is chosen'],['RUL','Ratio · discrete','Count of remaining cycles; meaningful zero'],['T2 / T24 / T48','Ratio · continuous','Absolute temperature in Rankine'],['alt','Interval · continuous','Altitude relative to a datum'],['P2 / stall margins','Unconfirmed','Source definition or zero-point convention needs checking']])}<p class="table-note">Throttle and simulator-modifier interval classifications are working interpretations. The full <a href="reports/results/feature_description_table.csv">lecturer-style feature table</a> labels exact counts/ranges and sampled unique counts.</p></details>
<details class="data-details"><summary>Explore sensor trends, distributions, and correlations</summary><figure class="research-figure"><img src="reports/figures/sensor_cycle_trends.svg" alt="DS01 development sensor means over cycles standardized within each engine." width="1300" height="430" loading="lazy"><figcaption>Whole-flight means standardized within each complete development engine for display. Uses future history; not an operational preprocessing method.</figcaption></figure><figure class="research-figure"><img src="reports/figures/sensor_distributions.svg" alt="Box plots of Wf fuel flow and T48 temperature in development diagnostic samples." width="1200" height="450" loading="lazy"><figcaption>Sampled distributions. Tukey-fence outliers are flags to investigate, not proven errors.</figcaption></figure><figure class="research-figure correlation-figure"><img src="reports/figures/development_correlation.svg" alt="Pearson correlation heatmap of DS01 development-sample operating conditions, sensor channels, and RUL." width="1000" height="800" loading="lazy"><figcaption>Pearson correlation on DS01 development sample. Operating regimes and temporal dependence confound interpretation; no causal or predictive claim.</figcaption></figure></details>
</section>
<section id="quality" class="quality-section"><div class="section wrap"><div class="section-label"><span>04 / VERIFY DATA QUALITY</span><span>SIX DIMENSIONS, EXPLICIT LIMITS</span></div><div class="section-heading"><h2>Clean numbers.<br>Careful conclusions.</h2><p>{t['numeric_cells']:,} numeric cells scanned.<br>No NaN or infinite values found. That alone does not prove the data is error-free.</p></div><div class="quality-grid">{''.join(f'<article><span class="quality-index">0{i+1}</span><h3>{h(r["dimension"])}</h3><p>{h(r["finding"])}</p><details><summary>Coverage & limits</summary><p><strong>Scope:</strong> {h(r["scope"])}</p><p>{h(r["limitation"])}</p></details></article>' for i,r in enumerate(s['quality']))}</div><p class="quality-footnote">No raw values removed or imputed. Global non-adjacent duplicates have not been exhaustively checked. Accuracy against physical reference measurements is unverified. The P2 sensor definition/unit and Kaggle version/terms remain open.</p></div></section>
<section id="next" class="section wrap"><div class="section-label"><span>05 / FROM UNDERSTANDING TO PREPARATION</span><span>PROPOSED NEXT STEPS</span></div><div class="section-heading"><h2>Build on what<br>we can explain.</h2><p>Start with DS01. Define when a prediction is made. Preserve engines and chronology. Then establish a baseline.</p></div><div class="next-grid"><article><h3>Keep the split honest</h3><p>Use separate development engines for validation and fit preprocessing on training engines only. This EDA exposed test structure and labels; avoid tuning to those test results.</p></article><article><h3>Make the features defensible</h3><p>Consider current-flight summaries from W + X_s. Exclude future cycles, known final lifetimes, true RUL, and hidden simulator health.</p></article><article><h3>Measure later</h3><p>MAE and RMSE will follow trained-model evaluation. There are no model scores, measured savings, or operational aviation claims yet.</p></article></div>
<div class="evidence-downloads"><div><p class="eyebrow">FOLLOW THE EVIDENCE</p><h3>Read. Re-run. Question.</h3><p>The notebook explains each step. The report collects the findings. Small exported tables keep every number traceable.</p></div><div class="download-links"><a href="notebooks/01-data-understanding.ipynb" download>Executed Jupyter notebook <span>↓</span></a><a href="docs/05-data-understanding.md">Task 3 report <span>↗</span></a><a href="reports/results/feature_dictionary.csv" download>Feature dictionary · CSV <span>↓</span></a><a href="reports/results/task3_summary.json">Audit summary & file hashes · JSON <span>↗</span></a></div></div>
<details class="data-details"><summary>Source notes & reproducibility</summary><p>Source files: N-CMAPSS_DS01-005.h5 and N-CMAPSS_DS02-006.h5. Analysis date: {h(s['analysis_date'])}. Read-only chunks of {s['configuration']['chunk_rows']:,} rows; sample size {s['configuration']['sample_rows_per_partition']:,} per partition.</p><p>Reference: accompanying seven-page April 2020 preprint (DS02-focused), Tables 1–4 and pp. 3–5; example notebook credited to Manuel Arias; wider collection: <a href="https://doi.org/10.3390/data6010005">Arias Chao et al. (2021)</a>. Real flight profiles drive simulated degradation and sensor responses.</p><p>Task scope follows the supplied task PDF, p. 1. The scales follow the supplied Dataset Scales PPTX (slides 3–4) and feature-description example notebook. The six quality dimensions follow the lecturer excerpt provided by the team. Source version/redistribution rights remain unverified. <a href="docs/ai-use-log.md">AI assistance disclosure</a>.</p><p>Run the notebook, then <code>python scripts/build_task3_report.py</code>. Generated values come from <code>reports/results/task3_summary.json</code> and the exported tables, not live engine telemetry.</p></details>
</section>
</main><footer class="wrap site-footer"><a class="wordmark" href="index.html">GR05 <span class="wordmark-detail">/ PREDICTIVE MAINTENANCE</span></a><p>Data understanding · {h(s['analysis_date'])}</p><a href="index.html">Back to the overview ↗</a></footer>
</body></html>
'''
(ROOT/'findings.html').write_text(page)
print('Generated docs/05-data-understanding.md and findings.html from executed evidence.')
