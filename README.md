# GR05 — Predictive Maintenance: Aircraft Engine Remaining Useful Life

Industrial Analytics · WS 2026/27 · Manufacturing / Maintenance

**Team:** Selçuk Ata Aksoy and Denzel Gregory Pragassa  
**Lecturer:** Prof. Dr. Monika Frey-Luxemburger  
**Status:** N-CMAPSS dataset proposal lecturer confirmed. (Kaggle Dataset: https://www.kaggle.com/datasets/bishals098/nasa-cmapss-2-engine-degradation)

## Problem
Unexpected equipment degradation can cause interruptions and maintenance costs. The project investigates whether sensor and operating data can estimate remaining useful life (RUL) to support maintenance planning.

## Research question
**How accurately can machine-learning regression models estimate the remaining useful life of simulated aircraft engines using N-CMAPSS sensor and operational data, compared with a simple baseline?**

## Dataset
- N-CMAPSS, introduced by Arias Chao et al. (2021), *Aircraft Engine Run-to-Failure Dataset under Real Flight Conditions for Prognostics and Diagnostics*: https://www.mdpi.com/2306-5729/6/1/5
- NASA PCoE repository, Turbofan Engine Degradation Simulation Data Set 2: https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/
- Kaggle Dataset: https://www.kaggle.com/datasets/bishals098/nasa-cmapss-2-engine-degradation
- Operating conditions are derived from real flight profiles; engine deterioration and sensor responses are simulated, **not records of real engine failures**.
- Proposed starting point: a feasible DS01 pilot, subject to verifying dataset files, licensing, and resource needs.

## Method
CRISP-DM: business understanding, data understanding, preparation, modeling, evaluation and business implications. Start with a simple RUL baseline, then compare regression models such as linear regression and random forest. Evaluate MAE/RMSE in remaining flight cycles, using held-out engines where feasible and documenting potential leakage.

## Deliverables
Project proposal and data evaluation; initial descriptive analysis; reproducible Python notebooks and model comparison; limitations and illustrative maintenance implications; milestone (19 Nov 2026) and final presentation (21 Jan 2027).

## Documentation
- [Project definition](docs/01-project-definition.md)
- [Dataset proposal](docs/04-dataset-evaluation.md)
- [Google Sheet roadmap](https://docs.google.com/spreadsheets/d/17AP7LQW_lRiLAHCcqhy8QmZdgw_bXJETPD5y3_tOEiU/edit)

Do not commit large raw datasets. Check HFU rules for AI-assisted academic work: https://www.hs-furtwangen.de/en/hfu-insights/studying-at-hfu/academic-work-including-with-ai-tools
