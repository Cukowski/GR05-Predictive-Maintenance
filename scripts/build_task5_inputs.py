"""Rebuild tracked Task 5 means/history CSV from audited Task 3 exports."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from src.descriptive_analysis import reconstruct_flights
if __name__=='__main__':print('Reconstructed',len(reconstruct_flights(ROOT)),'flight rows; within-flight variances are not reconstructed.')
