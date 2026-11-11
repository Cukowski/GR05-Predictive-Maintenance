# GR05 glossary — explain the project in plain language

| Term | Meaning in this project |
|---|---|
| Predictive maintenance | Using condition/history information to support estimates of future maintenance needs; no operational maintenance policy is deployed here |
| Reactive / preventive maintenance | Responding after faults / intervening on a planned schedule |
| Diagnosis / prognosis | Assessing present condition / estimating future evolution or remaining life |
| RUL | Remaining Useful Life, measured here in flight cycles until simulated end-of-life |
| Regression | Predicting a numerical value such as RUL, rather than choosing a fault class |
| Raw reading | One ordered sensor/operating snapshot inside a flight |
| Flight / cycle | One mission containing many readings; cycle is its index within a history |
| Engine / unit | Identifier for a source history, scoped to the dataset; cross-subset independence is unproven |
| Prepared row | One completed flight with features available at flight end |
| HDF5 | A container of named arrays and metadata; the source format of DS01/DS02 |
| N-CMAPSS | The simulated run-to-failure collection driven by realistic flight profiles; not the original 2008 benchmark |
| DS01 / DS02 | Two subsets of N-CMAPSS; not the original and new dataset respectively |
| W | Operating conditions: altitude, Mach, throttle and inlet temperature |
| X_s | Simulator channels representing physically measured sensor quantities |
| X_v / T | Virtual signals / hidden simulator health modifiers; excluded from our sensor-based inputs |
| A / Y | Auxiliary metadata / true historical RUL label |
| X / y | Inputs a future model may see / the target answer stored separately |
| T48 | Total temperature at the high-pressure turbine outlet; converted to Kelvin in preparation |
| Nc / Nf / Wf | Physical core speed / fan speed / fuel flow |
| P2 | Total pressure at fan inlet, psia, confirmed by journal Table 5 |
| LPC / HPC | Low-pressure / high-pressure compressor |
| HPT / LPT | High-pressure / low-pressure turbine |
| Rankine (°R) / Kelvin (K) | Absolute-temperature scales; K = °R × 5/9. Neither is Celsius |
| psia / kPa / rpm | Absolute pressure in pounds per square inch / kilopascals / rotations per minute |
| Feature engineering | Turning valid available measurements into explicit summaries, differences or ratios |
| Mean / standard deviation | Typical numerical level / spread; flight spreads use sample ddof 1 |
| Previous-flight difference | Current mean minus previous mean; undefined on the first observed flight |
| Causal trailing feature | A summary using current/earlier observations only; it does not imply causal scientific inference |
| Imputation | Filling missing predictor values using learned training-set rules; never filling target labels |
| Standardization | Subtracting a training mean and dividing by a training scale; not operating-regime correction |
| One-hot encoding | Turning a category such as DS01/DS02 into separate indicator columns |
| Nominal / ordinal | Labels without inherent order / ordered categories without equal numerical gaps |
| Interval / ratio scale | Meaningful differences / meaningful differences and ratios with a true zero |
| Discrete / continuous | Countable values / values on a continuous measurement scale; separate from measurement scale |
| Data leakage | Giving training or preparation information unavailable at prediction or evaluation time |
| Train / validation / test | Fit parameters / develop or compare choices / final held-out evaluation |
| Conservative group | Equal raw unit IDs linked across subsets for split safety, without proving physical identity |
| Quarantine | Retained data excluded from modeling due to a possible related test history |
| Pearson correlation r | Linear association from −1 to +1; not proof of causation or forecasting skill |
| Retrospective stage | A historical group formed using known true RUL; never an available model input |
| Confounding / regime shift | Other factors can explain an association / held-out operating conditions differ from training |
| MAE / RMSE | Average absolute cycle error / square root of mean squared cycle error; model evaluation is later work |
| Macro average | An average giving each engine equal weight, rather than each flight/reading |
| Baseline | A simple reference such as a constant training mean/median, to justify model complexity |
| Linear regression | A proposed weighted-sum model; not fitted yet |
| Random forest | A proposed average of randomized regression trees; not fitted yet |
| CRISP-DM | Business understanding, data understanding, preparation, modeling, evaluation and practical implications |
| Manifest / SHA-256 | A record of version inputs/artifacts / a content hash identifying exact file bytes, not proving upstream authenticity |

For physical definitions see [references](references.md); for actual measured results use the Task 3–5 reports rather than these definitions.
