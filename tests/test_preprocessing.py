"""Leakage, data-cleaning and causal feature tests; no large raw data required."""
from pathlib import Path
import tempfile
import unittest
import json
import h5py
import numpy as np
import pandas as pd
from src.preprocessing import (CHANNELS,aggregate_file,engineer_features,assign_splits,
                               make_preprocessor,feature_catalog,sha256,verify_version)


def flight_fixture():
    rows=[]
    for ds,unit in [('DS01',1),('DS02',2)]:
        for cycle in [1,2,3,4]:
            row=dict(dataset=ds,source_partition='dev',unit=unit,cycle=cycle,
                     flight_class=1,RUL=4-cycle,n_readings=10)
            for stem,_,_ in CHANNELS.values():
                row[stem+'_mean']=float(cycle+unit+10)
                row[stem+'_std']=1.
            rows.append(row)
    return pd.DataFrame(rows)


class PreprocessingTests(unittest.TestCase):
    def test_future_changes_cannot_change_earlier_features_or_cross_engine_history(self):
        original=flight_fixture()
        before=engineer_features(original)
        changed=original.copy()
        changed.loc[(changed.dataset=='DS01')&(changed.cycle==4),'T48_K_mean']=99999
        after=engineer_features(changed)
        pd.testing.assert_frame_equal(before[before.cycle<4],after[after.cycle<4])
        self.assertTrue(before.loc[before.cycle==1,'T48_K_delta_prev'].isna().all())
        self.assertEqual(before.loc[(before.dataset=='DS01')&(before.cycle==3),'T48_K_trailing3'].iloc[0],13.)

    def test_same_id_cannot_cross_splits_and_test_related_development_is_quarantined(self):
        f=flight_fixture()
        # DS01 test unit 10 and DS02 development unit 10 are linked conservatively.
        f.loc[f.dataset=='DS01','unit']=10
        f.loc[f.dataset=='DS01','source_partition']='test'
        f.loc[f.dataset=='DS02','unit']=10
        result=assign_splits(engineer_features(f),[5,6,18])
        self.assertEqual(set(result[result.dataset=='DS01'].split),{'test'})
        self.assertEqual(set(result[result.dataset=='DS02'].split),{'quarantine_test_related'})
        with self.assertRaises(ValueError):assign_splits(engineer_features(f),[10])

    def test_transform_is_fitted_on_training_only_and_unknown_categories_fail(self):
        train=pd.DataFrame({'a':[1.,3.,np.nan],'b':[10.,20.,30.], 'dataset':['DS01','DS02','DS01'],
                            'RUL':[500,400,300],'unit':[1,2,3]})
        pipe=make_preprocessor(['a','b']);pipe.fit(train)
        imp=pipe.named_transformers_['numeric'].named_steps['imputer']
        scale=pipe.named_transformers_['numeric'].named_steps['scaler']
        np.testing.assert_allclose(imp.statistics_,[2.,20.])
        medians=imp.statistics_.copy();means=scale.mean_.copy()
        validation=train.copy();validation['a']=[1e12,np.nan,-1e12]
        transformed=pipe.transform(validation)
        self.assertTrue(np.isfinite(transformed).all())
        np.testing.assert_array_equal(imp.statistics_,medians)
        np.testing.assert_array_equal(scale.mean_,means)
        self.assertFalse(any('RUL' in n or 'unit' in n for n in pipe.get_feature_names_out()))
        with self.assertRaises(ValueError):pipe.transform(train.assign(dataset='unknown'))

    def test_aggregation_matches_direct_units_and_std_across_chunk_boundaries(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'N-CMAPSS_DS01-TEST.h5'
            W=['alt','Mach','TRA','T2']
            X=['T24','T30','T48','T50','P15','P2','P21','P24','Ps30','P40','P50','Nf','Nc','Wf']
            with h5py.File(path,'w') as hdf:
                hdf['W_var']=np.array(W,dtype='S8');hdf['X_s_var']=np.array(X,dtype='S8')
                for part,unit in [('dev',1),('test',7)]:
                    hdf['A_'+part]=np.array([[unit,1,1,1]]*4+[[unit,2,1,0]]*4,dtype=float)
                    hdf['Y_'+part]=np.array([[1]]*4+[[0]]*4)
                    w=np.tile([100.,.5,50.,540.],(8,1));w[:,0]=[100,200,300,400,500,600,700,800]
                    x=np.full((8,len(X)),100.);x[0,X.index('T48')]=np.inf
                    hdf['W_'+part]=w;hdf['X_s_'+part]=x
            flights,audit=aggregate_file(path,chunk_rows=3)
            self.assertEqual(len(flights),4)
            np.testing.assert_allclose(flights.n_readings,[4,4,4,4])
            self.assertAlmostEqual(flights.iloc[0].alt_m_mean,250*.3048)
            self.assertAlmostEqual(flights.iloc[0].alt_m_std,np.std([100,200,300,400],ddof=1)*.3048)
            self.assertAlmostEqual(flights.iloc[0].T2_K_mean,300.)
            self.assertAlmostEqual(flights.iloc[0].T48_K_mean,100*5/9)
            self.assertEqual(audit.predictor_nonfinite.sum(),2)
            self.assertNotIn('P2_mean',flights)
            self.assertEqual(len(feature_catalog()),45)
            with h5py.File(path,'r+') as hdf:
                hdf['Y_dev'][0,0]=-1
            with self.assertRaises(ValueError):aggregate_file(path,chunk_rows=3)

    def test_existing_version_rejects_a_changed_artifact(self):
        with tempfile.TemporaryDirectory() as directory:
            folder=Path(directory)
            artifact=folder/'X_train.csv';artifact.write_text('feature\n1\n')
            manifest={'version_id':'test','artifacts':[{'file':artifact.name,'sha256':sha256(artifact)}]}
            (folder/'manifest.json').write_text(json.dumps(manifest))
            self.assertEqual(verify_version(folder)['version_id'],'test')
            artifact.write_text('feature\n999\n')
            with self.assertRaises(ValueError):verify_version(folder)

if __name__=='__main__':unittest.main()
