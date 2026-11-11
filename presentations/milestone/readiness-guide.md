# V6 milestone — readiness and rehearsal guide

**Prepared 11 November 2026. Progress/preparation session: 12 November 2026. Milestone presentation: Thursday 19 November 2026**, explicitly stated in lecturer overview slide 9. Confirm class time, allowed duration and required template separately.

**Assessment:** the technical evidence and draft presentation now cover the V6 milestone topics. Human review, speaking allocation, timing, and rehearsal remain. Do not describe the project as fully completed or the models as evaluated.

## Open these first

1. [Editable slide deck with embedded notes](GR05-milestone-draft.pptx).
2. [Portable full PDF](GR05-milestone-draft.pdf) and [short-route PDF](GR05-milestone-short-route.pdf).
3. [Speaker notes](speaker-notes.md), including proposed presenters and a 22-slide route.
4. [Task 5 dashboard](../../analysis.html), [Task 5 report](../../docs/07-task5-descriptive-analysis.md), and [executed notebook](../../notebooks/03-descriptive-analysis.ipynb).
5. [Local data placement](../../data/README.md) and [Task 4 manifest](../../reports/results/task4/manifest.json).

The full deck has 40 slides to reflect the breadth suggested by the separate milestone comments handout (including 10 theory and 5 business-understanding slides). It is not automatically appropriate for a short slot. The 22-slide route covers the V6 topics but reduces the separate handout's recommended slide counts; confirm the duration before choosing it. Do not rush 40 slides into 15 minutes.

The PDF uses the same slide specification as the editable PowerPoint and is a portable offline fallback. PowerPoint contains notes; the PDF does not. Open the PPTX on the presentation machine once to check fonts and rendering. Speaker/creator labels and slide numbers are included throughout. Presenter labels are proposals to confirm, not claims about actual individual work.

## V6 requirements mapped to evidence

Source: `tasks/IBS6 Industrial Analytics Project Tasks V6.0.pdf`, dated 9 November 2026; internal heading still V12.0. Pages 1–2 enumerate Tasks 1–6. The separate comments handout recommends coverage and requires slide numbers and creator/presenter names.

| Task/topic | Evidence available now | Remaining human decision / limitation |
|---|---|---|
| Introduction: team, domain, glossary, literature | README/team, notebook explanations, theory slides, sources | Both students must understand terms and review references; literature work is not claimed exhaustive |
| Task 1: scope, objectives, stakeholders/roles, timeline, success criteria | Project definition, proposed speaking allocation, visual roadmap, planned MAE/RMSE comparison | Confirm working role allocation and class time; no lecturer-approved error threshold is invented |
| Task 2: business case and inventory/access | Business case draft, inventory, data README, source sizes/hashes | Team review and original local download-version matching remain open; current source labels are recorded; savings are hypothetical |
| Task 3: structure/features, scales, distributions, quality | Executed notebook, full scan summaries and feature table | Accuracy/timestamps/independence limits remain; P2 source definition has been corrected from journal Table 5 |
| Task 4: cleaning, transformation, engineering, integration, versions | Executed notebook, pipeline, local X/y/rows, fitted transforms and manifest | No RUL model fitted; raw/prepared data stay local, not on GitHub |
| Task 5: statistics, patterns, hypotheses, grouping, business insight | Executed descriptive notebook, report, 6 analysis charts, structural charts, insight JSON | Hypothesis assessment is descriptive, not statistical proof or causal validation |
| Task 5: dashboard, summary, storytelling slide | `analysis.html`, report/JSON, deck slide 33 | Review narrative and rehearse; no model scores or savings |
| Task 6: introduction/plan/deliverables | Slides 1–4 and roadmap graphic | Confirm date and timing |
| Task 6: theory/business understanding | Slides 5–19 | Proposed speaker split; don't overrun allowed time |
| Task 6: source, understanding, preparation, raw/prepared comparison | Slides 20–28, local manifests and prepared files | Open files before speaking; don't start a full raw scan live |
| Task 6: initial descriptive visuals | Slides 29–33, dashboard | Explain sample unit and limitations with each plot |
| Task 6: one ML algorithm per student | Slides 34–37: linear regression / random forest | Proposed presenters Selçuk / Denzel; not yet trained, compare to constant baselines later |
| Task 6: next steps and timeline | Slide 38 and proposed roadmap | Future dates are team targets, not new lecturer deadlines |
| Presentation form | 40-slide PPTX/PDF with sources, slide numbers, creator/presenter footers and notes | Team must approve individual attribution and preview actual PPTX |

**Do we need model scores tomorrow?** V6 Task 6 asks for algorithm overviews, not a completed modeling/evaluation result. Explain the planned models honestly. Do not add rushed scores solely to make the deck appear more complete.

## The 90-second project explanation

“We are investigating whether sensor and operating data can estimate remaining useful life of simulated aircraft engines. The operating profiles are realistic, but degradation and sensor responses are simulated. Our two local N-CMAPSS subsets contain about 14.16 million readings. We turn those into 1,542 completed-flight entries because our prediction would be made at flight end.

We keep engine histories separate, fit preprocessing on training data only, and exclude hidden simulator health information. A possible cross-subset test-history link led us to quarantine 82 DS02 flights. We now have 574 training, 343 validation and 543 test flights.

Our descriptive analysis finds a negative association between T48 temperature and RUL in all seven training source histories, with correlations between −0.540 and −0.299. Operating context and a small number of engine groups limit what that means. Next we will compare simple constant baselines with linear regression and random forest. We have not yet measured RUL prediction accuracy or business savings.”

Practise this without memorizing every number. Be able to explain why each number matters.

## Numbers to know and what they mean

| Number | Meaning |
|---|---|
| 14,159,058 | Ordered readings across both local HDF5 files |
| 47 | Stored fields across W, X_s, X_v, T, Y, A; not all valid predictors |
| 19 | Dataset-scoped source histories, not proven independent engines |
| 1,542 | Dataset-engine-flight rows |
| 17 | Physical channels retained in the frozen Task 4 version (P2 excluded then) |
| 45 | Numeric candidate features before missingness/source indicators |
| 50 | Finite candidate model columns; 20-column simpler selection available |
| 574 / 343 / 543 / 82 | Training / validation / provided test / quarantine flights |
| 7 / 6 | Training source histories / conservative unit-ID groups |
| 57 | Expected first-flight missing differences across all 19 histories, not raw sensor NaNs |
| 567 | Nonmissing training values per previous-flight difference |
| −0.540 to −0.299 | T48–RUL per-training-history Pearson r |
| +13.62 K | Median paired late-minus-early T48 engine-stage median contrast across 7 histories |

## Likely questions — answers you should understand

**What is a raw row?** One aligned snapshot of flight conditions and sensor responses. Several readings share an engine, flight cycle and RUL label. They are not automatically duplicate errors.

**What is a prepared row?** One completed flight, using its own readings and earlier flights only. Prediction is explicitly at flight end.

**What is X versus y?** X is the allowed input information; y is true historical RUL in cycles. We store them separately so a model cannot read the answer.

**What does RUL zero mean?** The final simulated cycle under the verified convention. RUL equals final observed cycle minus current cycle. That final cycle is known retrospectively and excluded from predictors.

**Which inputs matter?** Physical operating conditions and sensor channels are candidates. T48 shows a descriptive association, but we have not demonstrated which features improve held-out predictions.

**Why not use all 47 fields?** They include the answer, IDs, labels and privileged simulator quantities. More columns can cause leakage, not better learning.

**Is this real failure data?** No. Real flight profiles drive simulated engine degradation and responses. We cannot claim real-world validation.

**What are T48, Nc and Wf?** T48 is total temperature at the high-pressure turbine outlet; Nc is physical core shaft speed; Wf is fuel flow. Prepared units are K, rpm and kg/s.

**What happened to P2?** The older local preprint omitted it, so the frozen preparation excluded it. We have now confirmed its definition in the 2021 journal Table 5: total pressure at fan inlet, psia. It can be reconsidered as a separate feature experiment. The source-definition refresh updates version identity without adding this channel.

**Why summarize by flight?** That matches the prediction point and makes a manageable dataset. It loses transient details and mixes phases, so it is a first representation rather than a universal optimum.

**What did cleaning remove?** No actual selected raw predictor values needed removal in this run. We checked validity and consistency, converted units and handled engineered gaps. We do not manufacture cleaning problems or delete IQR outliers blindly.

**Why missing values if the raw data has no NaNs?** A first-flight change has no previous flight. Three such differences across 19 histories produce 57 legitimate missing feature cells. Training medians and indicators handle them.

**What is scaling?** Subtract a training mean and divide by a training standard deviation so numeric ranges are comparable. It does not isolate degradation or make held-out values follow the training distribution.

**Why engine-based splits?** Random flight/reading splits could share the same history on both sides. All linked engine groups stay in one active split.

**Why quarantine unit 10?** That ID is supplied test in DS01 and development in DS02. Independence is unresolved, so the DS02 development history is retained but excluded from fitting/validation/scoring.

**What did Task 5 validate?** It assessed exploratory hypotheses descriptively. It did not conduct an independent-subject significance test, prove causation, or establish predictive value. Validation was already seen during branch review, so its check is not blinded confirmation.

**Can the RUL-stage groups be model inputs?** No; they require the true target. We use them retrospectively to explain historical patterns, not for deployment.

**Why is temperature higher late in life?** It is consistent with a candidate degradation-related pattern, but changing operating conditions and engine/source composition remain alternatives. We did not isolate a causal effect.

**What about the other sensors?** Their correlations differ; core speed even changes sign across training histories. A universal threshold is not justified. Small pooled delta correlations do not prove the absence of nonlinear predictive information.

**Why linear regression and random forest?** Linear regression is transparent; random forest is a manageable nonlinear comparison. Neither has been fitted here. Both must be compared on the same group-aware protocol against simple constants.

**What is MAE/RMSE?** MAE averages absolute cycle errors; RMSE emphasizes larger errors and remains in cycles. Report per-engine and macro-average errors as well as overall results.

**Have we saved money?** No observed economic outcomes exist. Savings and maintenance consequences remain qualitative scenarios.

**Can this be used on an aircraft?** No operational validation or certification is claimed. This is an offline student experiment.

## A three-minute demo with an offline fallback

1. Open the PDF and dashboard **before** the presentation. Verify that the figures load locally; don't depend on GitHub deployment or internet.
2. In Jupyter, show one Task 3 row/feature-table explanation. Explain unit/category differences.
3. Show the Task 4 manifest and a few rows of the existing prepared table. Show the same row identity across X/y/rows and point out that y is separate.
4. Open Task 5's recorded T48 result and life-stage chart. Say “association, not a causal effect or model score.”
5. Return to the next-steps slide. If software fails, use the PDF/chart exports; don't spend the talk debugging.

Do not run a 5 GB scan, regenerate the environment, or train an unplanned model live. No raw or processed datasets need to be uploaded to present the evidence.

## Before you call yourselves ready

- Use **12 November for progress/preparation and 19 November for the milestone**. Confirm time, allowed duration and required template.
- Agree proposed presenter/algorithm assignments and edit footer names if needed. Both students should be able to explain their individual contribution and AI assistance honestly.
- Review business-case and source claims. Current Kaggle v1/license label is recorded; the original download-version match remains unproven; say so if asked.
- Choose the full or short route and time a complete rehearsal. The long theoretical section follows the handout's recommendations but may not fit a short slot.
- Open the actual PowerPoint and offline PDF on the presentation machine. Font/rendering checks in a real presentation app remain a human task.
- Keep the raw and prepared datasets available locally if the lecturer asks to inspect them. Ensure the version path agrees with the manifest.
- Read the three limitations you must mention: simulated responses, few independent groups, operating-condition confounding.
- Never present the absence of model scores as a hidden completed experiment. State clearly that modeling is next.

These are readiness actions specific to the requested presentation, not a claim that the lecturer has approved the draft.


## For 12 November: show progress, then prepare the 19 November talk

Start with [the current task audit](../../docs/08-progress-audit.md) and [progress page](../../progress.html). Use its five-minute route to show Tasks 1–5, the split/feature decisions and one descriptive story. The full 40-slide deck is for milestone preparation, not a claim that a full talk is required in tomorrow's progress session. The final presentation remains 21 January 2027.

The reports and execution evidence are available; review/rehearsal and working-role confirmation remain team actions. Run `python scripts/check_project.py --raw-hashes --write-report` for current verification. This does not publish GitHub Pages or train a model.
