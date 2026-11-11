# GR05 references and source register

Updated/checked 11 November 2026. Primary scientific, software and course sources are distinguished from local generated evidence.

| Source | Use / limits |
|---|---|
| Arias Chao, M., Kulkarni, C., Goebel, K., & Fink, O. (2021). *Aircraft Engine Run-to-Failure Dataset under Real Flight Conditions for Prognostics and Diagnostics*. Data, 6(1), 5. [DOI](https://doi.org/10.3390/data6010005) | Dataset description; journal Table 5 confirms P2 and units; paper declares dataset CC0 1.0 |
| [NASA PCoE repository](https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/) | Original provider context; local checksums have not been compared with an upstream signed reference |
| [Kaggle redistribution](https://www.kaggle.com/datasets/bishals098/nasa-cmapss-2-engine-degradation) and [public metadata](https://www.kaggle.com/api/v1/datasets/view/bishals098/nasa-cmapss-2-engine-degradation) | Team-reported download source; current metadata reports v1, last update 10 Aug 2025, license label U.S. Government Works; original download-version match unverified |
| Supplied 7-page April 2020 preprint, local `data/Run_to_Failure_Simulation_Under_Real_Flight_Conditions_Dataset.pdf` | DS02-focused source/units; differs from later journal tables, notably P2 omitted |
| Supplied example notebook credited to Manuel Arias, local `data/N-CMAPSS_Example_data_loading_and_exploration.ipynb` | Loading and schema reference; not executed blindly or presented as team-authored analysis |
| Lecturer Project Tasks V6.0, dated 9 Nov 2026, pp. 1–2; internal heading V12.0 | Current Tasks 1–6 deliverables; local-only course material |
| Lecturer Semester Overview V1.0 | Week of 9 Nov: Task 6 preparation; week of 16 Nov: milestone |
| Lecturer IA Overview V1.0, slide 9 | Explicit milestone 19 Nov 2026; final 21 Jan 2027 |
| Lecturer milestone-comments handout | Topic coverage, recommended slide counts, creator/presenter labels and slide numbers |
| Lecturer Dataset Scales PPTX, slides 3–4, and Task 3 feature-table notebook | Scale meanings, valid operations, dtype/feature-summary format; statistical scale is not inferred solely from dtype |
| [scikit-learn common pitfalls](https://scikit-learn.org/stable/common_pitfalls.html) | Training-only fitted transformations and leakage |
| [SimpleImputer](https://scikit-learn.org/stable/modules/generated/sklearn.impute.SimpleImputer.html), [StandardScaler](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html), [OneHotEncoder](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html) | Implemented preprocessing components |
| [Linear models](https://scikit-learn.org/stable/modules/linear_model.html#ordinary-least-squares), [random forests](https://scikit-learn.org/stable/modules/ensemble.html#forest), [regression metrics](https://scikit-learn.org/stable/modules/model_evaluation.html#regression-metrics) | Proposed modeling explanations and future evaluation; no model scores yet |
| [HFU AI guidance](https://www.hs-furtwangen.de/en/hfu-insights/studying-at-hfu/academic-work-including-with-ai-tools) | Confirm permitted use/declaration with lecturer; actual assistance is in the AI log |

Generated notebook tables, JSON manifests, charts and report pages are **project outputs**, not independent datasets or additional literature. Their source hashes and limitations are preserved in the relevant Task 3–5 evidence. Course materials and large/local reference files remain ignored by Git.
