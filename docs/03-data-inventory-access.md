# Task 2 — Data Inventory & Access Report (Draft)

**Dataset:** NASA N-CMAPSS — Turbofan Engine Degradation Simulation Data Set 2\
**Current status (22 October 2026):** DS01 and DS02 acquired locally and fully scanned. File sizes, HDF5 structure, units, labels, and environment are recorded in the [Task 3 report](05-data-understanding.md) and [data access guide](../data/README.md). Upstream version and Kaggle redistribution terms remain unverified. The planned steps below are retained as the original access plan.

## Dataset provenance
- **Primary scientific description:** Arias Chao et al. (2021), https://doi.org/10.3390/data6010005
- **Original provider:** NASA Prognostics Center of Excellence, https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/
- **Acquisition source reported by the team:** Kaggle redistribution, https://www.kaggle.com/datasets/bishals098/nasa-cmapss-2-engine-degradation
- **Important distinction:** Confirm Kaggle files correspond to the N-CMAPSS **dataset 2**, rather than original 2008 C-MAPSS, and that they contain the expected fields and partitions.
- **Paper's dataset license:** CC0 1.0, per the paper. Verify any separate rights/conditions for the Kaggle redistribution.

## Original paper-based expectations (local verification now in Task 3)
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
- High-volume time-series data; the two local HDF5 files occupy approximately 4.958 GiB. Chunked processing avoids loading all arrays at once; exact file sizes are in the Task 3 report.
- Small number of independent DS01 engine units limits holdout sample diversity.
- Data from real flight operating profiles, but engine degradation and measurements are simulated.
- Model-data leakage if training uses RUL label, future cycles or simulator-only health information.
- Dataset licenses and Kaggle metadata must be checked at download time.

## Verification checklist
- [x] Local DS01/DS02 files acquired; exact filenames, byte sizes, and SHA-256 hashes recorded (archive/version metadata still open).
- [ ] Source/version and redistribution rights verified.
- [x] Expected HDF5 arrays, units and RUL confirmed for the two local files.
- [x] File sizes, record counts, and full feature inventory recorded.
- [x] Full read-only scans and descriptive feasibility runs completed on DS01 and DS02.
- [x] Local file placement, environment, and rerun instructions documented; source rights/version follow-up remains open.

## Source
Arias Chao, M., Kulkarni, C., Goebel, K., & Fink, O. (2021), *Aircraft Engine Run-to-Failure Dataset under Real Flight Conditions for Prognostics and Diagnostics*, Data 6(1), 5. https://doi.org/10.3390/data6010005. See Tables 2–8.
