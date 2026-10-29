# GR05 — Project Definition

**Course:** Industrial Analytics (WS 2026/27)  
**Group:** GR05, Manufacturing / Maintenance  
**Team:** Selçuk Ata Aksoy and Denzel Gregory Pragassa  
**Supervisor:** Prof. Dr. Monika Frey-Luxemburger  
**Status:** Topic and N-CMAPSS dataset approved by the lecturer; local DS01/DS02 access and descriptive feasibility verified; source terms and team scope review pending.

## One-sentence problem
Unexpected deterioration of industrial machinery can lead to unplanned downtime and additional maintenance costs, and sensor-based estimates of remaining useful life may support earlier maintenance planning.

## Primary research question
How accurately can classical machine-learning regression models estimate the remaining useful life (RUL) of simulated aircraft engines using N-CMAPSS operating and sensor data, relative to a simple baseline?

**Target:** remaining flight cycles until simulated end-of-life. This is a regression problem, not binary failure detection.

**Proposed success measures:** MAE and RMSE in flight cycles, evaluated on held-out engine units where supported by the dataset. No performance claim has yet been demonstrated.

## Objectives
1. Verify N-CMAPSS data availability, format and licensing and choose a manageable subset (DS01 is a candidate).
2. Understand flight-cycle histories, engine identifiers, sensor variables and RUL labels.
3. Prepare features and a leakage-resistant train/test design.
4. Implement a transparent baseline and compare at least one regression model.
5. Report RUL errors and qualitative limitations for maintenance decision support.
6. Present reproducible experiments, citations and an illustrative business-impact scenario.

## Research boundaries
The degradation processes and sensor measurements are simulated under operating conditions drawn from real flight profiles. Do not claim actual engine failures, operational validation, regulatory certification or guaranteed maintenance savings. Advanced deep learning and live deployment are out of initial scope.

## Methodology
CRISP-DM: business understanding → data understanding → preparation → modeling → evaluation → practical implications.

## Next decisions
- [x] Confirm with lecturer that N-CMAPSS/RUL is acceptable in the Manufacturing group.
- [x] Download and audit DS01/DS02 locally; record file identity and remaining provenance questions.
- [x] Define the end-of-flight predictor/target representation and conservative engine-group splits for Task 4.
- [ ] Finalize research scope after feasibility assessment.
