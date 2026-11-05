# Task 5 — Initial Descriptive Analysis

**Project research question:** How accurately can classical regression models estimate engine Remaining Useful Life (RUL) from sensor data compared with a simple baseline?

## Current status (5 November 2026)

The analysis notebook has been added on the Task 5 branch. Two SVG visualizations were generated from the *already tracked* Task 3 engine-summary CSV. **The flight-level sensor charts have not yet been executed**, because the full Task 4 prepared dataset is intentionally local and excluded from Git. No sensor–RUL conclusions, regression results, MAE/RMSE, or measured maintenance savings are claimed.

## Run the analysis

1. Check out `task5/descriptive-analysis` and activate the project Python environment.
2. Ensure `reports/results/task4/manifest.json` points to the local prepared data version. If the corresponding `data/processed/<version_id>/flights_features.csv` is absent, run `python scripts/prepare_data.py` with the raw HDF5 files installed according to `data/README.md`.
3. Launch Jupyter from repository root and execute `notebooks/03-descriptive-analysis.ipynb` top-to-bottom.
4. Inspect exported SVGs in `reports/figures/task5/` and CSV evidence in `reports/results/task5/`, and review H1–H4 with both team members before reporting any finding.
5. Add a descriptive report, dashboard, key-insights summary and storytelling slide from *measured* outputs rather than guessed chart narratives.

## Visuals

| Figure | Basis | Status |
| --- | --- | --- |
| `engine_lifetimes.svg` | `reports/results/engines.csv` (Task 3) | Generated and committed |
| `healthy_cycles.svg` | `reports/results/engines.csv` (Task 3) | Generated and committed |
| `01_train_rul_histogram.svg` | Prepared Task 4 training flights | Generated on notebook execution |
| `02_sensor_trajectories.svg` | Prepared Task 4 training flights | Generated on notebook execution |
| `03_train_correlation_heatmap.svg` | Prepared Task 4 training flights | Generated on notebook execution |
| `04_life_stage_sensor_boxplots.svg` | Prepared Task 4 training flights | Generated on notebook execution |
| `05_operating_conditions.svg` | Prepared Task 4 training flights | Generated on notebook execution |
| `06_previous_flight_changes.svg` | Prepared Task 4 training flights | Generated on notebook execution |

**Note:** The two tracked Task 3-derived charts display all known historical engine summaries, including pre-existing test partition summaries. They should be used only to describe dataset structure. The new notebook deliberately develops sensor hypotheses on training histories and uses validation histories only for checking pre-specified associations. It does not access test or quarantine flights for hypothesis development.

## Analyses corresponding to lecturer's Task 5 criteria

- **Descriptive statistics:** flight-level distributions, train-engine counts, RUL ranges.
- **Trends/patterns:** flight-cycle sensor trajectories, correlations and previous-flight changes.
- **Hypotheses:** H1 sensor–RUL association; H2 historical changes; H3 operating-context effects; H4 engine and dataset heterogeneity.
- **Segmentation:** retrospective RUL buckets (0–20, 21–50, >50 cycles), with engine-level medians and operating-condition comparisons; these labels are not available for deployment.
- **Business story:** identify candidate measurements for further assessment, note mission-profile confounding and generalization limitations, then motivate later grouped baseline-versus-regression comparisons.

## Methodological limitations

The dataset contains real flight-condition profiles with **simulated** degradation and sensor responses. Within-engine flight observations are not independent. Dataset-scoped engine IDs may be related across subsets, hence the existing split quarantine. Whole-flight means mix operating phases. Changes or correlations should not be equated with causality, model accuracy or operational aviation safety. No baseline/regression models are trained in Task 5.

**Sources:** [Task 3](05-data-understanding.md), [Task 4](06-data-preparation.md), [Task 4 manifest](../reports/results/task4/manifest.json), [Task 5 notebook](../notebooks/03-descriptive-analysis.ipynb).
