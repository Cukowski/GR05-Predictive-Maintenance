# GR05 — Predictive Maintenance

Estimating aircraft engine **Remaining Useful Life (RUL), in flight cycles**, using NASA N-CMAPSS data and Python machine learning.

**Course:** Industrial Analytics · Hochschule Furtwangen University · WS 2026/27\
**Domain:** Manufacturing / Maintenance\
**Team:** Selçuk Ata Aksoy and Denzel Gregory Pragassa\
**Lecturer:** Prof. Dr. Monika Frey-Luxemburger

## Current status

The lecturer approved the topic and dataset. Task 1 and both Task 2 reports now have explicit current scope, working roles, success criteria and source/constraint documentation. **Tasks 3–5** now have executed explanatory notebooks, reproducible evidence, and separate findings/preparation/analysis pages. A V6 milestone draft deck and readiness guide are available for review. Task 4 has built versioned local flight datasets and fitted preprocessing. Tasks 1–5 technical artifacts are available for progress review; team role confirmation, human understanding and rehearsal remain distinct actions.

DS01 and DS02 are available locally under `data/raw/`. The analysis scans every numeric field and reports structure, engine/flight counts, RUL label checks, summary statistics, and six data quality dimensions. Sampled distributions and outlier/duplicate diagnostics are labelled with their scope. Task 4 prepares 1,542 flight rows: 574 training, 343 validation, 543 test, and 82 quarantined for a possible cross-subset test-history link. It fits preprocessing only, with 50 candidate model columns and a simpler 20-column baseline selection. No RUL prediction model, MAE/RMSE result, or measured maintenance savings is claimed. Current source version/license labels are recorded. The original local download-version match and cross-subset independence remain unproven.

## Presentation readiness — V6

Start with [presentations/milestone/readiness-guide.md](presentations/milestone/readiness-guide.md). It maps the V6 task sheet to evidence and lists the confirmations/rehearsal still needed. Draft artifacts:

- [Editable 40-slide PowerPoint with notes](presentations/milestone/GR05-milestone-draft.pptx)
- [Offline full PDF](presentations/milestone/GR05-milestone-draft.pdf) and [22-slide short route](presentations/milestone/GR05-milestone-short-route.pdf)
- [Speaker notes and presenter proposals](presentations/milestone/speaker-notes.md)
- [Task 5 dashboard](analysis.html) and [completed descriptive report](docs/07-task5-descriptive-analysis.md)

**12 November is the progress/Task 6 preparation session. The milestone presentation is Thursday 19 November 2026**, explicitly dated in lecturer overview slide 9. Confirm class time and allowed speaking duration separately. Presenter assignments and next-stage dates are proposals, and both students still need to review/rehearse the deck. Models are explained as planned work; there are no claimed model scores.

## Start with the notebook

Use Python 3.12 (the executed environment) from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m jupyterlab
```

On Windows, activate with `.venv\Scripts\Activate.ps1` in PowerShell. Select the project `.venv` Python kernel/interpreter in Jupyter or VS Code. Open [notebooks/01-data-understanding.ipynb](notebooks/01-data-understanding.ipynb) and run all cells from top to bottom. File placement/download guidance is in [data/README.md](data/README.md).

The notebook explains HDF5, every variable's meaning/unit/scale, the lecturer-style feature description table, engine vs flight vs reading, RUL, operating regimes, sensors, distributions, correlations, and quality checks. It includes presentation questions to help both team members explain the results. It reads approximately 5 GB in chunks plus a checksum pass; runtime depends on hardware. Raw files are opened read-only.

After executing it, regenerate the Task 3 report and findings page:

```bash
python scripts/build_task3_report.py
```

The figures and compact CSV/JSON evidence are exported by the notebook. The page/report generator reads those exports, so the human-facing numbers remain traceable. Primary package versions are pinned in `requirements.txt`; `requirements-lock.txt` records the full installed environment. To reproduce that complete dependency set, install the latter instead.

## Task 4 — prepare the modeling dataset

Open [notebooks/02-preprocessing.ipynb](notebooks/02-preprocessing.ipynb) and run it top to bottom. It explains snapshots vs flights vs engines, the relevant inputs, physical units, missing values, engineering, engine-group splits, and how X (inputs) differs from y (the answer). Each prepared row is one **completed flight**, with a prediction made at its end. Future flights, final lifetime, IDs and hidden health state are excluded from predictors.

Command-line workflow:

```bash
python scripts/prepare_data.py
# Run notebooks/02-preprocessing.ipynb for the guided examples and charts.
python scripts/build_task4_report.py
python -m unittest discover -s tests -v
```

The actual current version is identified by [reports/results/task4/manifest.json](reports/results/task4/manifest.json). Its directory under `data/processed/` contains physical-unit features, finite `X_train.csv` / `X_validation.csv` / `X_test.csv`, separate RUL labels and row identities, quarantine rows, and `preprocessor.joblib`. Raw and processed data remain local and ignored by Git. Read the [Task 4 report](docs/06-data-preparation.md) or [preparation page](preparation.html) for the complete results and feature catalog.

Numeric preparation uses training-only median imputation with missingness indicators and standardization. The source collection DS01/DS02 is one-hot encoded. No raw predictor repair was needed in these files; 57 engineered first-flight gaps are handled explicitly. P2 remains excluded to keep the selected 17-channel representation stable; its definition/unit is now confirmed from journal Table 5. Both datasets are integrated, but equal unit IDs are linked conservatively across subsets: DS02 development unit 10 is quarantined because unit 10 is test in DS01. Validation IDs 5, 6, and 18 are fixed in configuration, independently of model performance.

The version fingerprint includes raw hashes, code/configuration, Python and relevant package versions; outputs are verified before reuse. Changed inputs produce a new version rather than overwriting an old one. Preprocessing must be refitted within each training fold if using grouped cross-validation later.

## Task 5 — descriptive findings

Execute [notebooks/03-descriptive-analysis.ipynb](notebooks/03-descriptive-analysis.ipynb). It builds its default input from tracked Task 3 aggregates, preserving Task 4 split assignments. It cannot reconstruct within-flight variances; its source manifest labels that limitation. An explicit `SOURCE='full_task4'` option reads the hash-verified local version instead.

```bash
python scripts/build_task5_inputs.py
# Run notebooks/03-descriptive-analysis.ipynb top to bottom.
python scripts/build_task5_report.py
```

The executed training findings show T48–RUL Pearson r between −0.540 and −0.299 across seven source histories (six conservative groups). Paired late-minus-early engine-median T48 differs by +13.62 K median. These are exploratory associations from simulated data; operating-regime effects and dependence remain. No causal or prediction-performance claim follows. Validation was previously seen during branch review, so the fixed check is not blinded confirmation.

The 2021 paper's Table 5 now confirms P2 as total pressure at the fan inlet, psia (checked 11 November). Its exclusion remains part of the frozen Task 4 version; the source-definition/code refresh creates a new version identity without changing the selected numerical feature representation. Previous local version directories remain intact.

To regenerate the presentation, install optional dependencies with `python -m pip install -r requirements-presentation.txt`, then run `python scripts/build_milestone_presentation.py`. The analysis environment itself does not require PowerPoint tooling.

## Problem and approach

**How accurately can machine-learning regression models estimate the remaining useful life of simulated aircraft engines using N-CMAPSS sensor and operational data, compared with a simple baseline?**

Follow **CRISP-DM**: business understanding → data understanding → preparation → modeling → evaluation → business implications. Start with a manageable DS01 pilot, candidate operating/sensor channels, and simple baselines before comparing regression models such as linear regression or random forest. Define the prediction point, separate engines across training/validation/test, and fit preprocessing only on training engines. Report MAE/RMSE in flight cycles and per-engine errors later.

Operating conditions come from real flight profiles; engine degradation and sensor responses are **simulated**. This is an offline academic project. Real-world aviation suitability and demonstrated financial benefits are outside scope. Dataset-scoped engine histories across subsets must not automatically be treated as independent engines.

## Dataset and sources

- [Arias Chao et al. (2021), Data 6(1), 5](https://doi.org/10.3390/data6010005): wider N-CMAPSS collection.
- [NASA Prognostics Center of Excellence](https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/): original provider, “Turbofan Engine Degradation Simulation Data Set 2.”
- [Kaggle redistribution](https://www.kaggle.com/datasets/bishals098/nasa-cmapss-2-engine-degradation): source reported by the team for the local files. The supplied accompanying preprint is dated April 2020 and focuses on DS02.
- Local task sheet, lecturer slides, Dataset Scales PPTX, and feature-table example notebook guide Task 3; source references and their limitations are recorded in the notebook/report.

## Repository guide

| Path | Purpose / status |
|---|---|
| [docs/01-project-definition.md](docs/01-project-definition.md) | Research question, objectives, and scope |
| [docs/02-business-case.md](docs/02-business-case.md) | Current business case, stakeholders, KPIs and illustrative value scenario |
| [docs/03-data-inventory-access.md](docs/03-data-inventory-access.md) | Sources, formats, access, exact local volumes and provenance limits |
| [docs/04-dataset-evaluation.md](docs/04-dataset-evaluation.md) | Historical dataset proposal |
| [docs/05-data-understanding.md](docs/05-data-understanding.md) | Task 3 findings and six-dimension quality report |
| [docs/07-task5-descriptive-analysis.md](docs/07-task5-descriptive-analysis.md) | Task 5 numerical findings, hypothesis assessment, caveats and sources |
| [notebooks/03-descriptive-analysis.ipynb](notebooks/03-descriptive-analysis.ipynb) | Executed descriptive analysis with source options and training-only hypotheses |
| [analysis.html](analysis.html), `presentations/milestone/` | Descriptive dashboard and milestone slides/notes/readiness guide |
| [docs/06-data-preparation.md](docs/06-data-preparation.md) | Task 4 report, feature engineering, integration and version comparison |
| [notebooks/02-preprocessing.ipynb](notebooks/02-preprocessing.ipynb) | Executed Task 4 tutorial, transformations and checks |
| [src/preprocessing.py](src/preprocessing.py), [config/preprocessing.json](config/preprocessing.json) | Flight preparation and explicit split/feature policies |
| [scripts/prepare_data.py](scripts/prepare_data.py), [scripts/build_task4_report.py](scripts/build_task4_report.py) | Create/verify local data versions and rebuild Task 4 report/page |
| [docs/08-progress-audit.md](docs/08-progress-audit.md), [progress.html](progress.html) | V6 Task 1–5 evidence audit and progress-session route |
| [docs/glossary.md](docs/glossary.md), [docs/decisions.md](docs/decisions.md), [docs/references.md](docs/references.md), [docs/literature-notes.md](docs/literature-notes.md) | Plain-language terms, explicit decisions and source register |
| [scripts/run_notebooks.py](scripts/run_notebooks.py), [scripts/build_reports.py](scripts/build_reports.py), [scripts/check_project.py](scripts/check_project.py) | End-to-end execution, report rebuilding and repeatable validation |
| [docs/ai-use-log.md](docs/ai-use-log.md) | Concise AI assistance and review disclosure |
| [notebooks/01-data-understanding.ipynb](notebooks/01-data-understanding.ipynb) | Executed guided analysis and presentation questions |
| [src/data_understanding.py](src/data_understanding.py) | Reusable read-only chunked audit and feature definitions |
| [data/README.md](data/README.md) | Data placement, source follow-up, exact sizes and hashes |
| `reports/figures/`, `reports/results/` | Task 3–5 figures and small reproducible evidence exports |
| [scripts/build_task3_report.py](scripts/build_task3_report.py) | Rebuilds the Task 3 report and findings HTML from exports |
| `tests/` | Chunk-boundary/numerical, causal-feature, split-isolation, scaling and semantic-scale checks |
| [index.html](index.html), [findings.html](findings.html), [preparation.html](preparation.html), `assets/` | Overview, Task 3 findings and Task 4 preparation, ready for GitHub Pages |

Document numbers indicate reading order, not task numbers. The current structure supports the original plan:

```text
GR05-Predictive-Maintenance/
├── README.md
├── requirements.txt
├── requirements-lock.txt
├── index.html
├── findings.html
├── preparation.html
├── analysis.html
├── progress.html
├── config/
├── assets/
├── docs/
│   ├── 01-project-definition.md
│   ├── 02-business-case.md
│   ├── 03-data-inventory-access.md
│   ├── 04-dataset-evaluation.md
│   ├── 05-data-understanding.md
│   ├── 06-data-preparation.md
│   ├── 07-task5-descriptive-analysis.md
│   ├── 08-progress-audit.md
│   ├── glossary.md
│   ├── literature-notes.md
│   ├── decisions.md
│   ├── references.md
│   └── ai-use-log.md
├── data/
│   ├── README.md
│   ├── raw/                         # Local only; ignored by Git
│   └── processed/                   # Versioned prepared data; local only
├── notebooks/
│   ├── 01-data-understanding.ipynb
│   ├── 02-preprocessing.ipynb
│   ├── 03-descriptive-analysis.ipynb
│   └── 04-modeling.ipynb            # Planned
├── src/
│   ├── data_understanding.py
│   ├── preprocessing.py
│   ├── features.py                   # Planned
│   ├── train.py                      # Planned
│   └── evaluate.py                   # Planned
├── scripts/
├── tests/
├── reports/
│   ├── figures/
│   └── results/
└── presentations/
    ├── milestone/
    └── final/                       # Planned
```

Create planned files when actual work needs them. Course PDFs/slides and downloaded example material remain local source references; avoid accidentally publishing course material or large downloads.

## Check the complete progress package

```bash
python scripts/run_notebooks.py --tasks 3 4 5
python scripts/build_reports.py --presentation
python -m unittest discover -s tests -v
python scripts/check_project.py --raw-hashes --write-report
python scripts/build_progress_report.py
```

Install `requirements-presentation.txt` for deck regeneration; omit `--presentation` when only rebuilding reports/pages. The checker validates execution state, source/code/artifact hashes, count reconciliation, matrix alignment, split isolation, training-only preparation, website/document links and corrected dates. The resulting [progress check JSON](reports/results/progress_check.json) records what was checked. A fresh clone without ignored data can use `--skip-local-data`, which explicitly does not verify local artifacts.

## Project website

The homepage keeps the project overview concise and links to [findings.html](findings.html) for the analysis, charts, quality checks, and downloads. The separate [preparation.html](preparation.html) explains Task 4 without crowding the homepage. The [analysis dashboard](analysis.html) adds Task 5 results, and [progress.html](progress.html) maps Tasks 1–5 to their current evidence. All pages work as static HTML without a framework. Optional JavaScript handles decorative turbine motion and engine-table filters; reduced-motion preferences are respected.

Open `index.html` locally. For GitHub Pages, after reviewing and pushing select **Settings → Pages → Deploy from a branch → main → /(root)**. See [GitHub's publishing-source instructions](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site). The expected address after deployment is `https://cukowski.github.io/GR05-Predictive-Maintenance/`; hosting has not been configured or verified here.

## Next steps and milestones

1. Use [the current progress audit](docs/08-progress-audit.md) for 12 November; review the reports and practise explaining rows, labels, features and splits.
2. Confirm working roles, allowed speaking duration and rehearsal for 19 November; retain the documented source/independence limits.
3. Train a transparent baseline on the smaller feature selection, then compare a simple regressor using development-engine validation before final test.

| Date | Milestone |
|---|---|
| 22 October 2026 | Local DS01/DS02 descriptive feasibility completed |
| 29 October 2026 | Task 4 pipeline executed; prepared local version and model matrices available, team review pending |
| 12 November 2026 | Progress / Task 6 preparation session |
| 19 November 2026 | Milestone presentation, per lecturer overview slide 9 |
| 21 January 2027 | Final modeling, evaluation, business discussion, and presentation |

Planning: [Google Sheet roadmap](https://docs.google.com/spreadsheets/d/17AP7LQW_lRiLAHCcqhy8QmZdgw_bXJETPD5y3_tOEiU/edit).

## Working practices and AI disclosure

Keep changes and commits meaningful. Do not commit raw datasets, credentials, environments, or notebook checkpoints. Verify claims, distinguish observation from interpretation, and preserve reproducibility. Follow [HFU AI guidance](https://www.hs-furtwangen.de/en/hfu-insights/studying-at-hfu/academic-work-including-with-ai-tools), agree the declaration format with the lecturer, and record substantive assistance and review in the [AI use log](docs/ai-use-log.md).
