# Tasks 1–5 — Progress audit for 12 November 2026

**Audit date:** 11 November 2026<br>
**Progress/preparation:** Thursday **12 November**<br>
**Milestone presentation:** Thursday **19 November**, per lecturer overview slide 9<br>
**Final presentation:** Thursday **21 January 2027**, per the same overview.

## Readiness conclusion

The Task 1–5 **technical deliverables and explanation material are available for the progress session**. This is not a claim of 100% human understanding, supervisor sign-off, independent source authenticity, or deployment. The working roles and presentation allocation need team confirmation, and both students need to review/rehearse. Model training/evaluation is later work; missing RUL model scores are not a gap in Tasks 1–5.

Source of requirements: Supplied Project Tasks V6.0, dated 9 November, pp. 1–2 (internal header V12.0); lecturer Semester Overview and IA Overview slide 9.

| Requirement | Coverage | Evidence | Status / explicit limit |
| --- | --- | --- | --- |
| Introduction | Team/domain, glossary, source register and initial business understanding | [docs/glossary.md](../docs/glossary.md) | Available; source/independence limits recorded |
| Task 1 | Problem, scope, objectives, stakeholders/working roles, success criteria and roadmap | [docs/01-project-definition.md](../docs/01-project-definition.md) | Available; working role allocation needs team confirmation |
| Task 2 / business | Value proposition, stakeholder impact, KPIs and illustrative maintenance scenario | [docs/02-business-case.md](../docs/02-business-case.md) | Report prepared; no actual costs/savings or human approval fabricated |
| Task 2 / data | Sources, formats, access, exact local volume and constraints | [docs/03-data-inventory-access.md](../docs/03-data-inventory-access.md) | Current public metadata checked; original download-version match unproven |
| Task 3 | Executed exploration, full feature/scale descriptions, distributions and six quality dimensions | [notebooks/01-data-understanding.ipynb](../notebooks/01-data-understanding.ipynb) | Executed; source definition refreshed |
| Task 4 | Cleaning/transformation, feature engineering, integration and model-ready matrices | [notebooks/02-preprocessing.ipynb](../notebooks/02-preprocessing.ipynb) | Executed; local version/checksums verified by checker |
| Task 4 / versions | Raw/prepared comparison, source/code/config identity, fitted preprocessing and local artifacts | [reports/results/task4/manifest.json](../reports/results/task4/manifest.json) | Available locally; large files remain ignored |
| Task 5 / analysis | Descriptive statistics, patterns, hypothesis assessment and retrospective grouping | [notebooks/03-descriptive-analysis.ipynb](../notebooks/03-descriptive-analysis.ipynb) | Executed; descriptive assessment, not formal independent-subject tests |
| Task 5 / communication | Descriptive report, dashboard, key insights and storytelling slide | [docs/07-task5-descriptive-analysis.md](../docs/07-task5-descriptive-analysis.md) | Available; story is slide 33 of the milestone draft |
| Task 6 preparation | Draft slides, visual timeline, algorithms per proposed speaker and notes | [presentations/milestone/GR05-milestone-draft.pptx](../presentations/milestone/GR05-milestone-draft.pptx) | Preparation available for progress; milestone is 19 November |

## Actual reproducible results

- 14,159,058 raw readings, 1,542 completed-flight rows, 19 dataset-scoped histories. These are not proven independent engines across subsets.
- Current prepared version: **`task4-v1-f8ab427897d5`**; 574 train / 343 validation / 543 test / 82 quarantined flights.
- 45 numeric candidates → 50 finite matrix columns; a 20-column simpler selection is also provided.
- No NaN/inf in the Task 3 scan and no raw predictor values needed removal in the actual Task 4 run. The 57 engineered first-flight gaps are handled with training-only medians/indicators.
- T48–RUL r ranges from -0.540 to -0.299 across seven training histories; median paired late−early T48 contrast is 13.62 K. These are descriptive, not causal or prediction-performance claims.
- Current source metadata: Kaggle reports v1 / U.S. Government Works, while the paper says dataset CC0 1.0. Local source sizes/hashes are recorded; an original download-version match and upstream reference checksum remain unproven.

## Verification

Last automated check: 2026-11-11T23:59:37.247243+01:00; status passed. See [machine-readable results](../reports/results/progress_check.json).

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
