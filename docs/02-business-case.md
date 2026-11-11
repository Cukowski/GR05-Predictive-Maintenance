# Task 2 — Business Case Report

**GR05 · Industrial Analytics · WS 2026/27**<br>
**Team:** Selçuk Ata Aksoy and Denzel Gregory Pragassa<br>
**Updated:** 11 November 2026 · prepared for the 12 November progress session.<br>
**Scope:** Offline student research; topic/dataset approved as reported by the team. No externally deployed system or measured economic outcome is claimed.

## Business problem and theoretical context

Maintenance planners balance continued operation against intervention lead time and the consequences of deteriorating equipment. Reactive maintenance responds after a fault; preventive maintenance uses planned intervals; predictive approaches use condition/history to estimate future needs. Diagnosis asks about present condition, while prognosis asks about future evolution or remaining useful life.

Our question is whether operating/sensor histories can estimate the RUL of simulated turbofan engines better than a transparent reference prediction. This is a regression problem, producing remaining flight cycles rather than a yes/no failure flag. The research may identify useful signals and forecasting limitations; it does not establish a maintenance policy for real aircraft.

## Proposed value and stakeholder impact

| Stakeholder | Potential use | Evidence needed before claiming value |
|---|---|---|
| Maintenance planners | Discuss intervention lead time | Independent forecast validation and a defined planning process |
| Reliability engineers | Examine signals and optimistic error cases | Error distributions, operating-context analysis and limitations |
| Operations management | Understand downtime/premature-maintenance trade-offs | Real cost, schedule and intervention data absent from this dataset |
| Analytics team / students | Reproducible baseline-versus-regressor comparison | Traceable features, group splits, scripts and honest reporting |
| Lecturer | Assess understanding, method and individual contribution | Reports, executed notebooks, explanations and presentation |

The industrial stakeholders are illustrative users, not organisations we claim to have consulted. Denzel and Selçuk are the actual project team; proposed responsibilities and review duties are documented in [Task 1](01-project-definition.md).

## Research question and decision scenario

**How accurately can classical regression models estimate engine RUL from operating/sensor data compared with simple constant baselines?**

Decision scenario: after a completed flight, a planner could review an RUL estimate alongside other approved maintenance information. Overestimation could encourage excessive confidence in remaining life; underestimation could prompt premature work. These are hypothetical implications, not observed errors or financial effects from this project. The dataset has no verified maintenance costs, downtime outcomes or economic intervention records.

## KPIs and success criteria

| KPI / check | Meaning | Evidence stage |
|---|---|---|
| MAE in flight cycles | Average absolute prediction error | Later model evaluation |
| RMSE in flight cycles | Greater emphasis on large cycle errors | Later model evaluation |
| Baseline-relative difference | Does a regressor improve on a constant mean/median reference? | Later development validation |
| Per-engine errors and macro averages | Prevent repeated flights from masking engine differences | Later evaluation |
| RUL optimism / error distribution | Examine potentially misleading overestimates | Later evaluation |
| Split and preprocessing integrity | No related engine across active splits; training-only learned transforms | Implemented and tested |
| Reproducibility and traceability | Raw identity, versioned features, executed outputs, source limits | Implemented and documented |

No target error threshold or minimum saving has been agreed with the lecturer. Good research requires an honest comparison, including when a regressor fails to beat a baseline. Hypothetical business KPIs (availability, intervention frequency, downtime and cost) cannot be reported as measured numerical project results.

## Data relevance and current feasibility

N-CMAPSS supplies run-to-failure histories, operating conditions, sensor channels and RUL labels. We acquired DS01/DS02 locally and completed data understanding, preparation and descriptive analysis. There are 14,159,058 readings and 1,542 flight rows from 19 dataset-scoped histories; those histories are not proven independent across subsets.

At the selected flight-end prediction point, valid current/earlier sensor and operating features are available. Hidden simulator health parameters, virtual sensors, true RUL and final lifetime are excluded from predictors. Raw/processed datasets remain local; compact audit evidence can be reviewed in Git.

## What has been learned so far

Task 5 uses 574 training flights, seven source histories but six conservative engine groups. T48–RUL correlation is negative in all seven source histories (−0.540 to −0.299). Paired late-minus-early engine-median T48 differs by +13.62 K median. This motivates temperature/context features for later evaluation; it does not prove wear causality, forecast accuracy or savings. Validation was already seen during review; its fixed descriptive check is not blinded confirmation.

## Boundaries, risks and next work

- Operating profiles are realistic; degradation and sensor responses are simulated.
- Few independent groups and changing operating regimes limit generalization.
- Phase mixing, source indicators and repeated flights may create misleading associations.
- Current Kaggle metadata and its different license label are recorded in the inventory; the exact original download-version match is unproven.
- The team must review the narrative and be able to explain individual contributions, including AI assistance.

Next: compare constant baselines, linear regression and random forest using development-engine validation, then reserve supplied test for final model evaluation. No predictive model has yet been trained.

## Sources

[Task 2 inventory](03-data-inventory-access.md), [Task 5 evidence](07-task5-descriptive-analysis.md), [source metadata](../reports/results/source_metadata.json), and [Arias Chao et al. (2021)](https://doi.org/10.3390/data6010005). Course requirements: supplied Project Tasks V6.0 pp. 1–2; dates: lecturer overview slide 9. [AI assistance disclosure](ai-use-log.md).
