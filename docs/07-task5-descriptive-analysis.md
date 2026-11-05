# Task 5 — Initial Descriptive Analysis

**Project research question:** How accurately can classical regression models estimate engine Remaining Useful Life (RUL) from sensor data compared with a simple baseline?

## Data sources and provenance

This descriptive analysis uses information from **the processed engine-cycle CSV in our GitHub repository** and the **NASA N-CMAPSS engine degradation datasets made available through Kaggle**. These are related stages of the same source-data pipeline, **not two independent datasets pooled together**.

1. **Original data — Kaggle NASA N-CMAPSS datasets:** The team acquired `N-CMAPSS_DS01-005.h5` (DS01) and `N-CMAPSS_DS02-006.h5` (DS02) through the [Kaggle NASA C-MAPSS 2 engine degradation dataset](https://www.kaggle.com/datasets/bishals098/nasa-cmapss-2-engine-degradation). These HDF5 files contain engine flight profiles, sensor values and RUL labels. The original files are retained locally under `data/raw/` and are deliberately excluded from Git because of their size.
2. **Processed cycle-level CSV — GitHub:** `reports/results/cycles.csv` was generated during Task 3 from the original DS01 and DS02 HDF5 data. It summarizes measurements for individual engine flight cycles, including flight conditions, sensor readings and RUL.
3. **Task 5 feature CSV — GitHub:** `reports/results/task5/flights_features_from_cycles.csv` was reconstructed from `reports/results/cycles.csv` and the Task 4 engine-split definitions. It contains flight-level features such as average sensor readings, historical changes, engineered ratios, engine identifiers and train/validation/test split labels.
4. **Full Task 4 prepared data — local alternative:** `data/processed/<version_id>/flights_features.csv` is created by the full Task 4 pipeline from the HDF5 files. It is excluded from Git and contains more features than the reconstructed Task 5 CSV. The Task 5 notebook currently expects this full local version.

**Data lineage:** Kaggle-hosted N-CMAPSS DS01/DS02 HDF5 → Task 3 processing → `reports/results/cycles.csv` → reconstructed `reports/results/task5/flights_features_from_cycles.csv` → available flight-level descriptive inputs. Separately, the full Task 4 pipeline generates the local `data/processed/` feature set. **The reconstructed CSV is based on Kaggle-originated data, but its construction does not constitute a new download or reprocessing of the raw Kaggle files.**

## Current status (5 November 2026)

The Task 5 branch contains the third notebook, `notebooks/03-descriptive-analysis.ipynb`, and two committed structural SVG figures. The reconstructed flight-feature CSV from the processed cycle-level data is also committed. **The six sensor-specific flight-level charts have not yet been generated and committed from the Task 5 notebook**: its input code still reads the full local Task 4 prepared CSV, which is not tracked on GitHub. Do not report those visualizations as completed until they have been executed and checked against an available source.

The tracked reconstructed CSV contains **1,542 engine-flight records**: 574 training, 343 validation, 543 test and 82 quarantined test-related flights. The intended hypothesis-building analysis uses the **training partition only**. No regression results, MAE/RMSE estimates or measured maintenance savings are claimed in Task 5.

## Run the analysis

1. Check out `task5/descriptive-analysis` and activate the project's Python environment.
2. For the **full Task 4 feature set**, use the Kaggle-sourced DS01/DS02 HDF5 files in `data/raw/` and run `python scripts/prepare_data.py` as described in [data/README.md](../data/README.md). Confirm that the generated `data/processed/<version_id>/flights_features.csv` matches [the Task 4 manifest](../reports/results/task4/manifest.json).
3. The **tracked alternative** `reports/results/task5/flights_features_from_cycles.csv` can support descriptive calculations on the fields it includes. Using it with the existing third notebook requires changing the notebook input path or adding a documented fallback; it is not a drop-in replacement for all Task 4 features.
4. Run `notebooks/03-descriptive-analysis.ipynb` from the repository root once its expected data source is available. Review the resulting SVG figures in `reports/figures/task5/` and CSV statistics in `reports/results/task5/`.
5. Record numerical findings, caveats, a dashboard or slide and a concise business interpretation **only after checking the executed results**. Clearly identify whether each figure came from the full Task 4 dataset or the reconstructed cycle-level CSV.

## Visuals

| Figure | Source | Status |
| --- | --- | --- |
| `engine_lifetimes.svg` | `reports/results/engines.csv`, derived from Kaggle-originated DS01/DS02 data in Task 3 | Generated and committed |
| `healthy_cycles.svg` | `reports/results/engines.csv` (Task 3) | Generated and committed |
| `01_train_rul_histogram.svg` | Training flight features from the Kaggle-originated, processed cycle data or full local Task 4 features | Pending notebook execution |
| `02_sensor_trajectories.svg` | Same training source | Pending notebook execution |
| `03_train_correlation_heatmap.svg` | Same training source | Pending notebook execution |
| `04_life_stage_sensor_boxplots.svg` | Same training source | Pending notebook execution |
| `05_operating_conditions.svg` | Same training source | Pending notebook execution |
| `06_previous_flight_changes.svg` | Same training source | Pending notebook execution |

**Partition safeguards:** The two existing Task 3 engine-summary charts describe the overall dataset structure and may include historical test-partition summaries; they should not be used to choose predictive features. The Task 5 notebook develops sensor hypotheses from training histories and uses validation histories only for pre-specified descriptive checks. Test and quarantine histories must not be used for hypothesis development.

## Analyses corresponding to the lecturer's Task 5 criteria

- **Descriptive statistics:** distributions of flight-level variables, training-engine counts and historical RUL ranges.
- **Trends and patterns:** per-engine flight-cycle sensor trajectories, correlations with RUL and previous-flight changes.
- **Hypotheses:** H1 sensor–RUL association; H2 historical changes; H3 operating-context effects; H4 engine and dataset heterogeneity.
- **Segmentation:** retrospective RUL groups (0–20, 21–50 and >50 cycles) with engine-level median comparisons. These groups are for analysis only and are **not available as deployment features**.
- **Business story:** use measured results to identify candidate sensor measurements and explain the implications and limits for predictive maintenance ahead of the later baseline-versus-regression comparison.

## Methodological limitations

The Kaggle-hosted N-CMAPSS data combines real flight-condition profiles with **simulated** engine degradation and sensor responses. Flight observations within the same engine are dependent, and operating conditions can confound relationships with RUL. A whole-flight mean also blends different phases of flight.

The processed cycle CSV and its reconstructed feature CSV do **not** preserve all the original high-frequency measurements or every feature generated by the full Task 4 processing pipeline. Conclusions based on these summaries must not be described as findings obtained by re-running the complete Kaggle HDF5 analysis. Correlation is not causation or proof of predictive accuracy or operational aviation suitability. No baseline or regression model is trained in Task 5.

**Sources:** [Kaggle data source](https://www.kaggle.com/datasets/bishals098/nasa-cmapss-2-engine-degradation), [data acquisition and processing](../data/README.md), [Task 3](05-data-understanding.md), [Task 4](06-data-preparation.md), [processed cycle CSV](../reports/results/cycles.csv), [reconstructed Task 5 feature CSV](../reports/results/task5/flights_features_from_cycles.csv), [Task 4 manifest](../reports/results/task4/manifest.json) and [Task 5 notebook](../notebooks/03-descriptive-analysis.ipynb).
