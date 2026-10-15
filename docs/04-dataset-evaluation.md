# N-CMAPSS Dataset Proposal — For Professor Review

> **Historical proposal:** The lecturer has since approved the topic and dataset. The proposal below is retained as context; its questions reflect the proposal stage. See the current [Business Case Report](02-business-case.md) and [Data Inventory & Access Report](03-data-inventory-access.md) for Task 2 progress. Data access and feasibility remain unverified.

**GR05 · Manufacturing / Maintenance · 15 October 2026**  
**Students:** Selçuk Ata Aksoy and Denzel Gregory Pragassa

## Proposed topic
**Predictive Maintenance Using Aircraft Engine Sensor Data: Remaining Useful Life Estimation**

**Problem:** Equipment degradation can create unexpected downtime and maintenance expenditure. Can data analytics help estimate when maintenance may be needed?

**Research question:** How accurately can classical regression models predict the remaining useful life (RUL) of simulated turbofan engines from operational and sensor data, compared to a simple baseline?

## Dataset and scientific source
N-CMAPSS, described in Arias Chao et al. (2021), *Aircraft Engine Run-to-Failure Dataset under Real Flight Conditions for Prognostics and Diagnostics*, Data 6(1), 5. https://www.mdpi.com/2306-5729/6/1/5

Official NASA Prognostics Center of Excellence repository (*Turbofan Engine Degradation Simulation Data Set 2*): https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/

The dataset contains simulated engine-degradation trajectories driven by real flight-condition profiles. Engine failures are **simulated**, not observed real-world failure events.

## Proposed work
- Select and inspect one manageable subset (DS01 candidate); verify schema, labels, file size, and conditions of use.
- Perform data exploration: operating conditions, engine sensor trajectories, correlations, and RUL evolution.
- Build simple baseline forecasts and compare classical ML regression models.
- Evaluate with MAE/RMSE in flight cycles using proper engine-level holdout without target leakage.
- Discuss how predicted RUL might influence maintenance decisions in an **illustrative**, not deployed, scenario.

## Course milestones
- **15 Oct:** topic and dataset discussion with lecturer
- **By 22 Oct:** pilot data feasibility and research scope decision
- **19 Nov:** business case, dataset and initial descriptive analysis presentation
- **21 Jan:** final modeling, evaluation, business discussion and presentation

## Questions for Professor
1. Is N-CMAPSS suitable for the Manufacturing/Maintenance domain despite its simulated degradation?
2. Is RUL regression with baseline comparisons sufficient as a semester-project core scope?
3. Are there additional grading, report, or presentation requirements?

**Current status:** research proposal only; data parsing, experiments and model results have not been completed.
