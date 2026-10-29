"""Build or verify a local versioned Task 4 dataset: python scripts/prepare_data.py."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.preprocessing import prepare_data

if __name__=='__main__':
    directory,manifest=prepare_data(ROOT)
    print('Local dataset:',directory.relative_to(ROOT))
    print('Matrices:',manifest['matrix_shapes'])
    print('Quarantined flights:',manifest['quarantined_flights'])
