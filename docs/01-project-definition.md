# Task 1 — Project Definition

**Course:** Industrial Analytics · HFU · WS 2026/27<br>
**Group/domain:** GR05 · Manufacturing / Maintenance<br>
**Team:** Selçuk Ata Aksoy and Denzel Gregory Pragassa<br>
**Lecturer:** Prof. Dr. Monika Frey-Luxemburger<br>
**Status, 11 November:** Topic/dataset approved as reported by the team. Definition and progress artifacts are prepared; the team should confirm the working role allocation before the milestone.

## Problem and research question

Unexpected equipment deterioration makes maintenance timing uncertain. The project asks:

**How accurately can classical regression models estimate Remaining Useful Life (RUL) of simulated turbofan engines from operating and sensor data, compared with transparent constant baselines?**

RUL is a numerical count of remaining flight cycles, not a fault-class label. The selected prediction point is **the end of a completed flight**. A prediction uses that flight's observations and earlier observed flights; it cannot use future measurements, known final lifetime, or simulator-only health state.

## Scope, objectives and constraints

1. Explain N-CMAPSS DS01/DS02 sources, schema, units, scales and quality limitations.
2. Prepare reproducible flight-level features from the two local files, maintaining source identity.
3. Preserve supplied test histories, group equal unit IDs conservatively across subsets, and quarantine DS02 development unit 10 because the same ID is supplied test in DS01.
4. Establish transparent constant RUL references; then compare linear regression and random forest using development-engine validation.
5. Report errors in cycles, engine-level differences, overoptimistic estimates and limitations.
6. Explain plausible maintenance-planning implications without claiming measured savings or operational suitability.

Tasks 3–5 currently provide the data evidence and preparation; objective 4's predictive model experiments and objective 5's model scores remain later work. The integrated representation has 1,542 flight rows, 45 numeric candidates and a 20-column simpler modeling selection after transformation. DS01-only refitting remains a possible sensitivity experiment.

Constraints: two students; few independent engine groups; source/mission shift; simulated degradation and responses; whole-flight phase mixing; unresolved cross-subset identity. Deep learning, production deployment and operational aviation validation are outside the initial scope. No substantial raw dataset is committed to Git.

## Stakeholders and working roles

| Participant / stakeholder | Responsibility / interest | Basis |
|---|---|---|
| Selçuk Ata Aksoy | Proposed coordination, pipeline/reproducibility and linear-regression explanation | Working allocation for progress; team to confirm |
| Denzel Gregory Pragassa | Descriptive-analysis foundation, literature/business explanation and proposed random-forest overview | Task 5 commits establish the analysis foundation; future allocation to confirm |
| Both students | Source checking, interpretation, AI disclosure, joint review, individual understanding and rehearsal | Shared project responsibility |
| Lecturer | Topic/scope feedback and academic assessment | Course context |
| Hypothetical maintenance/reliability/operations users | Lead time, forecast errors and maintenance trade-offs | Business-case stakeholders, not claimed external partners |

These roles do not imply lecturer approval or assert that each person independently authored AI-assisted material. Actual work is traceable through commits and [the AI use log](ai-use-log.md).

## Measurable success criteria

| Criterion | How it is assessed | Current state |
|---|---|---|
| Reproducible input identity | Local raw SHA-256, schema/quality exports, prepared-version manifest | Available |
| Leakage-resistant representation | Flight-end features; no target/hidden health in X; group-separated splits; training-only fitted preparation | Implemented and checked |
| Complete descriptive evidence | Executed notebook, statistics, grouping, charts, documented findings/limits | Available |
| Baseline-relative RUL performance | Compare MAE/RMSE in cycles against mean/median constant references on development groups | Planned; no scores yet |
| Engine-level generalization | Per-engine errors and macro averages, with optimism/underprediction analysis | Planned |
| Honest business interpretation | Separate observed statistics, proposed modeling, and hypothetical value | Applied in reports/slides |

No numerical MAE/RMSE acceptance threshold has been agreed; none is invented. The research is still informative if a simple model does not outperform its baseline, provided the evaluation and negative result are reported rigorously.

## Project plan and deliverables

| Period / date | Work and evidence | Status |
|---|---|---|
| 15–22 October | Definition, topic approval, business case, dataset access | Documented |
| 22 October | Data understanding notebook and quality evidence | Executed; refreshed for current progress |
| 29 October | Preparation pipeline and local versioned matrices | Implemented; current version recorded in manifest |
| 5–11 November | Denzel's Task 5 draft, review, execution/reporting completion | Available |
| **12 November** | **Progress / Task 6 preparation session** | Ready for progress discussion |
| **19 November** | **Milestone presentation** | Draft slides/notes available; rehearse and confirm duration |
| After milestone–December | Constant baselines, regressors and group-aware evaluation | Team planning target |
| December–January | Robustness, error analysis, business interpretation, final synthesis | Team planning target |
| **21 January 2027** | **Final presentation**, per lecturer overview | Scheduled in supplied material |

The visual roadmap is in [the milestone assets](../presentations/milestone/assets/roadmap.png); deliverables are mapped individually in [the readiness guide](../presentations/milestone/readiness-guide.md). Future work windows are team planning proposals, not extra lecturer deadlines.

## Method and references

Follow CRISP-DM: business understanding → data understanding → preparation → modeling → evaluation → business implications. See [focused literature notes](literature-notes.md), [glossary](glossary.md), [decisions](decisions.md), [references](references.md), [business case](02-business-case.md) and the [V6 task audit](08-progress-audit.md).
