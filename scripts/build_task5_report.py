"""Generate measured Task 5 report/dashboard from executed notebook exports."""
from pathlib import Path
import csv,json,html,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from src.descriptive_analysis import insight_markdown
E=ROOT/'reports/results/task5'
if not (E/'training_insights.json').exists():raise SystemExit('Run notebooks/03-descriptive-analysis.ipynb first.')
i=json.loads((E/'training_insights.json').read_text());p=json.loads((E/'analysis_provenance.json').read_text())
def read(name):
 with (E/name).open(newline='') as f:return list(csv.DictReader(f))
def mt(headers,rows):return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |',*['| '+' | '.join(map(str,row))+' |' for row in rows]])
def ht(headers,rows):return '<div class="table-scroll"><table><thead><tr>'+''.join('<th scope="col">'+html.escape(str(c))+'</th>' for c in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+html.escape(str(c))+'</td>' for c in row)+'</tr>' for row in rows)+'</tbody></table></div>'
corr=read('train_per_engine_correlations.csv');val=read('validation_per_engine_correlations.csv');stats=read('train_descriptive_statistics.csv')
val_t=[float(r['r_with_RUL']) for r in val if r['sensor']=='T48_K_mean']
condition_rows=[[r['life_stage'],f"{r['alt_m_mean']:.1f}",f"{r['Mach_mean']:.3f}",f"{r['TRA_pct_mean']:.2f}"] for r in i['condition_stage_medians']]
summary_rows=[[r[''],r['count'],f"{float(r['mean']):.3f}",f"{float(r['std']):.3f}",f"{float(r['min']):.3f}",f"{float(r['max']):.3f}"] for r in stats]
figures=[('01_train_rul_histogram','Training RUL distribution','574 flights, 7 source histories, 6 conservative groups. RUL spans 0–99 cycles.'),
('02_sensor_trajectories','Sensor trajectories','T48 in Kelvin, Nc in rpm, Wf in kg/s. Operating conditions and engine/source differences remain.'),
('03_train_correlation_heatmap','Training correlations','Descriptive Pearson correlations; repeated flights are dependent. No p-values or causal claims.'),
('04_life_stage_sensor_boxplots','Retrospective RUL-stage comparison','One median per source history and stage; Late 0–20, Middle 21–50, Early >50. Groups use true RUL, never deployable inputs.'),
('05_operating_conditions','Operating context','Flight-weighted distributions, not engine-median comparisons. Regime variation can confound sensor–RUL associations.'),
('06_previous_flight_changes','Previous-flight differences','567 nonmissing values per channel; 7 expected first-flight gaps. Added predictive value is untested.')]
report=f'''# Task 5 — Initial Descriptive Analysis

**GR05 · Industrial Analytics · HFU · WS 2026/27**<br>
**Evidence executed and reviewed:** 11 November 2026<br>
**Analysis foundation:** Denzel Gregory Pragassa; reproducibility/reporting completion AI-assisted, team review pending.<br>
**Research question:** How accurately can classical regression models estimate engine RUL from sensor/operating data compared with a simple baseline?

## Status and V6 deliverables

Task 5's descriptive computation/reporting artifacts have been completed for team presentation review. This does not complete model development or establish predictive accuracy. The supplied Project Tasks V6.0 PDF, p. 2, dated 9 November 2026 (internal header V12.0), asks for descriptive statistics, trends/patterns, hypothesis assessment, grouping and business insights, delivered as findings, report, dashboard, insight summary and storytelling slide.

| Deliverable | Evidence |
|---|---|
| Exploratory findings and descriptive statistics | Executed `notebooks/03-descriptive-analysis.ipynb`; CSVs under `reports/results/task5/` |
| Descriptive analytics report and key insights | This report and `training_insights.json` |
| Visual summary/dashboard | [analysis.html](../analysis.html); six analysis charts plus two reproducible structural charts |
| Grouping/segmentation | Retrospective RUL stages and engine-level median comparisons; no clustering claimed |
| Hypothesis assessment | H1–H4 below, explicitly descriptive rather than formal significance tests |
| Data storytelling slide | Story slide in the milestone draft under `presentations/milestone/` |

## Source lineage and reproducibility

Kaggle-acquired N-CMAPSS DS01/DS02 HDF5 → audited Task 3 `reports/results/cycles.csv` → reconstructed Task 5 means/history table. These are stages of one data lineage, not independent sources pooled as new evidence. Reconstruction does not restore raw high-frequency measurements or within-flight variance. The full Task 4 dataset remains a separate explicit input option, `SOURCE='full_task4'`, verified against its local artifact manifest.

Actual input for this execution: **{p['description']}**. Path `{p['source_path']}`; SHA-256 `{p['sha256']}`. Task 3 cycle export SHA-256 `{p['cycle_export_sha256']}`. Task 4 split policy version `{p['task4_version']}`. The source table has {p['row_count']:,} rows, but analysis uses **{i['training_flights']} training flights only**; the fixed validation table is displayed separately. Test/quarantine rows are not used to develop these sensor findings.

Rebuild input with `python scripts/build_task5_inputs.py`, execute the notebook top to bottom, then run `python scripts/build_task5_report.py`. The notebook also regenerates both structural charts from `engines.csv`. Its appendix includes historical test structure for context, not feature selection. The tracked reconstruction was independently compared with the overlapping full Task 4 fields within numerical tolerance.

## Findings and hypothesis assessment

{insight_markdown(i)}

### H2 numerical detail

Previous-flight-difference correlations with RUL are {', '.join(f'{name}: {value:.3f}' for name,value in i['delta_rul_correlations'].items())}. These small pooled linear associations do not establish an incremental prediction benefit; nonlinear or engine-specific effects are not ruled out. We retain history as a candidate to evaluate on development engines rather than claim it improves forecasting.

### H3 operating-condition summaries

{mt(['Historical stage','Median altitude [m]','Median Mach','Median throttle [%]'],condition_rows)}

These are **flight-weighted** medians. They document different operating context across retrospective life stages; they are not an adjusted causal comparison and may reflect source/engine composition. Each stage contains a different set of flights from the same histories.

### Descriptive validation check

The four validation source histories have T48–RUL correlations from **{min(val_t):.3f} to {max(val_t):.3f}**, all negative. Their magnitudes differ, and Wf includes a positive association in DS02:18. This is a fixed exploratory check of the branch's three preselected channels. Validation had already been inspected during integration review; this is not independent preregistered confirmation. No model selection or test evaluation is performed here.

{mt(['Validation history','Sensor','Pearson r'],[[r['engine_id'],r['sensor'],f"{float(r['r_with_RUL']):.3f}"] for r in val])}

## Full summary statistics

{mt(['Variable','Count','Mean','Sample std','Minimum','Maximum'],summary_rows)}

Histories are **not** independent flight samples. Seven source histories map to six conservative unit-ID groups. No standard errors or significance tests treating 574 flights as independent subjects are reported.

## Visual evidence

'''+ '\n\n'.join(f'### {title}\n\n![{title}](../reports/figures/task5/{name}.svg)\n\n{caption}' for name,title,caption in figures)+'''

## Business story for the milestone

**Observation:** T48 is higher in the historical late-life group and negatively associated with RUL within each training source history.

**Interpretation:** temperature and operating context deserve investigation as model inputs. Core speed and fuel-flow relationships vary; a single universal threshold is not justified.

**Decision next:** compare a transparent constant baseline with simple regression models, using grouped development validation before final test. A training mean constant is natural for squared-error comparison; a median constant minimizes absolute error. Model scores and savings are still unknown.

**Practical limits:** overoptimistic RUL could defer maintenance, pessimistic RUL could encourage premature work. These are possible decision consequences, not measured costs. A real deployment would require independent validation and domain oversight beyond this semester project.

## Provenance updates and remaining caveats

The 2021 journal paper [Table 5](https://www.mdpi.com/2306-5729/6/1/5) confirms P2 as total pressure at the fan inlet, in psia (checked 11 November). The older local preprint omitted that row. Task 4 still excludes P2 to retain the selected 17-channel representation. Its current code/metadata refresh creates a new hash-identified version without changing the representation or 50-column matrix schema; earlier local versions remain intact.

The paper declares the dataset CC0 1.0. Current Kaggle metadata reports version 1 and the license label U.S. Government Works; see the inventory/source snapshot. The exact original local download-version match is still unproven. Real flight profiles drive simulated degradation and sensor responses. There is no evidence here of operational aviation suitability, real-engine fault prediction, economic savings, or RUL accuracy. Cross-subset independence remains uncertain; conservative grouping and unit-10 quarantine mitigate one known risk without proving all independence.

## Sources and review history

- Supplied Project Tasks V6.0, p. 2; milestone comments handout for presentation form.
- [Task 3 report](05-data-understanding.md), [Task 4 report](06-data-preparation.md), [data access](../data/README.md), and tracked CSV exports.
- Arias Chao et al. (2021), [Data 6(1), 5](https://doi.org/10.3390/data6010005); [Kaggle redistribution](https://www.kaggle.com/datasets/bishals098/nasa-cmapss-2-engine-degradation).
- Denzel's six-commit Task 5 branch was integrated on 11 November as a working draft. That review ran all eight original code cells in an isolated checkout. This subsequent milestone-readiness pass saves execution outputs, numerical interpretation, source options and regeneration steps in the repository.
- [AI assistance log](ai-use-log.md); human fact-checking and rehearsal pending.

This report/dashboard are generated by `scripts/build_task5_report.py` from notebook exports. The assessment is descriptive; no predictive model is fitted.
'''
(ROOT/'docs/07-task5-descriptive-analysis.md').write_text(report)
cards=[('T48 / RUL',f"{i['t48_r_min']:.3f} to {i['t48_r_max']:.3f}",'Pearson r across 7 training source histories; all negative.'),('LATE − EARLY T48',f"+{i['late_minus_early_T48_K_median']:.2f} K",'Median paired engine-stage contrast; retrospective RUL groups.'),('TRAINING SCOPE',str(i['training_flights']),'Flights; 7 source histories but 6 conservative engine-ID groups.')]
page='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>What the signals say — GR05</title><meta name="description" content="GR05 Task 5 descriptive findings: training sensor trends, context, hypotheses and limitations."><link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="assets/site.css"><link rel="stylesheet" href="assets/findings.css"></head><body><a class="skip-link" href="#main">Skip to content</a><header class="site-header wrap"><a class="wordmark" href="index.html">GR05<span class="wordmark-detail"> / DESCRIPTIVE ANALYSIS</span></a><nav aria-label="Main navigation"><a href="findings.html">Data</a><a href="preparation.html">Preparation</a><a href="docs/07-task5-descriptive-analysis.md">Report ↗</a></nav></header><main id="main"><section class="findings-hero wrap"><div><p class="eyebrow">TASK 05 / INITIAL DESCRIPTIVE ANALYSIS</p><h1>What the<br>signals <em>say.</em></h1><p class="hero-description">A temperature pattern.<br>A reason to investigate.</p><p class="hero-context">Verified descriptive findings from the training histories, before any RUL model is fitted. Correlation is not causality or forecast accuracy.</p><a class="button primary" href="notebooks/03-descriptive-analysis.ipynb" download>Get the executed notebook ↓</a></div><aside class="evidence-panel"><div class="evidence-label">TRAINING EVIDENCE <span>11 NOV 2026</span></div><span class="big-count">7 / 7</span><p>training histories show negative T48–RUL association</p><p class="evidence-footnote">Seven source histories are not seven proven independent engines. Equal IDs across subsets are linked conservatively. No model scores or savings claimed.</p></aside></section><section class="section wrap"><div class="section-label"><span>THE NUMBERS WE CAN DEFEND</span><span>TRAINING ONLY</span></div><div class="block-grid" style="grid-template-columns:repeat(auto-fit,minmax(230px,1fr))">'''
page+=''.join(f'<article><span>{html.escape(label)}</span><h3>{html.escape(value)}</h3><p>{html.escape(text)}</p></article>' for label,value,text in cards)
page+='</div></section><section class="quality-section"><div class="section wrap"><div class="section-heading"><h2>A signal worth testing.<br>Not a maintenance rule.</h2><p>T48 deserves a place in later model comparisons. Regime effects, repeated flights and a small fleet prevent stronger conclusions.</p></div><div class="next-grid"><article><h3>Observation</h3><p>T48 rises in retrospective late-life groups. Within-engine correlations with RUL are consistently negative.</p></article><article><h3>Interpretation</h3><p>Core-speed effects change sign across histories; context and heterogeneity matter. No universal threshold is established.</p></article><article><h3>Next decision</h3><p>Evaluate a constant baseline, linear regression and random forest on held-out development engines. Test stays out of model selection.</p></article></div></div></section><section class="section wrap">'
for n,title,caption in figures:
 page+=f'<figure class="research-figure"><img src="reports/figures/task5/{n}.svg" alt="{html.escape(title+": "+caption)}" loading="lazy"><figcaption><strong>{html.escape(title)}</strong> · {html.escape(caption)}</figcaption></figure>'
page+='<details class="data-details"><summary>Operating context and validation details</summary>'+ht(['Stage','Altitude median [m]','Mach median','Throttle median [%]'],condition_rows)+f'<p>Operating medians are flight-weighted. Validation T48 r: {min(val_t):.3f} to {max(val_t):.3f}; previously inspected, so not blinded confirmation. Test and quarantine are excluded from sensor hypotheses.</p></details>'
page+='''<div class="evidence-downloads"><div><p class="eyebrow">FOLLOW THE EVIDENCE</p><h3>Read. Re-run. Rehearse.</h3><p>Default input reconstructs means/history from tracked Task 3 cycle exports. It does not restore within-flight variance or reprocess raw HDF5.</p></div><div class="download-links"><a href="docs/07-task5-descriptive-analysis.md">Descriptive report ↗</a><a href="reports/results/task5/training_insights.json">Measured insight summary ↗</a><a href="reports/results/task5/analysis_provenance.json">Input provenance ↗</a><a href="presentations/milestone/GR05-milestone-draft.pptx" download>Milestone presentation draft ↓</a></div></div><details class="data-details"><summary>Source and review notes</summary><p>Scope: Project Tasks V6.0, page 2. Source: Kaggle-acquired N-CMAPSS DS01/DS02, through audited Task 3 means and Task 4 split assignments. Degradation and readings are simulated. No predictive model fitted.</p><p>Current source labels are recorded; original download-version matching and cross-subset independence remain open. P2 is now defined by journal Table 5; the frozen preparation version still excludes it. <a href="docs/ai-use-log.md">AI assistance disclosure</a>.</p></details></section></main><footer class="wrap site-footer"><a class="wordmark" href="index.html">GR05</a><p>Descriptive evidence · 11 November 2026</p><a href="index.html">Project overview ↗</a></footer></body></html>'''
(ROOT/'analysis.html').write_text(page)
print('Generated Task 5 report and analysis.html from executed evidence.')
