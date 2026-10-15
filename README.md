# GR05 — Predictive Maintenance

Estimating aircraft engine **Remaining Useful Life (RUL), in flight cycles**, using NASA N-CMAPSS data and Python machine learning.

**Course:** Industrial Analytics · Hochschule Furtwangen University · WS 2026/27\
**Domain:** Manufacturing / Maintenance\
**Team:** Selçuk Ata Aksoy and Denzel Gregory Pragassa\
**Lecturer:** Prof. Dr. Monika Frey-Luxemburger

## Current status

The lecturer has approved the topic and dataset. Task 1 (Project Definition) is documented; Task 2 (Business Case and Dataset) is in progress. The Business Case Report and Data Inventory & Access Report are drafts awaiting team review.

This repository currently contains project documentation. Dataset files, Python dependencies, notebooks, EDA, and model experiments have not yet been added. The Kaggle package structure, access conditions, and resource requirements remain to be verified. No experimental results or maintenance savings have been demonstrated.

## Problem and research question

Unexpected equipment degradation can interrupt operations and increase maintenance costs. RUL estimates may help maintenance planners balance early intervention against continued operation.

**How accurately can machine-learning regression models estimate the remaining useful life of simulated aircraft engines using N-CMAPSS sensor and operational data, compared with a simple baseline?**

The project is an offline academic demonstration. Operational aviation use and measured financial benefits are outside its scope.

## Dataset

- **Scientific source:** Arias Chao et al. (2021), [Aircraft Engine Run-to-Failure Dataset under Real Flight Conditions for Prognostics and Diagnostics](https://doi.org/10.3390/data6010005).
- **Original provider:** [NASA Prognostics Center of Excellence](https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/), “Turbofan Engine Degradation Simulation Data Set 2.”
- **Planned download source:** [Kaggle N-CMAPSS redistribution](https://www.kaggle.com/datasets/bishals098/nasa-cmapss-2-engine-degradation).
- **Initial scope:** a DS01 pilot, subject to checking the actual files, licensing, and local memory/storage requirements.

Operating conditions come from real flight profiles; engine degradation and sensor responses are **simulated**, rather than observations of real engine failures. Paper-described properties must be distinguished from properties verified in the downloaded files. See the [Data Inventory & Access Report](docs/03-data-inventory-access.md).

## Approach

Follow **CRISP-DM**: business understanding → data understanding → preparation → modeling → evaluation → business implications.

1. Verify the dataset source, schema, engine IDs, flight cycles, RUL labels, and provided development/test partitions.
2. Explore a small DS01 sample before loading larger arrays; document missing values, operating conditions, and sensor/RUL trajectories by engine.
3. Define when predictions are made and separate engines across training, validation, and testing. Respect provided partitions and fit preprocessing on training data only.
4. Establish a simple baseline, then compare manageable regression models such as linear regression and random forest. Exclude future information, target labels, and unjustified simulator-only features from predictors.
5. Report **MAE and RMSE in flight cycles**, including per-engine errors and RUL overestimation. Discuss maintenance implications using clearly labeled hypothetical scenarios.

**Planned tools:** Python, pandas, NumPy, Matplotlib, scikit-learn, Jupyter, and an HDF5 reader such as h5py if the downloaded format requires it. Record dependencies and setup instructions when the first inspection workflow is implemented.

## Repository guide

| Path | Purpose / status |
|---|---|
| [docs/01-project-definition.md](docs/01-project-definition.md) | Task 1: research question, objectives, and scope |
| [docs/02-business-case.md](docs/02-business-case.md) | Task 2: Business Case Report — draft |
| [docs/03-data-inventory-access.md](docs/03-data-inventory-access.md) | Task 2: Data Inventory & Access Report — draft; file verification pending |
| [docs/04-dataset-evaluation.md](docs/04-dataset-evaluation.md) | Original dataset proposal, retained as historical context |
| [docs/ai-use-log.md](docs/ai-use-log.md) | AI assistance, verification, and human review record |
| [.gitignore](.gitignore) | Excludes local data, secrets, environments, and generated caches |
| [index.html](index.html), `assets/` | Static project landing page with a decorative turbine and space for future findings |

Document numbers indicate reading order, not course task numbers. Add `notebooks/` for exploratory work and `src/` for reusable code when implementation starts. Keep local raw and processed datasets under `data/raw/` and `data/processed/`; both paths are ignored by Git. Commit small, reviewed summaries and figures with their generation steps.

### Planned structure

The following layout is a roadmap. Create planned files and folders when there is actual content; the repository guide above lists the current files. Research questions remain in `docs/01-project-definition.md`.

```text
GR05-Predictive-Maintenance/
├── README.md
├── index.html                       # GitHub Pages landing page
├── assets/                          # Page styles, script, and favicon
├── requirements.txt                 # Add with the first working notebook
├── .gitignore
├── docs/
│   ├── 01-project-definition.md
│   ├── 02-business-case.md
│   ├── 03-data-inventory-access.md
│   ├── 04-dataset-evaluation.md
│   ├── 05-methodology.md            # Planned
│   ├── decisions.md                 # Planned
│   ├── references.md                # Planned
│   └── ai-use-log.md
├── data/
│   ├── README.md                    # Planned: download and storage instructions
│   ├── raw/                         # Local only; ignored by Git
│   └── processed/                   # Local only; ignored by Git
├── notebooks/                       # Planned
│   ├── 01-data-exploration.ipynb
│   ├── 02-preprocessing.ipynb
│   └── 03-modeling.ipynb
├── src/                             # Planned: extract reusable notebook code
│   ├── preprocessing.py
│   ├── features.py
│   ├── train.py
│   └── evaluate.py
├── reports/                         # Planned
│   ├── figures/
│   └── results/
└── presentations/                   # Planned
    ├── milestone/
    └── final/
```

## Project website

The [landing page](index.html) introduces the project and its current progress. The turbine is a decorative SVG illustration, not a visualization of dataset measurements. Findings remain marked as pending until experiments are documented. The site uses plain HTML, CSS, and JavaScript with no external libraries, fonts, analytics, or build step. Motion can be paused and follows the visitor's reduced-motion preference; all project content remains available without JavaScript.

Open `index.html` in a browser for a local preview. After reviewing and pushing, enable GitHub Pages under **Settings → Pages → Build and deployment → Deploy from a branch**, selecting **main** and **/(root)**. See [GitHub's publishing-source instructions](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site). The expected address after successful deployment is `https://cukowski.github.io/GR05-Predictive-Maintenance/`. Hosting has not been configured or verified as part of this change.

Update the status text, progress roadmap, and footer date in `index.html` as work advances. Replace the pending findings with reviewed figures and model comparisons only after recording their source experiments and evaluation protocol. Keep styles in `assets/site.css` and decorative behavior in `assets/site.js`.

## Next steps and milestones

1. Review both Task 2 drafts together; confirm the prediction point, baseline, and illustrative business scenario.
2. Obtain DS01 and record its source/version, license, filenames, sizes, and available hardware in the inventory report.
3. Implement reproducible schema inspection and a small initial EDA notebook. Confirm feasibility before expanding the scope.

| Date | Planned milestone |
|---|---|
| 22 October 2026 | Pilot feasibility and research scope decision |
| 19 November 2026 | Business case, dataset, and initial descriptive analysis presentation |
| 21 January 2027 | Final modeling, evaluation, business discussion, and presentation |

Planning: [Google Sheet roadmap](https://docs.google.com/spreadsheets/d/17AP7LQW_lRiLAHCcqhy8QmZdgw_bXJETPD5y3_tOEiU/edit).

## Working practices and AI disclosure

Keep changes small and commits meaningful. Do not commit raw datasets, credentials, local environments, or notebook checkpoints. Verify scientific claims and references, distinguish planned work from measured results, and retain enough information to reproduce analyses.

Follow [HFU guidance on academic work with AI tools](https://www.hs-furtwangen.de/en/hfu-insights/studying-at-hfu/academic-work-including-with-ai-tools): clarify permitted use and the declaration format with the lecturer. Record assistance and human verification in the [AI use log](docs/ai-use-log.md), and keep supporting conversations where useful or required by the lecturer.
