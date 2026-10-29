"""Generate Task 4 report/page from actual preparation evidence; no raw data access."""
from pathlib import Path
import csv
import html
import json
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/'reports/results/task4'
if not (E/'manifest.json').exists():raise SystemExit('Run scripts/prepare_data.py or the Task 4 notebook first.')
m=json.loads((E/'manifest.json').read_text())

def read(name):
    with (E/name).open(newline='') as f:return list(csv.DictReader(f))

def mdtable(headers,rows):
    return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |',
        *['| '+' | '.join(str(x).replace('|','/') for x in row)+' |' for row in rows]])

def esc(v):return html.escape(str(v))

def table(headers,rows):
    return '<div class="table-scroll"><table><thead><tr>'+''.join(f'<th scope="col">{esc(h)}</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join(f'<td>{esc(v)}</td>' for v in row)+'</tr>' for row in rows)+'</tbody></table></div>'

splits=read('split_summary.csv');engines=read('engine_splits.csv');catalog=read('feature_catalog.csv')
audit=read('cleaning_audit.csv');impute=read('imputation_parameters.csv');preview=read('prepared_preview.csv')
headers=['Subset','Original partition','Prepared split','Flights','Histories','Original readings']
rows=[[r[k] for k in ['dataset','source_partition','split','flights','histories','raw_readings']] for r in splits]
feature_rows=[[r[k] for k in ['feature','family','source','unit','definition']] for r in catalog]
selected_impute=[r for r in impute if int(r['missing_all'])>0]
comparison=[['Raw','One ordered reading',m['raw_readings'],'47 stored fields; six aligned blocks'],
 ['Prepared','One completed flight',m['processed_flights'],'45 physical/history features + metadata + RUL'],
 *[[s.title(),'One completed flight',shape[0],str(shape[1])+' finite model inputs; target separate'] for s,shape in m['matrix_shapes'].items()],
 ['Quarantine','One completed flight',m['quarantined_flights'],'Retained; no fitting, validation, or test scoring']]
with (E/'raw_processed_comparison.csv').open('w',newline='') as f:
    writer=csv.writer(f,lineterminator='\n');writer.writerow(['stage','row_meaning','rows','representation']);writer.writerows(comparison)
artifact_rows=[[r['file'],f"{r['bytes']:,}",r['sha256']] for r in m['artifacts']]
raw_rows=[[r['file'],f"{r['bytes']:,}",r['sha256']] for r in m['raw_files']]
local=f"data/processed/{m['version_id']}"
report=f'''# Task 4 — Data Preparation and Feature Engineering

**GR05 · Industrial Analytics · HFU · WS 2026/27**<br>
**Team:** Selçuk Ata Aksoy and Denzel Gregory Pragassa<br>
**Prepared version:** `{m['version_id']}`<br>
**Run:** {m['created_at']}<br>
**Status:** Pipeline executed, modeling inputs exported; team interpretation review pending. No RUL prediction model trained.

## 1. What this task means

Task 3 examined what is in our files. Task 4 turns those observations into a repeatable, well-defined input for a future model. A model cannot automatically know which columns are labels, which values use different units, or which engine histories must stay separate. Those are preparation decisions we must explain.

The supplied `tasks/IBS6 Industrial Analytics Project Tasks V4.0.pdf`, p. 2, dated 26 October 2026 (internal heading V12.0), asks for cleaning, transformation/normalization, feature engineering, integration and versioned data. All requested deliverables are provided:

| Deliverable | Actual artifact |
|---|---|
| Cleaned dataset ready for modeling | `{local}/flights_features.csv`; finite `X_*.csv`, separate `y_*.csv` and matching `rows_*.csv` |
| Preprocessing pipeline | `src/preprocessing.py`, `config/preprocessing.json`, CLI `scripts/prepare_data.py`; saved fitted `preprocessor.joblib` in the local version |
| Feature engineering documentation | This report, executed `notebooks/02-preprocessing.ipynb`, full `feature_catalog.csv` |
| Versioned raw/processed comparison | Raw SHA-256 identity, code/config/environment fingerprint, immutable local prepared version, artifact checksums, compact comparison/audit evidence |

## 2. Understand the data without machine-learning terminology

Think of each engine as a diary. A **reading** is a detailed snapshot during a flight. A **flight** groups many snapshots. A **history** groups that engine's flights in order. The historical **RUL** is the number of remaining flight cycles until simulated end-of-life.

Our original files contain **{m['raw_readings']:,} readings**, arranged in **{m['engine_histories']} dataset-scoped histories**. They are not 14 million independent engines. The simulation uses real flight operating profiles; degradation and sensor responses are simulated, not measured actual engine failures. Independence between subsets is unresolved.

For this version we make a prediction **at the end of a completed flight**. Everything in that flight and previous observed flights is available; tomorrow's measurements and the known final failure cycle are not. Therefore the prepared dataset has **{m['processed_flights']:,} flight rows**. This is the prediction contract, not just a convenient reduction in file size.

| Kind of entry | Examples | Meaning and relevance |
|---|---|---|
| Operating conditions (W) | altitude, Mach, throttle, inlet temperature | Describe the flight situation; sensor values can change because conditions changed |
| Sensor channels (X_s) | temperatures, pressures, fuel flow, fan/core speed | Describe engine response; combine them with operating context |
| Target (Y) | RUL | Historical answer for training/evaluation, kept separately as y |
| Metadata (A) | unit, cycle, flight class | Identify/order/group histories and describe coverage; not predictors here |
| Source collection | DS01 / DS02 | Categorical context for the combined table, encoded as two source indicators |
| Simulator-only information | virtual X_v, health modifiers T, health state hs | Excluded from baseline inputs; not assumed available from physical sensors |
| Unresolved measured channel | P2 | Excluded pending source definition/unit confirmation |

`X` means the inputs a future model may see; `y` means the answer. Unit 10 is a label, not twice unit 5. RUL is a count in flight cycles. Temperatures are absolute Rankine in the source, not Celsius. The distinction between stored numeric dtype and measurement meaning follows the lecturer's scale guide from Task 3.

### An actual prepared entry

The preview export contains DS01 unit {preview[0]['unit']}, flight {preview[0]['cycle']}, with {int(float(preview[0]['n_readings'])):,} readings, mean altitude {float(preview[0]['alt_m_mean']):.2f} m and mean T48 {float(preview[0]['T48_K_mean']):.2f} K. Its historical RUL is {preview[0]['RUL']} cycles. Its previous-flight difference is missing because this is the first observed flight. Filling that missing predictor does not mean changing the historical RUL.

## 3. Cleaning and consistency decisions

{mdtable(['Subset','Partition','Readings','Non-finite predictor cells','Impossible predictor cells','Readings removed'],[[r[k] for k in ['dataset','partition','raw_readings','predictor_nonfinite','impossible_predictor_values','readings_removed']] for r in audit])}

The run found **{m['predictor_nonfinite']} non-finite selected predictor cells**, **{m['impossible_predictor_values']} unambiguously impossible selected predictor cells**, and removed **{m['readings_removed']} raw readings**. We report zeros because that is the observed result. This is not a proof of physical accuracy or absence of every possible sentinel.

The pipeline supports NaN/infinity handling by converting invalid predictor values to missing before aggregation. Non-positive absolute temperatures, pressures and shaft speeds, and negative Mach/fuel flow are treated as impossible under this scoped representation. Finite unusual values are retained; IQR flags are not deletion rules. Altitude is not required to be positive as a universal physical rule because its reference datum matters.

Keys, flight class and targets must be valid: positive integer engine/cycle IDs, class in 1/2/3, nonnegative integer RUL, aligned arrays. Bad keys or labels stop the run; they are not median-imputed or reconstructed. Within-flight target/class conflicts, backward/noncontiguous cycles and inconsistent retrospective RUL labels also stop the run. Duplicate aggregate keys are prohibited; repeated raw unit/cycle pairs are expected because a flight has many readings. Global exact raw-row deduplication is not performed.

After aggregation and causal feature engineering there are **{m['missing_numeric_features']} missing feature cells**, all in previous-flight differences at the beginning of histories. Training has {m['missing_by_split']['train']}, validation {m['missing_by_split']['validation']}, test {m['missing_by_split']['test']}, quarantine {m['missing_by_split']['quarantine_test_related']}. First-flight gaps are expected, rather than newly discovered broken sensors.

## 4. Physical transformations and aggregation

Seventeen channels are retained: W's four operating conditions plus thirteen X_s channels. P2 is excluded. Units are converted before computing flight statistics:

| Conversion | Formula |
|---|---|
| ft → m | × 0.3048 |
| absolute °R → K | × 5/9 |
| psia → kPa | × 6.894757293168 |
| lb/s → kg/s | × 0.45359237 |
| Mach, throttle %, rpm | retained |

Each flight's mean and sample standard deviation (ddof 1) use all finite selected readings. Within-chunk moments are combined with stable weighted moment formulas across chunk boundaries. The count `n_readings` counts original observations, not finite cells, and is not claimed to be verified seconds. Unit conversions are fixed mathematical transformations; they do not learn from validation/test data.

Whole-flight summaries mix climb/cruise/descent. They are a manageable initial representation, not a demonstrated isolation of causal degradation. Future phase-based features require a separate justified preparation version.

## 5. Dataset integration and conservative split policy

The prepared flight tables are appended under a common schema with explicit source identity. A source history uses `dataset:unit` (e.g. DS01:2); the split grouping additionally links equal raw unit IDs across subsets conservatively. Equal IDs do not prove identical physical engines, but ignoring the uncertainty could let related histories cross splits.

**Critical conflict:** DS01 unit 10 is supplied test; DS02 unit 10 is supplied development. Its **{m['quarantined_flights']} DS02 development flights are retained in quarantine**, and used in neither training nor validation nor test scoring. Original test rows retain their supplied designation.

Validation IDs **5, 6, 18** are fixed in configuration before any performance experiment. Other eligible development histories become training. This yields:

{mdtable(headers,rows)}

Training spans 7 source histories but only 6 conservative unit-ID groups; validation spans 4 source histories and 3 conservative groups. Test has 7 source histories/groups. These are not a proof of total independence; unrecognized cross-ID dependence remains possible. The preprocessor fits only on the **{m['fitting_rows']} training flights**. This version integrates both subsets; the simpler DS01-only scope remains available by selecting the DS01 histories under the same grouping policy and refitting preprocessing.

![Integrated flight allocation](../reports/figures/task4_split_allocation.svg)

Task 3 inspected test structure/labels. That exposure is documented and must not become adaptive tuning. The arbitrary fixed validation choice is a starting protocol, not a statistically optimal holdout. Later grouped cross-validation must fit imputer/scaler/encoder again inside each training fold.

## 6. Feature engineering catalog

There are **{m['numeric_features']} numeric candidates**: 17 means + 17 within-flight standard deviations + 1 reading count + 3 trailing means + 3 previous-flight differences + 4 physical combinations. Source identity is the only categorical input. The baseline selection uses just 17 means + reading count + 2 source indicators = **{m['baseline_columns']} columns**.

Trailing means use current and up to two previous flight means, separately within a source history; no centered windows or backward filling. Differences use current minus immediately previous flight. The first difference is undefined. Pressure/speed ratios are **ratios of flight means**, not averages of instantaneous ratios. They are diagnostics, not calibrated health or efficiency estimates.

{mdtable(['Feature','Family','Source','Unit','Definition'],feature_rows)}

![Causal historical feature](../reports/figures/task4_causal_history.svg)

No target, engine ID, cycle index, final lifetime, healthy/degraded flag, flight-class code, virtual sensor or health modifier enters the feature matrix. Dataset source is allowed only as categorical context, not a claim of degradation. All statistics are available by the end of the current flight.

## 7. Fitted preprocessing: missing values, encoding, scaling

The saved scikit-learn `ColumnTransformer` contains:

1. Numeric `SimpleImputer(strategy='median', add_indicator=True, keep_empty_features=True)` fitted on training flights only.
2. `StandardScaler` fitted to those imputed numeric features and their missingness indicators (training standard deviation with ddof 0; zero-variance scale becomes 1).
3. `OneHotEncoder` for the declared DS01/DS02 source categories; source columns stay unscaled 0/1. Unexpected source categories raise an error.

The actual missing-value features and learned medians are:

{mdtable(['Feature','Training median','Missing training','Missing all histories'],[[r[k] for k in ['feature','training_median','missing_train','missing_all']] for r in selected_impute])}

The numeric 45 inputs gain three missingness indicators, then two source indicators: **{m['model_columns']} model columns** in total. Numeric missingness indicators are standardized along with numeric features, so their matrix values are no longer literal 0/1. The full readable feature table preserves physical units and missing cells; the finite X matrices are the imputed/scaled representation.

All active X matrices are finite and use the same column order. `y_*.csv` retains unchanged RUL in flight cycles. `rows_*.csv` provides matching identity and grouping fields in exactly the same order.

Maximum absolute fitted numeric training column mean after standardization: **{m['fit_numeric_max_abs_mean']:.3g}** (floating-point tolerance). Validation/test do not have to be centered or within a fixed range. Scaling is not operating-regime correction and does not prove better RUL performance.

![Before/after training standardization](../reports/figures/task4_scaling.svg)

Official references: [scikit-learn common pitfalls](https://scikit-learn.org/stable/common_pitfalls.html), [SimpleImputer](https://scikit-learn.org/stable/modules/generated/sklearn.impute.SimpleImputer.html), [StandardScaler](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html), [OneHotEncoder](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html).

## 8. Raw vs prepared comparison and versioning

{mdtable(['Stage','Row meaning','Rows','Representation'],comparison)}

Raw file identity is retained, without rewriting/copying the raw dataset into Git:

{mdtable(['Raw file','Bytes','SHA-256'],raw_rows)}

Prepared data is stored locally at **`{local}/`**. The version fingerprint combines raw file hashes, configuration, preprocessing/helper code hashes, Python and relevant package versions. Every output artifact has a recorded checksum; matching versions are verified/reused. Changed code, policy, data or dependency versions produce a new directory. Existing output files are not silently overwritten.

`manifest.json` describes this version; it lists artifact hashes but is not self-hashed. It is an integrity record for local reproducibility, not a cryptographic signature or upstream provenance certificate.

{mdtable(['Local artifact','Bytes','SHA-256'],artifact_rows)}

`flights_features.csv` includes all rows and original labels, including quarantine; no separate X/y quarantine matrices are made because those rows are not intended for scoring. `preprocessor.joblib` is a fitted transformation, not an RUL predictor. `baseline_columns.json` defines the smaller input selection. Raw and processed files remain ignored by Git; compact manifests, summaries, feature definitions and figures under `reports/` can be reviewed/versioned in Git.

## 9. Reproduce and use the results

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/prepare_data.py
python -m jupyterlab
# Run notebooks/02-preprocessing.ipynb top to bottom for explanations and figures.
python scripts/build_task4_report.py
python -m unittest discover -s tests -v
```

The CLI builds or verifies the prepared version and exports compact evidence. The notebook executes the same pipeline, explains the decisions, verifies matrices, demonstrates that held-out transformations do not refit training parameters, and saves three preparation figures. The report/page generator reads those actual exports. Use the version manifest rather than guessing a directory name.

For the first modeling experiment, load `X_train.csv` and `y_train.csv`, choose `baseline_columns.json`, and use the corresponding validation files. Keep `rows_*.csv` for per-engine metrics. If changing validation groups or using cross-validation, refit preprocessing accordingly. Final test should follow model selection; do not treat repeated row samples as independent engines.

Targeted tests cover chunk-boundary aggregation and unit conversions, non-finite handling, causal/history isolation, cross-subset test quarantine, training-only medians/scaling, and unknown-category rejection. The original Task 3 tests also remain available. No RUL model is fitted and no MAE/RMSE is asserted.

## 10. Limitations and next decisions

- A small number of conservative engine groups limits confidence; the 50-column candidate set is not validated and a 20-column baseline is provided.
- Unit-based conservative linking addresses one known risk, but cross-subset independence remains unresolved; it can also over-group unrelated engines.
- Whole-flight summaries mix phases, lose detailed transient ordering and can retain operating-regime effects. Reading count may encode flight-class/source differences.
- Dataset indicators can encourage source-specific rules. Compare DS01-only and integrated experiments on development validation rather than assuming pooling helps.
- Source version and Kaggle redistribution terms still need confirmation; unresolved P2 is excluded, not silently assigned a definition.
- Data is simulated. No operational aviation validation, economic savings, or predictive accuracy is established by successful preprocessing.

Next: review the representation with both team members, then fit and compare transparent baseline models using held-out engine groups and MAE/RMSE in cycles. Include per-engine and macro averages alongside any overall flight-weighted result.

## 11. Sources and AI disclosure

Task requirements: supplied Project Tasks V4.0, p. 2, 26 October 2026. Physical meaning: Task 3 report and supplied N-CMAPSS preprint/example; measurement scales: lecturer's Dataset Scales guide. Pipeline API behavior: official scikit-learn links above. AI coding/drafting assistance and human review status: [AI use log](ai-use-log.md).

This report and `preparation.html` are generated from `scripts/build_task4_report.py`; edit narrative there if regenerating, and keep measured results tied to the manifest and CSV exports.
'''
(ROOT/'docs/06-data-preparation.md').write_text(report)

first=preview[0]
page=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="GR05 Task 4: how raw engine readings become versioned, modeling-ready flight data."><meta name="theme-color" content="#eeede7"><title>Ready for the next cycle — GR05</title><link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="assets/site.css"><link rel="stylesheet" href="assets/findings.css"></head>
<body><a class="skip-link" href="#main">Skip to content</a><header class="site-header wrap"><a class="wordmark" href="index.html"><span class="brand-icon" aria-hidden="true">✳</span> GR05<span class="wordmark-detail"> / DATA PREPARATION</span></a><nav aria-label="Main navigation"><a href="index.html">Overview</a><a href="findings.html">Data findings</a><a class="repo-link" href="https://github.com/Cukowski/GR05-Predictive-Maintenance">GitHub ↗</a></nav></header>
<main id="main"><section class="findings-hero wrap" aria-labelledby="page-title"><div><p class="eyebrow"><span class="status-dot orange" aria-hidden="true"></span> TASK 04 / DATA PREPARATION</p><h1 id="page-title">Ready for<br>the next <em>cycle.</em></h1><p class="hero-description">From millions of snapshots<br>to one clear flight entry.</p><p class="hero-context">Before a model learns, we decide what it may see. Here is how we clean, summarize, split, and version the engine data.</p><div class="hero-actions"><a class="button primary" href="notebooks/02-preprocessing.ipynb" download>Get the guided notebook ↓</a><a class="text-link" href="docs/06-data-preparation.md">Read Task 4 report ↗</a></div></div><aside class="evidence-panel" aria-label="Preparation results"><div class="evidence-label">PREPARED FLIGHTS <span>{esc(m['created_at'][:10])}</span></div><span class="big-count">{m['processed_flights']:,}</span><p>completed flights, explicitly represented</p><div class="evidence-facts"><div><strong>{m['matrix_shapes']['train'][0]}</strong><span>training flights</span></div><div><strong>{m['matrix_shapes']['validation'][0]}</strong><span>validation flights</span></div><div><strong>{m['matrix_shapes']['test'][0]}</strong><span>test flights</span></div></div><p class="evidence-footnote">{m['quarantined_flights']} additional flights retained in quarantine. {m['model_columns']} candidate model inputs; {m['baseline_columns']}-column simpler baseline available. No prediction model trained.</p><span class="evidence-line">{esc(m['version_id'])}</span></aside></section>
<nav class="chapter-nav" aria-label="Page sections"><div class="wrap"><a href="#meaning">01 / Understand</a><a href="#prepare">02 / Prepare</a><a href="#split">03 / Keep apart</a><a href="#version">04 / Reproduce</a></div></nav>
<section id="meaning" class="section wrap"><div class="section-label"><span>01 / WHAT IS AN ENTRY?</span><span>EXPLAIN IT BEFORE MODELING IT</span></div><div class="section-heading"><h2>An engine diary.<br>One flight per entry.</h2><p>A raw row is a snapshot. A prepared row summarizes a completed flight. An engine history puts those flights in order.</p></div><div class="concept-flow"><article><span>READING</span><h3>A moment in flight</h3><p>Altitude, speed, temperature, pressure and fuel flow describe what the engine is doing under particular operating conditions.</p></article><article><span>FLIGHT</span><h3>A useful summary</h3><p>Means, variation, and earlier-flight changes become inputs available at the end of the current flight.</p></article><article><span>ANSWER</span><h3>Remaining useful life</h3><p>Historical RUL says how many flight cycles remained. It stays separate from the inputs, so the model cannot see the answer.</p></article></div>
<aside class="insight"><span class="eyebrow">ONE ACTUAL PREPARED ENTRY</span><h3>DS01 · engine {esc(first['unit'])} · flight {esc(first['cycle'])}</h3><p>{int(float(first['n_readings'])):,} readings summarize this flight. Mean altitude: {float(first['alt_m_mean']):,.1f} m. Mean T48: {float(first['T48_K_mean']):,.1f} K. Historical target: {esc(first['RUL'])} remaining cycles. No previous-flight change exists yet because it is the first observed flight.</p></aside>
<details class="data-details"><summary>Which columns are useful, and which stay out?</summary>{table(['Entry type','Use'],[['Operating conditions W','4 channels: describe the mission context'],['Measured sensors X_s','13 channels: pressures, temperatures, flows and shaft speeds'],['P2','Excluded while its definition/unit is unresolved'],['Unit and cycle','Order/group metadata, not predictors'],['Flight class','Coverage diagnostics only'],['DS01 / DS02','Source identity encoded as two categorical indicators'],['RUL','Target y, separate from feature matrix X'],['Hidden simulator T / X_v / hs','Excluded from the sensor-based candidate representation']])}<p>Simulation responses driven by realistic flight profiles are not observations of real engine failures. An ID stored as a number is still a label. Absolute Rankine temperatures become Kelvin, not Celsius.</p></details></section>
<section id="prepare" class="quality-section"><div class="section wrap"><div class="section-label"><span>02 / THE PREPARATION PIPELINE</span><span>PLAIN RULES, TRACEABLE RESULTS</span></div><div class="section-heading"><h2>Consistent inputs.<br>Visible decisions.</h2><p>Preparation decides what a model may learn from. It does not establish how accurately that model will predict.</p></div><div class="quality-grid"><article><span class="quality-index">01</span><h3>Clean carefully</h3><p>{m['predictor_nonfinite']} non-finite and {m['impossible_predictor_values']} impossible selected predictor values found. {m['readings_removed']} readings deleted. Rare finite values remain; inconsistent keys or labels stop the pipeline.</p></article><article><span class="quality-index">02</span><h3>Use common units</h3><p>Altitude in metres, temperatures in Kelvin, pressures in kPa, fuel flow in kg/s. Raw files keep their original values.</p></article><article><span class="quality-index">03</span><h3>Summarize flights</h3><p>17 channel means + 17 spreads + a reading count. Whole-flight averages are manageable; they still mix mission phases.</p></article><article><span class="quality-index">04</span><h3>Look backward only</h3><p>Three trailing means and three previous-flight changes use current or earlier flights. Four physical combinations add diagnostic candidates.</p></article><article><span class="quality-index">05</span><h3>Fill what is missing</h3><p>{m['missing_numeric_features']} expected gaps occur in first-flight differences. Training medians fill them; three extra indicators retain that information.</p></article><article><span class="quality-index">06</span><h3>Encode & scale</h3><p>Two source-category indicators. Numeric features and missingness indicators use training means and scales only. No target or engine ID enters X.</p></article></div></div></section>
<section class="section wrap"><div class="section-heading"><h2>A feature is a question<br>we ask of the flight.</h2><p>Was the temperature high? Did it vary? Has it changed since the previous flight? Every candidate has an explicit formula.</p></div><figure class="research-figure"><img src="reports/figures/task4_causal_history.svg" width="1000" height="420" alt="DS01 engine 1 current-flight temperature means compared with a trailing three-flight mean using no future flights." loading="lazy"><figcaption>Current plus up to two previous flights. No centered window, future measurements or final-lifetime normalization.</figcaption></figure><details class="data-details"><summary>Inspect all 45 numeric candidate features</summary>{table(['Feature','Unit','Meaning'],[[r['feature'],r['unit'],r['definition']] for r in catalog])}<p>A smaller 20-column baseline selection is also exported. Extra features are candidates to validate later, not evidence of improved prediction.</p></details><figure class="research-figure"><img src="reports/figures/task4_scaling.svg" width="1100" height="420" alt="Histogram of training T48 flight means in Kelvin before scaling and in training standard scores after scaling." loading="lazy"><figcaption>Standardization makes numerical scales comparable. It is not a correction for operating-regime differences, and does not prove predictive accuracy. Validation/test use the same fitted training rules.</figcaption></figure></section>
<section id="split" class="dark-section"><div class="section wrap"><div class="section-label"><span>03 / KEEP RELATED HISTORIES TOGETHER</span><span>THE UNIT-10 CONFLICT</span></div><div class="project-grid"><h2>Combine the schema.<br>Respect the histories.</h2><div><p class="lead">An ID appears in test in one collection and development in the other.</p><p class="dark-copy">DS01 unit 10 is provided test; DS02 unit 10 is provided development. Independence is unresolved. We conservatively link equal IDs and retain the {m['quarantined_flights']} DS02 flights outside training, validation and scoring.</p><p class="dark-note">Validation IDs 5, 6 and 18 are fixed by policy, not chosen using performance. Other eligible development histories are training. The supplied test histories remain test.</p></div></div></div></section>
<section class="section wrap"><figure class="research-figure"><img src="reports/figures/task4_split_allocation.svg" width="1000" height="430" alt="Stacked counts of DS01 and DS02 completed flights allocated to training, validation, provided test and quarantine." loading="lazy"><figcaption>Train {m['matrix_shapes']['train'][0]} · validation {m['matrix_shapes']['validation'][0]} · test {m['matrix_shapes']['test'][0]} · quarantine {m['quarantined_flights']}. Training contains six conservative groups, not 574 independent engines.</figcaption></figure>{table(headers,rows)}<p class="quality-footnote">Conservative grouping reduces a known risk; it does not prove complete independence. Task 3 test exposure is documented. Later grouped cross-validation must refit preprocessing inside each training fold.</p></section>
<section id="version" class="section wrap"><div class="section-label"><span>04 / VERSIONED & READY FOR MODELING</span><span>RAW → PHYSICAL FEATURES → MODEL INPUTS</span></div><div class="section-heading"><h2>Same sources.<br>A reproducible next step.</h2><p>Original HDF5 files stay unchanged. Versioned CSVs, aligned labels and metadata, and fitted preprocessing stay local.</p></div>{table(['Stage','Row meaning','Rows','Representation'],comparison)}<aside class="insight"><span class="eyebrow">LOCAL DATASET VERSION</span><h3>{esc(m['version_id'])}</h3><p><code>{esc(local)}/</code></p><p>The fingerprint records raw bytes, code, configuration and package versions. Saved files are checksum-verified before reuse; changed inputs create a new version. Raw/processed datasets remain outside Git.</p></aside><div class="evidence-downloads"><div><p class="eyebrow">READ · RUN · EXPLAIN</p><h3>The deliverables.</h3><p>Run the guided notebook or <code>python scripts/prepare_data.py</code>. Rebuild this page/report with <code>python scripts/build_task4_report.py</code>. No prediction model is trained here.</p></div><div class="download-links"><a href="notebooks/02-preprocessing.ipynb" download>Executed Task 4 notebook <span>↓</span></a><a href="docs/06-data-preparation.md">Feature engineering & preparation report <span>↗</span></a><a href="reports/results/task4/manifest.json">Version manifest & artifact hashes <span>↗</span></a><a href="reports/results/task4/feature_catalog.csv" download>Feature catalog · CSV <span>↓</span></a><a href="reports/results/task4/raw_processed_comparison.csv" download>Raw vs prepared comparison · CSV <span>↓</span></a></div></div><details class="data-details"><summary>Limitations and what comes next</summary><p>Only a few engine groups, phase mixing, collection effects and unresolved cross-subset independence limit conclusions. Source version/terms still need confirmation. The candidate features are not validated indicators of wear.</p><p>Next: fit a transparent baseline, compare simple regressors with development-engine validation, then evaluate final test. Report MAE/RMSE in flight cycles and per-engine errors. No operational aviation suitability or measured savings is claimed.</p><p>Task requirements: supplied Project Tasks V4.0 PDF, p. 2, dated 26 October 2026. More context: <a href="findings.html">Task 3 findings</a>, <a href="docs/ai-use-log.md">AI assistance disclosure</a>, and the official scikit-learn sources linked in the report.</p></details></section></main><footer class="wrap site-footer"><a class="wordmark" href="index.html">GR05 <span class="wordmark-detail">/ PREDICTIVE MAINTENANCE</span></a><p>Data preparation · {esc(m['created_at'][:10])}</p><a href="index.html">Back to overview ↗</a></footer></body></html>
'''
(ROOT/'preparation.html').write_text(page)
print('Generated Task 4 report, comparison CSV, and preparation.html for',m['version_id'])
