# GR05 — Predictive Maintenance

Estimating aircraft engine **Remaining Useful Life (RUL), in flight cycles**, using NASA N-CMAPSS data and Python machine learning.

**Course:** Industrial Analytics · Hochschule Furtwangen University · WS 2026/27\
**Domain:** Manufacturing / Maintenance\
**Team:** Selçuk Ata Aksoy and Denzel Gregory Pragassa\
**Lecturer:** Prof. Dr. Monika Frey-Luxemburger

## Current status

The lecturer approved the topic and dataset. Task 1 is documented; the Task 2 reports remain drafts. **Task 3: Data Understanding** now has an executed, explanatory Jupyter notebook, a report, and a separate findings page. Team review of the interpretations is pending.

DS01 and DS02 are available locally under `data/raw/`. The analysis scans every numeric field and reports structure, engine/flight counts, RUL label checks, summary statistics, and six data quality dimensions. Sampled distributions and outlier/duplicate diagnostics are labelled with their scope. No predictive model, MAE/RMSE result, or measured maintenance savings is claimed. Upstream version/redistribution terms and some variable semantics remain open.

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
| [docs/02-business-case.md](docs/02-business-case.md) | Task 2 Business Case Report — draft |
| [docs/03-data-inventory-access.md](docs/03-data-inventory-access.md) | Task 2 inventory, updated with local verification |
| [docs/04-dataset-evaluation.md](docs/04-dataset-evaluation.md) | Historical dataset proposal |
| [docs/05-data-understanding.md](docs/05-data-understanding.md) | Task 3 findings and six-dimension quality report |
| [docs/ai-use-log.md](docs/ai-use-log.md) | Concise AI assistance and review disclosure |
| [notebooks/01-data-understanding.ipynb](notebooks/01-data-understanding.ipynb) | Executed guided analysis and presentation questions |
| [src/data_understanding.py](src/data_understanding.py) | Reusable read-only chunked audit and feature definitions |
| [data/README.md](data/README.md) | Data placement, source follow-up, exact sizes and hashes |
| `reports/figures/`, `reports/results/` | Seven figures and small reproducible evidence exports |
| [scripts/build_task3_report.py](scripts/build_task3_report.py) | Rebuilds the Task 3 report and findings HTML from exports |
| `tests/` | Chunk-boundary/numerical and semantic-scale checks |
| [index.html](index.html), [findings.html](findings.html), `assets/` | Overview and separate research findings, ready for GitHub Pages |

Document numbers indicate reading order, not task numbers. The current structure supports the original plan:

```text
GR05-Predictive-Maintenance/
├── README.md
├── requirements.txt
├── requirements-lock.txt
├── index.html
├── findings.html
├── assets/
├── docs/
│   ├── 01-project-definition.md
│   ├── 02-business-case.md
│   ├── 03-data-inventory-access.md
│   ├── 04-dataset-evaluation.md
│   ├── 05-data-understanding.md
│   ├── 06-methodology.md            # Planned
│   ├── decisions.md                 # Planned
│   ├── references.md                # Planned
│   └── ai-use-log.md
├── data/
│   ├── README.md
│   ├── raw/                         # Local only; ignored by Git
│   └── processed/                   # Planned; local only
├── notebooks/
│   ├── 01-data-understanding.ipynb
│   ├── 02-preprocessing.ipynb       # Planned
│   └── 03-modeling.ipynb            # Planned
├── src/
│   ├── data_understanding.py
│   ├── preprocessing.py            # Planned
│   ├── features.py                   # Planned
│   ├── train.py                      # Planned
│   └── evaluate.py                   # Planned
├── scripts/
├── tests/
├── reports/
│   ├── figures/
│   └── results/
└── presentations/                   # Planned
    ├── milestone/
    └── final/
```

Create planned files when actual work needs them. Course PDFs/slides and downloaded example material remain local source references; avoid accidentally publishing course material or large downloads.

## Project website

The homepage keeps the project overview concise and links to [findings.html](findings.html) for the analysis, charts, quality checks, and downloads. Both pages work as static HTML without a framework. Optional JavaScript handles decorative turbine motion and engine-table filters; reduced-motion preferences are respected.

Open `index.html` locally. For GitHub Pages, after reviewing and pushing select **Settings → Pages → Deploy from a branch → main → /(root)**. See [GitHub's publishing-source instructions](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site). The expected address after deployment is `https://cukowski.github.io/GR05-Predictive-Maintenance/`; hosting has not been configured or verified here.

## Next steps and milestones

1. Review the Task 2 drafts, Task 3 notebook, feature scales, and quality limitations together; practise explaining the findings.
2. Confirm source version/terms, P2 and stall-margin definitions, and whether shared histories across subsets limit independence.
3. Decide the prediction point and DS01 preparation/validation protocol before implementing preprocessing and a baseline.

| Date | Milestone |
|---|---|
| 22 October 2026 | Local DS01/DS02 descriptive feasibility completed; team scope review pending |
| 19 November 2026 | Business case, dataset, and initial descriptive analysis presentation |
| 21 January 2027 | Final modeling, evaluation, business discussion, and presentation |

Planning: [Google Sheet roadmap](https://docs.google.com/spreadsheets/d/17AP7LQW_lRiLAHCcqhy8QmZdgw_bXJETPD5y3_tOEiU/edit).

## Working practices and AI disclosure

Keep changes and commits meaningful. Do not commit raw datasets, credentials, environments, or notebook checkpoints. Verify claims, distinguish observation from interpretation, and preserve reproducibility. Follow [HFU AI guidance](https://www.hs-furtwangen.de/en/hfu-insights/studying-at-hfu/academic-work-including-with-ai-tools), agree the declaration format with the lecturer, and record substantive assistance and review in the [AI use log](docs/ai-use-log.md).
