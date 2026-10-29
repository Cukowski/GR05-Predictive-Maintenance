# Local data and source references

Place the exact HDF5 files here (ignored by Git):

```text
data/
├── README.md
├── raw/
│   ├── N-CMAPSS_DS01-005.h5
│   └── N-CMAPSS_DS02-006.h5
├── N-CMAPSS_Example_data_loading_and_exploration.ipynb
└── Run_to_Failure_Simulation_Under_Real_Flight_Conditions_Dataset.pdf
```

The two files at `data/` root are locally supplied reference material from Kaggle. The PDF is a seven-page April 2020 preprint focused on DS02; the example notebook is credited to Manuel Arias. They are not required to execute our notebook and have not been modified. Do not run or commit the supplied example simply to reproduce our analysis.

Acquisition source reported by the team: [Kaggle N-CMAPSS redistribution](https://www.kaggle.com/datasets/bishals098/nasa-cmapss-2-engine-degradation). Download through your own account under the applicable terms; select DS01-005 and DS02-006 and extract them into `data/raw/`. No credentials belong in this repository. Record the download date, dataset version identifier, and redistribution terms when confirmed. An upstream checksum comparison has not been performed.

| File | Bytes | Local SHA-256 |
|---|---|---|
| N-CMAPSS_DS01-005.h5 | 2873351432 | `3abdcee2a3c8136e8880e5d43ac8cdf12ab9f7f3ab37145f23b24c11335afbed` |
| N-CMAPSS_DS02-006.h5 | 2450472504 | `47971a68b239ecb756833218a95d68ded6eb7e63ee84e86671c8b188de1ca765` |

Hashes identify local bytes, not source authenticity or licensing. These files require approximately 4.958 GiB of disk space. The notebook scans them in 100,000-row chunks and retains small engine-flight summaries and diagnostic samples. Allow additional room for the virtual environment and notebook outputs. Available hardware, filesystem cache, and Jupyter overhead affect runtime/memory; no fixed minimum RAM or runtime is asserted.

Run [the Task 3 notebook](../notebooks/01-data-understanding.ipynb) using the [repository setup](../README.md). It opens HDF5 read-only and exports small evidence tables to `reports/results/` and SVGs to `reports/figures/`. Large raw data remains excluded from Git. `data/processed/` now contains Task 4 version directories and is also ignored.

## Prepared versions (Task 4)

Run `python scripts/prepare_data.py` from the repository root or execute [notebooks/02-preprocessing.ipynb](../notebooks/02-preprocessing.ipynb). The active version ID and exact local path are recorded in [the preparation manifest](../reports/results/task4/manifest.json). Each directory contains `flights_features.csv`, finite `X_*.csv` inputs, unchanged RUL `y_*.csv` targets, matching `rows_*.csv` metadata, quarantine rows, fitted preprocessing, and artifact hashes. See the [Task 4 report](../docs/06-data-preparation.md).

Raw hashes plus configuration, code and package versions identify each prepared version. Existing matching output files are verified before reuse; altered inputs create a new directory. Raw files are never overwritten. Earlier local prepared versions may coexist and remain ignored; select the version named by the current manifest rather than choosing an arbitrary directory.
