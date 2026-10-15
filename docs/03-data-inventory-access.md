# Task 2 — Data Inventory & Access Report (Draft)

**Dataset:** NASA N-CMAPSS — Turbofan Engine Degradation Simulation Data Set 2\
**Current status:** Paper reviewed; professor approved dataset; Kaggle package contents, download size, and environment requirements NOT YET verified.

## Dataset provenance
- **Primary scientific description:** Arias Chao et al. (2021), https://doi.org/10.3390/data6010005
- **Original provider:** NASA Prognostics Center of Excellence, https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/
- **Proposed access:** Kaggle redistribution, https://www.kaggle.com/datasets/bishals098/nasa-cmapss-2-engine-degradation
- **Important distinction:** Confirm Kaggle files correspond to the N-CMAPSS **dataset 2**, rather than original 2008 C-MAPSS, and that they contain the expected fields and partitions.
- **Paper's dataset license:** CC0 1.0, per the paper. Verify any separate rights/conditions for the Kaggle redistribution.

## What the paper describes (not yet independently verified in downloaded Kaggle files)
- **Format:** HDF5 (`.h5`), one file per dataset group in the source; DS08 split across multiple files.
- **Groups:** DS01–DS08; 128 simulated units across groups, seven degradation/failure modes.
- **DS01:** 10 units, one failure mode, three flight classes and approximately 7.6 million measurement records (not a file size in MB).
- **Development/test arrays:** `W_dev`, `X_s_dev`, `X_v_dev`, `T_dev`, `Y_dev`, `A_dev` and corresponding `_test` variables.
- **Scenario descriptors:** altitude (`alt`), Mach number (`Mach`), throttle-resolver angle (`TRA`), fan-inlet temperature (`T2`).
- **Measured sensors:** 14 signals including fuel flow (`Wf`), fan/core speeds (`Nf`, `Nc`), temperature (`T24`, `T30`, `T48`, `T50`), and pressures.
- **Target:** `Y_dev` / `Y_test` — RUL in **flight cycles**.
- **Auxiliary data:** engine unit, cycle, flight class and health state.
- **Other available quantities:** virtual sensors (`X_v_*`) and underlying simulator health parameters (`T_*`); avoid treating them as available real-world inputs without justification.

## Planned access and validation steps
1. Download the selected Kaggle archive with browser or Kaggle CLI under an authenticated account, observing terms of use.
2. List exact filenames and sizes; compare against the original paper's HDF5 structure.
3. Verify DS01 development/test partitions, unit IDs, RUL labels and variable metadata.
4. Record bytes, number of observations, units, cycles, nulls, and columns. Confirm available RAM/storage.
5. Load a **small subset first**, inspecting sensor trajectories and RUL on a per-engine basis.
6. Save reproducible download instructions, dependencies and source version; do not commit gigabytes of raw data to GitHub.
7. Choose an evaluation protocol that separates engines and respects provided partitions.

## Constraints and risks
- High-volume time-series data; memory and disk needs are currently unknown for the Kaggle copy.
- Small number of independent DS01 engine units limits holdout sample diversity.
- Data from real flight operating profiles, but engine degradation and measurements are simulated.
- Model-data leakage if training uses RUL label, future cycles or simulator-only health information.
- Dataset licenses and Kaggle metadata must be checked at download time.

## Verification checklist
- [ ] Kaggle downloaded and exact archive contents logged.
- [ ] Source/version and redistribution rights verified.
- [ ] Expected HDF5 groups, units and RUL confirmed.
- [ ] File sizes, record counts, column inventory recorded.
- [ ] Feasibility run completed on DS01.
- [ ] Data access and reproducibility instructions finalized.

## Source
Arias Chao, M., Kulkarni, C., Goebel, K., & Fink, O. (2021), *Aircraft Engine Run-to-Failure Dataset under Real Flight Conditions for Prognostics and Diagnostics*, Data 6(1), 5. https://doi.org/10.3390/data6010005. See Tables 2–8.
