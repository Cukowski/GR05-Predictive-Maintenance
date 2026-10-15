# Task 2 — Business Case Report (Draft)

**GR05 — Industrial Analytics WS 2026/27**\
**Team:** Selçuk Ata Aksoy and Denzel Gregory Pragassa\
**Domain:** Manufacturing / Maintenance\
**Topic:** Aircraft Engine Remaining Useful Life Estimation with NASA N-CMAPSS\
**Status:** Professor-approved topic and dataset; analysis not yet performed.

## Business problem
Unexpected equipment degradation can increase maintenance uncertainty, cause operational interruptions, and lead to expensive maintenance decisions. Maintenance planners must balance early inspection against the risks of continuing to operate an asset close to its end-of-life.

## Value proposition
Explore whether regression models trained on simulated aircraft-engine operating conditions and sensor measurements can estimate **remaining useful life (RUL), in flight cycles**, more accurately than a transparent baseline. Reliable estimates could potentially assist maintenance planning; the project will not claim demonstrated cost savings or aviation suitability.

## Stakeholders
| Stakeholder | Interest or potential impact |
|---|---|
| Maintenance planning team | Scheduling interventions with appropriate lead time |
| Reliability engineers | Assessing degradation signals and model uncertainty |
| Operations management | Understanding downtime and premature-maintenance trade-offs |
| Data analytics team | Reproducible modeling, validation, and results |
| Safety/compliance stakeholders | Avoiding false reassurance and unsafe interpretation |

## Project research question
How accurately can classical regression models estimate remaining useful life of simulated turbofan engines using the N-CMAPSS dataset, compared with a simple baseline?

## KPIs and success criteria
**Technical, measurable with dataset:**
- Mean Absolute Error (MAE), in flight cycles, on held-out engines.
- Root Mean Squared Error (RMSE), in flight cycles, on held-out engines.
- Improvement or deterioration relative to the defined baseline.
- Error distribution by engine and analysis of RUL overestimation (optimism).
- Reproducible training and evaluation procedure with no target leakage.

**Business KPIs, to be discussed only as hypothetical scenarios:** equipment availability, unscheduled downtime, maintenance lead time, intervention frequency, and costs of early/late maintenance. Dataset has no verified observed economic outcomes; do not present numerical savings as measured facts.

## Scope and limitations
- N-CMAPSS uses **real flight operating profiles with simulated engine degradation**. It is not measured real-world run-to-failure engine data.
- Offline demonstration only; not a deployable aircraft safety or maintenance system.
- Initial pilot: one manageable subset, likely DS01, subject to the actual Kaggle files.
- Evaluate by engine (and respect predefined train/test partition as appropriate), not by randomly mixing time samples from a single engine.
- Use sensor and operating features available at the time of prediction; exclude target RUL and inaccessible health/model parameters.

## Decisions still open
- [ ] Confirm when predictions are made (end of each flight vs. arbitrary measurement sample).
- [ ] Choose actual baseline after exploring the data.
- [ ] Choose preliminary metric interpretation and business use-case scenario.
- [ ] Have both team members review and revise this draft.

## Sources
Arias Chao, M., Kulkarni, C., Goebel, K., & Fink, O. (2021). *Aircraft Engine Run-to-Failure Dataset under Real Flight Conditions for Prognostics and Diagnostics*. Data, 6(1), 5. https://doi.org/10.3390/data6010005

HFU Industrial Analytics Project Tasks V2.0, 15 October 2026.
