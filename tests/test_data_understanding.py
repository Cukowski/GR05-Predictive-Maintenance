"""Numerical and boundary checks for the full-scan audit; no raw data required."""
from pathlib import Path
import tempfile
import unittest
import numpy as np
import h5py
from src.data_understanding import scan_file, engine_summary, consistency_report, measurement_scale

NAMES = {'A':['unit','cycle','Fc','hs'], 'W':['alt','Mach','TRA','T2'],
         'X_s':['T24','T30','T48','T50','P15','P2','P21','P24','Ps30','P40','P50','Nf','Nc','Wf'],
         'X_v':['T40','P30','P45','W21','W22','W25','W31','W32','W48','W50','SmFan','SmLPC','SmHPC','phi'],
         'T':['fan_eff_mod','fan_flow_mod','LPC_eff_mod','LPC_flow_mod','HPC_eff_mod','HPC_flow_mod','HPT_eff_mod','HPT_flow_mod','LPT_eff_mod','LPT_flow_mod']}

class AuditTests(unittest.TestCase):
    def test_chunked_scan_matches_direct_statistics_and_preserves_flights(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'N-CMAPSS_DS01-TEST.h5'
            reference={}
            with h5py.File(path,'w') as f:
                for g,names in NAMES.items(): f[g+'_var']=np.array(names,dtype='S20')
                for part,unit in [('dev',1),('test',2)]:
                    # Eight observations, two cycles. An exact duplicate straddles
                    # the 3-row chunk boundary (indices 2 and 3).
                    for g,names in NAMES.items():
                        x=np.arange(8*len(names),dtype=float).reshape(8,-1)+100
                        if g=='A': x=np.array([[unit,1,1,1]]*4+[[unit,2,1,0]]*4,dtype=float)
                        else: x[3]=x[2]
                        if g=='W': x[0,0]=np.nan; x[7,1]=np.inf
                        f[g+'_'+part]=x
                        reference[part,g]=x
                    f['Y_'+part]=np.array([[1]]*4+[[0]]*4,dtype=np.int64)
            result=scan_file(path,chunk_rows=3,sample_rows=8)
            for part in ['dev','test']:
                rows=result['stats'][(result['stats'].partition==part)&(result['stats'].group=='W')]
                direct=reference[part,'W'].copy(); direct[~np.isfinite(direct)]=np.nan
                np.testing.assert_allclose(rows['mean'],np.nanmean(direct,axis=0))
                np.testing.assert_allclose(rows['std'],np.nanstd(direct,axis=0,ddof=1))
            self.assertEqual(result['stats'].missing.sum(),2)
            self.assertEqual(result['stats'].infinite.sum(),2)
            self.assertEqual(result['checks'].adjacent_exact_duplicates.tolist(),[1,1])
            self.assertEqual(result['checks'].sample_exact_duplicates.tolist(),[1,1])
            self.assertEqual(len(result['cycles']),4)
            self.assertEqual(engine_summary(result['cycles']).cycles.tolist(),[2,2])
            self.assertEqual(consistency_report(result['cycles']).rul_formula_violations.sum(),0)
            self.assertEqual(result['cycles'].readings.tolist(),[4,4,4,4])

    def test_scales_use_semantics_instead_of_storage_or_uniqueness(self):
        expected={'unit':'Nominal','hs':'Nominal','Fc':'Ordinal','cycle':'Interval',
                  'RUL':'Ratio','T2':'Ratio','alt':'Interval','P2':'Unconfirmed'}
        for name,scale in expected.items():
            self.assertEqual(measurement_scale(name,'A')['scale'],scale)
        self.assertEqual(measurement_scale('RUL','Y')['variability'],'discrete')
        self.assertEqual(measurement_scale('T2','W')['variability'],'continuous')

if __name__=='__main__': unittest.main()
