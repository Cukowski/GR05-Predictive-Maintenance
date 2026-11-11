# GR05 decision and limitation record

Updated 11 November 2026. This records implemented choices and explicit working proposals; it does not claim lecturer/team approval beyond the topic/dataset approval reported by the team.

| Decision / state | Rationale | Evidence / next action |
|---|---|---|
| Predict continuous RUL in flight cycles | Matches available labels and research question | Task 1; MAE/RMSE evaluation later |
| Predict at completed-flight end | Makes feature availability and unit of analysis explicit | Task 4; no future data in history features |
| Use DS01 + DS02 with source identity | Compatible schemas and available local files | Integrated flight table; DS01-only refit remains a sensitivity option |
| Link equal IDs conservatively across subsets | Independence is unresolved | Split checker; may over-group different physical engines |
| Quarantine DS02 development unit 10 | Same ID is supplied test in DS01 | 82 retained flights, excluded from fitting/validation/scoring |
| Fixed validation IDs 5, 6, 18 | Predeclared preparation policy rather than model-performance selection | config/preprocessing.json; re-fit within grouped CV later |
| 17 physical channels retained | Manageable original representation; no hidden simulator variables | P2 excluded initially; definition now confirmed but adding it is a separate feature experiment |
| P2 metadata corrected on 11 November | Journal Table 5 confirms total pressure at fan inlet, psia | Current dictionary/report corrected; output version fingerprint updates, numerical feature representation unchanged |
| Preserve finite unusual values | IQR flags do not establish physical errors | No automatic outlier deletion; invalid-key/label errors fail the pipeline |
| Training-only imputation/scaling | Avoid held-out information influencing preparation | Parameter checks and tests; y stays unchanged |
| Feature history uses current/prior flights only | Respect the prediction point | Future-change invariance test |
| Keep a 20-column baseline selection beside 50 candidates | Manageable comparison for a small fleet | No claim that engineering improves accuracy before modeling |
| Task 5 reconstruction is descriptive input only | Cycle means cannot restore within-flight variance | Default tracked source; explicit full Task 4 option |
| H1–H4 assessment is exploratory/descriptive | Dependent flights and few groups do not support independent-observation significance claims | No causal/p-value claims; results motivate future comparisons |
| Prior test/validation inspection is disclosed | Those partitions were already examined for data understanding/review | Not a blinded confirmatory study; avoid adaptive tuning to test |
| Dates: 12 Nov progress, 19 Nov milestone | Lecturer semester schedule and overview slide 9 distinguish the weeks | All current slides/notes corrected; confirm class time/duration separately |
| Working roles/models are proposed | Actual individual assignments cannot be inferred from task files alone | Task 1 role table; both students to confirm and rehearse |
| Source metadata labels differ | Journal says dataset CC0 1.0; Kaggle currently labels U.S. Government Works | Record separately; original download-version/receipt and upstream checksum match remain unverified |
| Raw and prepared versions stay local | Avoid publishing large raw data or private/local material | Git ignore rules; compact evidence and local hash manifests retained |

The current prepared version is named by [the manifest](../reports/results/task4/manifest.json). Code, configuration and source hashes determine the version; previous local directories remain intact. A metadata/source-definition refresh can create a new version without changing the selected 17-channel numerical representation.
