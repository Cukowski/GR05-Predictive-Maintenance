# Task 2 — Data Inventory & Access Report

**Dataset:** NASA N-CMAPSS · Turbofan Engine Degradation Simulation Data Set 2<br>
**Updated:** 11 November 2026 · V6 progress evidence.<br>
**Status:** Local source files, format, access steps, volume, relevance and constraints documented; current public source metadata checked. Original download receipt/version match and upstream checksum comparison remain explicitly unverified.

## Sources and access

| Source / item | Role | Access / evidence |
|---|---|---|
| NASA Prognostics Center of Excellence | Original dataset provider | [NASA repository](https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/) |
| Arias Chao et al. (2021), Data 6(1), 5 | Scientific description and variable definitions | [Journal paper](https://doi.org/10.3390/data6010005) |
| Kaggle: `bishals098/nasa-cmapss-2-engine-degradation` | Team-reported acquisition source | [Dataset page](https://www.kaggle.com/datasets/bishals098/nasa-cmapss-2-engine-degradation) |
| Public Kaggle metadata view | Current source version/license label, checked 11 November | [Metadata endpoint](https://www.kaggle.com/api/v1/datasets/view/bishals098/nasa-cmapss-2-engine-degradation); [compact recorded snapshot](../reports/results/source_metadata.json) |
| Local April 2020 preprint and example notebook | Supporting reference material, focused on DS02 | `data/` root; local-only, not Git-tracked |
| Lecturer PDFs/slides/example | Course requirements and measurement-scale guidance | `tasks/`; local-only, not Git-tracked |

Use your own Kaggle access to download the selected HDF5 files, extract them into `data/raw/`, and follow [data/README.md](../data/README.md). Credentials, archives and large raw arrays must not be committed. The project scripts need no internet to analyse existing local files.

## Version and license provenance

The public Kaggle metadata currently reports **version 1**, last updated **10 August 2025**, with license label **U.S. Government Works**. The journal explicitly declares the **dataset CC0 1.0**. These source statements are recorded separately; they are not silently treated as the same license or as a legal conclusion.

The local files are identified by their exact byte sizes and SHA-256 below. Current online version metadata does not prove the original downloaded files came from that version. No original download receipt or upstream checksum match has been established. These are provenance limitations, not missing values in the measurement arrays. Citation and source links are preserved; no raw data or third-party course materials are published here.

## Exact local files

| File | Bytes | Local SHA-256 |
|---|---|---|
| `N-CMAPSS_DS01-005.h5` | 2873351432 | `3abdcee2a3c8136e8880e5d43ac8cdf12ab9f7f3ab37145f23b24c11335afbed` |
| `N-CMAPSS_DS02-006.h5` | 2450472504 | `47971a68b239ecb756833218a95d68ded6eb7e63ee84e86671c8b188de1ca765` |

Combined local size: approximately **4.958 GiB**. The two accompanying source files are `Run_to_Failure_Simulation_Under_Real_Flight_Conditions_Dataset.pdf` and `N-CMAPSS_Example_data_loading_and_exploration.ipynb`; they are reference documents, not additional independent measurement datasets.

## Verified structure and volume

HDF5 contains named arrays, not a single flat CSV. Each file has development and test arrays for W, X_s, X_v, T, Y and A, plus column-name metadata. Numeric arrays align row-for-row within the same file/partition.

| Subset / supplied partition | Readings | Source histories | Engine-flight pairs |
|---|---:|---:|---:|
| DS01 development | 4906636 | 6 | 553 |
| DS01 test | 2735232 | 4 | 341 |
| DS02 development | 5263447 | 6 | 446 |
| DS02 test | 1253743 | 3 | 202 |
| Total | 14159058 | 19 | 1542 |

These are dataset-scoped histories, not proof of 19 independent physical engines. There are **47 numeric fields**: operating conditions W (4), measured sensor channels X_s (14), virtual channels X_v (14), hidden simulator health modifiers T (10), RUL Y (1), auxiliary metadata A (4). RUL is in flight cycles. No explicit timestamp column is present.

`unit`, `cycle`, `Fc` and `hs` are stored as float64 but have identifier/index/category meanings. The [feature table](../reports/results/feature_description_table.csv), [Task 3 report](05-data-understanding.md) and notebook explain each variable, unit and scale.

**Source correction:** P2 is total pressure at fan inlet, psia, confirmed from journal Table 5 on 11 November. The older local preprint omitted it. The Task 4 representation still excludes P2 to keep the selected 17-channel baseline representation stable; definition confirmation does not silently add a feature to a prior version.

## Relevance, constraints and risks

- RUL labels and complete simulated histories support a supervised regression study.
- Real flight profiles drive simulated degradation/responses; actual engine failures or operational validation are not claimed.
- DS02 development covers long-flight class 3, whereas test also covers shorter classes: this is an operating-regime generalization challenge.
- Engine IDs recur across subsets. Preparation groups equal IDs conservatively and quarantines DS02 development unit 10 because that ID is supplied test in DS01.
- RUL, final lifetime, future flights and hidden health information must not enter predictors.
- Chunked reads avoid loading all raw arrays at once; local environment, cache and disk throughput influence runtime. No fixed minimum-RAM guarantee is asserted.
- Whole-flight aggregates lose transient detail. Sampled diagnostic quantiles/duplicates do not prove exact population properties or physical accuracy.

## Acquisition-to-preparation workflow

1. Download the two selected files and retain their source/version receipt if available.
2. Place them under `data/raw/`; compare byte sizes and local hashes before reproducing analysis.
3. Install the pinned project environment and execute Task 3 to inspect arrays/quality.
4. Execute Task 4 to generate immutable local version directories with X inputs, y labels, identity rows and fitted preprocessing.
5. Execute Task 5 for source-labelled descriptive analysis; its default tracked reconstruction does not reprocess raw HDF5 or restore within-flight variance.
6. Use [the current preparation manifest](../reports/results/task4/manifest.json), not an arbitrary local directory, to locate the active version.

Evidence: [Task 3 audit](05-data-understanding.md), [Task 4 preparation](06-data-preparation.md), [Task 5 analysis](07-task5-descriptive-analysis.md), [decision log](decisions.md) and [project checker](../scripts/check_project.py).
