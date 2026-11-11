"""Test descriptive evidence reconstruction and partition safeguards."""
from pathlib import Path
import json,unittest
import numpy as np
import pandas as pd
from src.descriptive_analysis import training_insights,load_flights

ROOT=Path(__file__).resolve().parents[1]

class DescriptiveTests(unittest.TestCase):
 def test_insights_reject_validation_or_test_rows(self):
  for label in ['validation','test','quarantine_test_related']:
   with self.assertRaises(ValueError):training_insights(pd.DataFrame({'split':[label]}))

 def test_tracked_reconstruction_preserves_held_out_groups_and_measurements(self):
  # Source exports, not raw HDF5, make this check possible in a fresh clone.
  rows,provenance=load_flights(ROOT,'reconstructed')
  self.assertEqual(len(rows),1542)
  self.assertEqual((rows.split=='train').sum(),574)
  self.assertEqual((rows.split=='quarantine_test_related').sum(),82)
  active=rows[rows.split!='quarantine_test_related']
  self.assertTrue((active.groupby('conservative_group').split.nunique()==1).all())
  cycles=pd.read_csv(ROOT/'reports/results/cycles.csv')
  check=rows.merge(cycles,on=['dataset','unit','cycle'],validate='one_to_one')
  np.testing.assert_allclose(check.T48_K_mean,check.T48_mean*5/9)
  self.assertTrue((check.RUL==check.RUL_min).all())
  train=rows[rows.split=='train']
  result=training_insights(train)
  self.assertEqual(result['t48_negative_histories'],7)
  self.assertEqual(result['conservative_groups'],6)
  self.assertTrue(all(n==567 for n in result['delta_nonmissing_counts'].values()))
  self.assertGreater(result['late_minus_early_T48_K_median'],0)
  self.assertNotIn('T48_K_std',rows)
  self.assertIn('not full Task 4 variances',provenance['description'])

if __name__=='__main__':unittest.main()
