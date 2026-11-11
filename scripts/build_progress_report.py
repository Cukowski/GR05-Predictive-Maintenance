"""Build a V6 Task 1–5 progress audit and concise website entry point."""
from pathlib import Path
import json,html
ROOT=Path(__file__).resolve().parents[1]
meta=json.loads((ROOT/'reports/results/task4/manifest.json').read_text())
insight=json.loads((ROOT/'reports/results/task5/training_insights.json').read_text())
checkpath=ROOT/'reports/results/progress_check.json'
check=json.loads(checkpath.read_text()) if checkpath.exists() else None
rows=[
 ('Introduction','Team/domain, glossary, source register and initial business understanding','docs/glossary.md','Available; source/independence limits recorded'),
 ('Task 1','Problem, scope, objectives, stakeholders/working roles, success criteria and roadmap','docs/01-project-definition.md','Available; working role allocation needs team confirmation'),
 ('Task 2 / business','Value proposition, stakeholder impact, KPIs and illustrative maintenance scenario','docs/02-business-case.md','Report prepared; no actual costs/savings or human approval fabricated'),
 ('Task 2 / data','Sources, formats, access, exact local volume and constraints','docs/03-data-inventory-access.md','Current public metadata checked; original download-version match unproven'),
 ('Task 3','Executed exploration, full feature/scale descriptions, distributions and six quality dimensions','notebooks/01-data-understanding.ipynb','Executed; source definition refreshed'),
 ('Task 4','Cleaning/transformation, feature engineering, integration and model-ready matrices','notebooks/02-preprocessing.ipynb','Executed; local version/checksums verified by checker'),
 ('Task 4 / versions','Raw/prepared comparison, source/code/config identity, fitted preprocessing and local artifacts','reports/results/task4/manifest.json','Available locally; large files remain ignored'),
 ('Task 5 / analysis','Descriptive statistics, patterns, hypothesis assessment and retrospective grouping','notebooks/03-descriptive-analysis.ipynb','Executed; descriptive assessment, not formal independent-subject tests'),
 ('Task 5 / communication','Descriptive report, dashboard, key insights and storytelling slide','docs/07-task5-descriptive-analysis.md','Available; story is slide 33 of the milestone draft'),
 ('Task 6 preparation','Draft slides, visual timeline, algorithms per proposed speaker and notes','presentations/milestone/GR05-milestone-draft.pptx','Preparation available for progress; milestone is 19 November'),
]

def mt(headers,rows):return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |',*['| '+' | '.join(map(str,r))+' |' for r in rows]])
source='Supplied Project Tasks V6.0, dated 9 November, pp. 1–2 (internal header V12.0); lecturer Semester Overview and IA Overview slide 9.'
verification=f"Last automated check: {check['checked_at']}; status {check['status']}. See [machine-readable results](../reports/results/progress_check.json)." if check else 'Run `python scripts/check_project.py --raw-hashes --write-report` to record the current automated verification.'
report=f'''# Tasks 1–5 — Progress audit for 12 November 2026

**Audit date:** 11 November 2026<br>
**Progress/preparation:** Thursday **12 November**<br>
**Milestone presentation:** Thursday **19 November**, per lecturer overview slide 9<br>
**Final presentation:** Thursday **21 January 2027**, per the same overview.

## Readiness conclusion

The Task 1–5 **technical deliverables and explanation material are available for the progress session**. This is not a claim of 100% human understanding, supervisor sign-off, independent source authenticity, or deployment. The working roles and presentation allocation need team confirmation, and both students need to review/rehearse. Model training/evaluation is later work; missing RUL model scores are not a gap in Tasks 1–5.

Source of requirements: {source}

{mt(['Requirement','Coverage','Evidence','Status / explicit limit'],[[a,b,f'[{c}](../{c})',d] for a,b,c,d in rows])}

## Actual reproducible results

- 14,159,058 raw readings, 1,542 completed-flight rows, 19 dataset-scoped histories. These are not proven independent engines across subsets.
- Current prepared version: **`{meta['version_id']}`**; 574 train / 343 validation / 543 test / 82 quarantined flights.
- 45 numeric candidates → 50 finite matrix columns; a 20-column simpler selection is also provided.
- No NaN/inf in the Task 3 scan and no raw predictor values needed removal in the actual Task 4 run. The 57 engineered first-flight gaps are handled with training-only medians/indicators.
- T48–RUL r ranges from {insight['t48_r_min']:.3f} to {insight['t48_r_max']:.3f} across seven training histories; median paired late−early T48 contrast is {insight['late_minus_early_T48_K_median']:.2f} K. These are descriptive, not causal or prediction-performance claims.
- Current source metadata: Kaggle reports v1 / U.S. Government Works, while the paper says dataset CC0 1.0. Local source sizes/hashes are recorded; an original download-version match and upstream reference checksum remain unproven.

## Verification

{verification}

The checker validates notebook execution/error state, CSV row/count reconciliation, current code/config fingerprints, source hashes, split separation, saved artifact hashes, matrix/target/metadata alignment, training-only fitted parameters, report/website links and presentation dates. With `--raw-hashes`, both complete raw files are SHA-256 checked. `--skip-local-data` exists for fresh clones and explicitly skips the ignored files; it is not an equivalent full local validation.

## Rebuild and check everything

```bash
source .venv/bin/activate
python -m pip install -r requirements-presentation.txt
python scripts/run_notebooks.py --tasks 3 4 5
python scripts/build_reports.py --presentation
python -m unittest discover -s tests -v
python scripts/check_project.py --raw-hashes --write-report
# Refresh the progress page to include the recorded check result:
python scripts/build_progress_report.py
```

The raw files must already be present as described in [data/README.md](../data/README.md). The full notebook run processes approximately 5 GB and requires a local Jupyter kernel. Use `python scripts/prepare_data.py` for preparation alone. Report builders read exported evidence, rather than inventing results or requiring a new raw download.

## What to show on 12 November (five-minute progress route)

1. Open [progress.html](../progress.html), then give the one-sentence research question.
2. Explain reading → flight → history, RUL and the end-of-flight prediction point.
3. Show one raw/processed comparison and the 574/343/543/82 split. Explain why related histories cannot leak across splits.
4. Open [the Task 5 dashboard](../analysis.html): show T48 associations and the retrospective stage comparison; explain the operating-context/independence limits.
5. Show the [19 November milestone draft](../presentations/milestone/GR05-milestone-draft.pptx), proposed algorithms and next work.

Raw and prepared files are both available locally; they are not website downloads. Do not rerun raw scans live. An [offline PDF](../presentations/milestone/GR05-milestone-draft.pdf) and [speaker/readiness notes](../presentations/milestone/readiness-guide.md) support a software-independent fallback.

## Remaining items that cannot be completed by assertion

- **Team confirmation:** working roles, individual contributions, proposed algorithm presenters, allowed presentation duration and human review of the final narrative.
- **Understanding/rehearsal:** both students can explain their code/charts and AI assistance; a script cannot certify that.
- **Source limitations:** original download receipt/version match, upstream reference checksum and cross-subset physical independence are not established.
- **Scope:** no RUL predictor trained, no MAE/RMSE measured, no savings or operational aviation validity demonstrated.
- **Hosting:** current website source is regenerated/checked locally. External GitHub Pages publication is separate and has not been performed by this audit.

These are recorded review/actions or honest study limits, not hidden unfinished computation. No approval or empirical result is fabricated to make a checklist look complete.
'''
(ROOT/'docs/08-progress-audit.md').write_text(report)
status='Automated checks recorded' if check else 'Verification command available'
page='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Progress, clearly — GR05</title><meta name="description" content="GR05 Tasks 1–5 progress, reproducible evidence and milestones: 12 November preparation, 19 November presentation."><link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="assets/site.css"><link rel="stylesheet" href="assets/findings.css"></head><body><a class="skip-link" href="#main">Skip to content</a><header class="site-header wrap"><a class="wordmark" href="index.html">GR05<span class="wordmark-detail"> / PROJECT PROGRESS</span></a><nav aria-label="Main navigation"><a href="analysis.html">Analysis</a><a href="preparation.html">Preparation</a><a href="docs/08-progress-audit.md">Audit ↗</a></nav></header><main id="main"><section class="findings-hero wrap"><div><p class="eyebrow">TASKS 01–05 / PROGRESS SESSION</p><h1>Evidence.<br>Ready to <em>explain.</em></h1><p class="hero-description">12 November: progress.<br>19 November: milestone.</p><p class="hero-context">Definition, business case, data understanding, preparation and descriptive results. A clear record of what exists and what we still need to review together.</p><a class="button primary" href="docs/08-progress-audit.md">Read the task audit ↗</a></div><aside class="evidence-panel"><div class="evidence-label">PROGRESS SNAPSHOT <span>11 NOV 2026</span></div><span class="big-count">1–5</span><p>task deliverables available for review</p><div class="evidence-facts"><div><strong>3</strong><span>executed notebooks</span></div><div><strong>574</strong><span>training flights</span></div><div><strong>19 Nov</strong><span>milestone</span></div></div><p class="evidence-footnote">Technical checks do not certify team understanding or human approval. No predictive model scores or savings are claimed.</p></aside></section><nav class="chapter-nav" aria-label="Evidence sections"><div class="wrap"><a href="findings.html">Data understanding</a><a href="preparation.html">Preparation</a><a href="analysis.html">Descriptive findings</a><a href="presentations/milestone/readiness-guide.md">Rehearsal guide</a></div></nav><section class="section wrap"><div class="section-label"><span>THE REQUIREMENTS AND THE EVIDENCE</span><span>V6 · PAGES 1–2</span></div><div class="quality-grid">'''
for a,b,c,d in rows:
 page+=f'<article><span class="quality-index">{html.escape(a)}</span><h3>{html.escape(b.split(",")[0])}</h3><p>{html.escape(d)}</p><a class="text-link" href="{html.escape(c)}">Open evidence ↗</a></article>'
page+='</div></section><section class="quality-section"><div class="section wrap"><div class="section-heading"><h2>Not just files.<br>Checks you can repeat.</h2><p>'+status+'. Notebook execution, exact input identity, finite matrices, group separation and evidence links are checked locally.</p></div><p><code>python scripts/check_project.py --raw-hashes --write-report</code></p><p class="quality-footnote">Current public source labels are recorded. Original download-version matching and cross-subset independence remain limited. The team still needs to confirm roles and rehearse.</p></div></section><section class="section wrap"><div class="evidence-downloads"><div><p class="eyebrow">FOR THE MILESTONE ON 19 NOVEMBER</p><h3>Explain what we know.</h3><p>Models are the next stage. The draft includes algorithm overviews, verified descriptive evidence, speaker notes and sources.</p></div><div class="download-links"><a href="presentations/milestone/GR05-milestone-draft.pptx" download>Editable milestone draft ↓</a><a href="presentations/milestone/GR05-milestone-draft.pdf">Offline full PDF ↗</a><a href="presentations/milestone/readiness-guide.md">Rehearsal and Q&amp;A guide ↗</a><a href="docs/glossary.md">Plain-language glossary ↗</a><a href="docs/decisions.md">Decisions and limitations ↗</a></div></div></section></main><footer class="wrap site-footer"><a class="wordmark" href="index.html">GR05</a><p>Progress evidence · 11 November 2026</p><a href="index.html">Project overview ↗</a></footer></body></html>'
(ROOT/'progress.html').write_text(page)
print('Generated docs/08-progress-audit.md and progress.html')
