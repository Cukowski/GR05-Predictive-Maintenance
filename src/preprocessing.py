"""Task 4: read-only flight aggregation, causal features, and train-only transforms.

Run through scripts/prepare_data.py or notebooks/02-preprocessing.ipynb.
Raw arrays remain immutable. The persisted sklearn object is preprocessing, not
an RUL prediction model. Model-ready matrices and raw-derived rows stay ignored.
"""
from pathlib import Path
import hashlib
import importlib.metadata
import json
import platform
import shutil
import tempfile
from datetime import datetime
from zoneinfo import ZoneInfo
import h5py
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from src.data_understanding import column_names

# raw name -> output stem, physical unit, exact/declared conversion factor.
CHANNELS = {
    'alt': ('alt_m', 'm', 0.3048), 'Mach': ('Mach', 'dimensionless', 1.),
    'TRA': ('TRA_pct', '%', 1.), 'T2': ('T2_K', 'K', 5/9),
    'T24': ('T24_K', 'K', 5/9), 'T30': ('T30_K', 'K', 5/9),
    'T48': ('T48_K', 'K', 5/9), 'T50': ('T50_K', 'K', 5/9),
    'P15': ('P15_kPa', 'kPa', 6.894757293168),
    'P21': ('P21_kPa', 'kPa', 6.894757293168),
    'P24': ('P24_kPa', 'kPa', 6.894757293168),
    'Ps30': ('Ps30_kPa', 'kPa', 6.894757293168),
    'P40': ('P40_kPa', 'kPa', 6.894757293168),
    'P50': ('P50_kPa', 'kPa', 6.894757293168),
    'Nf': ('Nf_rpm', 'rpm', 1.), 'Nc': ('Nc_rpm', 'rpm', 1.),
    'Wf': ('Wf_kg_s', 'kg/s', 0.45359237),
}
HISTORY_CHANNELS = ['T48_K', 'Nc_rpm', 'Wf_kg_s']
NUMERIC_BASE = [v[0] + '_mean' for v in CHANNELS.values()] + ['n_readings']
META = ['dataset', 'source_partition', 'unit', 'cycle', 'engine_id', 'conservative_group', 'flight_class', 'split']


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(8*1024*1024), b''):
            digest.update(block)
    return digest.hexdigest()


def feature_catalog(window=3):
    records = []
    for raw, (stem, unit, factor) in CHANNELS.items():
        for suffix, formula in [('mean', 'Mean of finite readings in the current completed flight'),
                                ('std', 'Sample standard deviation of finite readings in the current flight (ddof=1)')]:
            records.append(dict(feature=f'{stem}_{suffix}', family='current_flight', source=raw,
                unit=unit, definition=formula, conversion_factor=factor, available='end of current flight',
                baseline=(suffix=='mean')))
    records.append(dict(feature='n_readings', family='current_flight', source='row count', unit='readings',
        definition='Number of ordered readings in current flight; proxy for observed flight length, not verified seconds',
        conversion_factor=1, available='end of current flight', baseline=True))
    for stem in HISTORY_CHANNELS:
        for suffix, definition in [(f'trailing{window}', f'Mean of current and up to {window-1} previous flight means, within the same history'),
                                   ('delta_prev', 'Current flight mean minus previous flight mean; missing on first observed flight')]:
            records.append(dict(feature=f'{stem}_{suffix}', family='causal_history', source=stem,
                unit=CHANNELS[next(raw for raw,v in CHANNELS.items() if v[0]==stem)][1], definition=definition,
                conversion_factor=1, available='end of current flight; no future flights', baseline=False))
    for name, definition, unit in [
        ('lpc_pressure_ratio', 'P24 mean / P21 mean, both total pressures', 'dimensionless'),
        ('burner_to_lpt_pressure_ratio', 'P40 mean / P50 mean; diagnostic ratio, not calibrated efficiency', 'dimensionless'),
        ('hpt_to_lpt_temperature_drop_K', 'T48 mean minus T50 mean; diagnostic temperature difference', 'K difference'),
        ('core_to_fan_speed_ratio', 'Nc mean / Nf mean; diagnostic shaft speed ratio', 'dimensionless')]:
        records.append(dict(feature=name, family='physical_combination', source='current flight means',
            unit=unit, definition=definition, conversion_factor=1, available='end of current flight', baseline=False))
    return pd.DataFrame(records)


def aggregate_file(path, chunk_rows=100_000):
    """Scan relevant raw columns; merge stable within-chunk flight moments.

    Invalid predictor numbers become NaN, not invented measurements. Broken
    keys/targets/categorical codes stop the run; they must not be guessed.
    Repeated unit/cycle keys are legitimate within-flight readings, not duplicates.
    """
    dataset = Path(path).stem.split('_')[1].split('-')[0]
    output, audit = [], []
    with h5py.File(path, 'r') as hdf:
        for part in ['dev', 'test']:
            n = len(hdf['A_'+part])
            if any(len(hdf[g+'_'+part]) != n for g in ['W','X_s','Y']):
                raise ValueError('Array rows are not aligned')
            source_names = column_names(hdf,'W') + column_names(hdf,'X_s')
            if not set(CHANNELS).issubset(source_names):
                raise ValueError('Missing required predictor channels')
            positions = [source_names.index(k) for k in CHANNELS]
            stems = [v[0] for v in CHANNELS.values()]
            factors = np.array([v[2] for v in CHANNELS.values()])
            counts = dict(dataset=dataset, partition=part, raw_readings=n,
                          predictor_nonfinite=0, impossible_predictor_values=0,
                          readings_removed=0, invalid_key_or_label_rows=0)
            pieces = []
            previous = None
            for start in range(0, n, chunk_rows):
                aux = hdf['A_'+part][start:start+chunk_rows]
                y = hdf['Y_'+part][start:start+chunk_rows, 0]
                # Keys and categories must be interpretable; never median-impute IDs/labels.
                invalid = (~np.isfinite(aux[:, :3]).all(axis=1) |
                           (aux[:, :2] < 1).any(axis=1) |
                           (aux[:, :2] != np.floor(aux[:, :2])).any(axis=1) |
                           ~np.isin(aux[:, 2], [1,2,3]) |
                           ~np.isfinite(y) | (y < 0) | (y != np.floor(y)))
                if invalid.any():
                    raise ValueError(f'{dataset}/{part}: invalid key/category/RUL; no output written')
                keys = np.column_stack([aux[:,0], aux[:,1]])
                order = np.vstack([previous,keys]) if previous is not None else keys
                if ((order[1:,0] == order[:-1,0]) & (order[1:,1] < order[:-1,1])).any():
                    raise ValueError('Cycle order reverses within an engine')
                previous=keys[-1].copy()
                raw = np.column_stack([hdf['W_'+part][start:start+chunk_rows],
                                       hdf['X_s_'+part][start:start+chunk_rows]])[:,positions]
                finite=np.isfinite(raw)
                counts['predictor_nonfinite'] += int((~finite).sum())
                bad = np.zeros_like(finite)
                for j,name in enumerate(CHANNELS):
                    if name.startswith(('T2','T3','T4','T5','P','N')) and name != 'TRA':
                        bad[:,j] = finite[:,j] & (raw[:,j] <= 0)
                    elif name in ['Mach','Wf']:
                        bad[:,j] = finite[:,j] & (raw[:,j] < 0)
                counts['impossible_predictor_values'] += int(bad.sum())
                raw[~finite | bad]=np.nan
                values=raw*factors
                frame=pd.DataFrame(values,columns=stems)
                frame['unit']=aux[:,0].astype(int);frame['cycle']=aux[:,1].astype(int)
                frame['flight_class']=aux[:,2].astype(int);frame['RUL']=y
                grouped=frame.groupby(['unit','cycle'],sort=True)
                agg=grouped[stems].agg(['count','mean','var'])
                agg.columns=['__'.join(c) for c in agg.columns]
                agg['n_readings']=grouped.size()
                for col in ['RUL','flight_class']:
                    agg[col+'_min']=grouped[col].min();agg[col+'_max']=grouped[col].max()
                pieces.append(agg.reset_index())
            combined=pd.concat(pieces,ignore_index=True)
            records=[]
            for (unit,cycle), chunks in combined.groupby(['unit','cycle'],sort=True):
                row=dict(dataset=dataset,source_partition=part,unit=int(unit),cycle=int(cycle),
                         n_readings=int(chunks.n_readings.sum()))
                for label in ['RUL','flight_class']:
                    if chunks[label+'_min'].min() != chunks[label+'_max'].max():
                        raise ValueError(f'Inconsistent {label} within a flight')
                    row[label]=int(chunks[label+'_min'].min())
                for stem in stems:
                    count=chunks[stem+'__count'].to_numpy()
                    means=chunks[stem+'__mean'].to_numpy()
                    valid=count>0
                    total=int(count.sum())
                    mean=np.sum(count[valid]*means[valid])/total if total else np.nan
                    m2=np.sum(chunks[stem+'__var'].fillna(0).to_numpy()*np.maximum(count-1,0))
                    m2+=np.sum(count[valid]*(means[valid]-mean)**2)
                    row[stem+'_mean']=mean
                    row[stem+'_std']=np.sqrt(max(m2/(total-1),0)) if total>1 else np.nan
                records.append(row)
            flights=pd.DataFrame(records)
            if flights.duplicated(['unit','cycle']).any():
                raise ValueError('Unexpected duplicate aggregate flight key')
            # Label-only retrospective audit; engine lifetime is never a feature.
            final=flights.groupby('unit').cycle.transform('max')
            if not (flights.RUL == final-flights.cycle).all():
                raise ValueError('RUL audit fails: inspect labels, do not repair using future lifetime')
            for _, history in flights.groupby('unit'):
                if not (history.cycle.diff().dropna()==1).all() or history.flight_class.nunique()!=1:
                    raise ValueError('Noncontiguous cycles or changing flight class')
            output.append(flights);audit.append(counts)
            print(f'{dataset}/{part}: {n:,} readings → {len(flights):,} completed flights',flush=True)
    return pd.concat(output,ignore_index=True),pd.DataFrame(audit)


def engineer_features(flights, window=3):
    """Each row depends only on that history's current or earlier flights."""
    rows=flights.sort_values(['dataset','source_partition','unit','cycle']).reset_index(drop=True).copy()
    rows['engine_id']=rows.dataset+':'+rows.unit.astype(str)
    # Equal IDs are linked conservatively; this does not establish shared identity.
    rows['conservative_group']='unit:'+rows.unit.astype(str)
    groups=rows.groupby(['dataset','source_partition','unit'],sort=False)
    for stem in HISTORY_CHANNELS:
        source=stem+'_mean'
        rows[stem+f'_trailing{window}']=groups[source].transform(lambda v:v.rolling(window,min_periods=1).mean())
        rows[stem+'_delta_prev']=groups[source].diff()
    def divide(a,b):
        return rows[a].div(rows[b].where(rows[b] != 0))
    rows['lpc_pressure_ratio']=divide('P24_kPa_mean','P21_kPa_mean')
    rows['burner_to_lpt_pressure_ratio']=divide('P40_kPa_mean','P50_kPa_mean')
    rows['hpt_to_lpt_temperature_drop_K']=rows.T48_K_mean-rows.T50_K_mean
    rows['core_to_fan_speed_ratio']=divide('Nc_rpm_mean','Nf_rpm_mean')
    return rows


def assign_splits(features, validation_unit_ids):
    rows=features.copy()
    reserved=set(rows.loc[rows.source_partition=='test','unit'])
    val=set(validation_unit_ids)
    if reserved & val:
        raise ValueError('Validation IDs overlap provided test IDs')
    rows['split']=np.select([
        rows.source_partition=='test',
        rows.unit.isin(reserved), rows.unit.isin(val)],
        ['test','quarantine_test_related','validation'],default='train')
    active=rows[rows.split!='quarantine_test_related']
    if active.groupby('conservative_group').split.nunique().max()!=1:
        raise ValueError('A conservative engine group crosses active splits')
    for ds,group in rows.groupby('dataset'):
        if set(group.loc[group.source_partition=='dev','unit']) & set(group.loc[group.source_partition=='test','unit']):
            raise ValueError(f'{ds}: supplied partitions overlap')
    return rows


def make_preprocessor(numeric_features):
    """Impute/scale numeric values; one-hot encode collection identity, not IDs."""
    return ColumnTransformer([
        ('numeric',Pipeline([
            ('imputer',SimpleImputer(strategy='median',add_indicator=True,keep_empty_features=True)),
            ('scaler',StandardScaler()),
        ]),list(numeric_features)),
        ('source',OneHotEncoder(categories=[['DS01','DS02']],handle_unknown='error',sparse_output=False),['dataset'])
    ],remainder='drop',verbose_feature_names_out=True)


def verify_version(directory):
    manifest=json.loads((directory/'manifest.json').read_text())
    for artifact in manifest['artifacts']:
        path=directory/artifact['file']
        if not path.is_file() or sha256(path)!=artifact['sha256']:
            raise ValueError(f'Versioned artifact changed or missing: {path}')
    return manifest


def prepare_data(root):
    root=Path(root).resolve()
    config=json.loads((root/'config/preprocessing.json').read_text())
    fixed_contract = {
        'schema_version': 'task4-v1', 'prediction_point': 'end_of_completed_flight',
        'cross_dataset_grouping': 'conservatively_link_equal_unit_ids',
        'exclude_unconfirmed_sensor': 'P2',
        'numeric_imputation': 'training_median_with_missing_indicators',
        'scaling': 'training_standard_score_ddof_0', 'categorical_predictors': ['dataset'],
        'outlier_policy': 'retain_finite_values_no_IQR_deletion',
    }
    for name, expected in fixed_contract.items():
        if config.get(name) != expected:
            raise ValueError(f'Unsupported {name}: changing this policy requires a new implementation/schema')
    if config['chunk_rows'] < 1 or config['rolling_window_flights'] < 1:
        raise ValueError('Chunk size and trailing window must be positive')
    paths=[root/'data/raw'/name for name in config['files']]
    for path in paths:
        if not path.is_file(): raise FileNotFoundError(f'Expected raw file: {path}')
    raw_manifest=[dict(file=p.name,bytes=p.stat().st_size,sha256=sha256(p)) for p in paths]
    versions={name:importlib.metadata.version(name) for name in ['numpy','pandas','h5py','scikit-learn','scipy','joblib']}
    versions['python']=platform.python_version()
    code_manifest={name:sha256(root/name) for name in ['src/preprocessing.py','src/data_understanding.py','config/preprocessing.json']}
    fingerprint=hashlib.sha256(json.dumps(dict(config=config,raw=raw_manifest,versions=versions,code=code_manifest),sort_keys=True).encode()).hexdigest()
    version_id=config['schema_version']+'-'+fingerprint[:12]
    parent=root/'data/processed';parent.mkdir(parents=True,exist_ok=True)
    destination=parent/version_id
    if destination.exists():
        manifest=verify_version(destination)
        export_evidence(root,destination,manifest)
        print('Verified existing immutable version:',version_id,flush=True)
        return destination,manifest
    results=[aggregate_file(p,config['chunk_rows']) for p in paths]
    flights=pd.concat([r[0] for r in results],ignore_index=True)
    audit=pd.concat([r[1] for r in results],ignore_index=True)
    if flights.duplicated(['dataset','unit','cycle']).any(): raise ValueError('Integrated flight key collision')
    features=assign_splits(engineer_features(flights,config['rolling_window_flights']),config['validation_unit_ids'])
    catalog=feature_catalog(config['rolling_window_flights'])
    numeric=catalog.feature.tolist()
    if len(numeric)!=len(set(numeric)):raise ValueError('Duplicate feature names')
    features[numeric]=features[numeric].replace([np.inf,-np.inf],np.nan)
    training=features[features.split=='train']
    if training.empty or set(training.dataset)!=set(['DS01','DS02']):raise ValueError('Training does not cover both datasets')
    if training[numeric].isna().all().any():raise ValueError('An entire training feature is missing; review instead of inventing values')
    preprocessing=make_preprocessor(numeric)
    preprocessing.fit(training[numeric+['dataset']])
    output_names=preprocessing.get_feature_names_out().tolist()
    split_summary=features.groupby(['dataset','source_partition','split'],as_index=False).agg(
        flights=('cycle','size'),histories=('engine_id','nunique'),raw_readings=('n_readings','sum'))
    assignment=features[
        ['dataset','source_partition','unit','engine_id','conservative_group','flight_class','split']].drop_duplicates()
    imputer=preprocessing.named_transformers_['numeric'].named_steps['imputer']
    scaler=preprocessing.named_transformers_['numeric'].named_steps['scaler']
    scaling=pd.DataFrame({'output_feature':output_names[:len(scaler.mean_)],
                          'training_mean':scaler.mean_,'training_scale':scaler.scale_})
    imputation=pd.DataFrame({'feature':numeric,'training_median':imputer.statistics_,
        'missing_train':training[numeric].isna().sum().to_numpy(),
        'missing_all':features[numeric].isna().sum().to_numpy()})
    temp=Path(tempfile.mkdtemp(prefix='.building-',dir=parent))
    try:
        features.to_csv(temp/'flights_features.csv',index=False,float_format='%.12g')
        features[features.split=='quarantine_test_related'].to_csv(temp/'quarantine.csv',index=False,float_format='%.12g')
        shapes={}
        for split in ['train','validation','test']:
            selected=features[features.split==split]
            X=preprocessing.transform(selected[numeric+['dataset']])
            if not np.isfinite(X).all():raise ValueError('Non-finite transformed matrix')
            pd.DataFrame(X,columns=output_names).to_csv(temp/f'X_{split}.csv',index=False,float_format='%.12g')
            selected[['RUL']].to_csv(temp/f'y_{split}.csv',index=False)
            selected[META].to_csv(temp/f'rows_{split}.csv',index=False)
            shapes[split]=list(X.shape)
        joblib.dump(preprocessing,temp/'preprocessor.joblib')
        catalog.to_csv(temp/'feature_catalog.csv',index=False)
        split_summary.to_csv(temp/'split_summary.csv',index=False)
        assignment.to_csv(temp/'engine_splits.csv',index=False)
        audit.to_csv(temp/'cleaning_audit.csv',index=False)
        scaling.to_csv(temp/'scaling_parameters.csv',index=False)
        imputation.to_csv(temp/'imputation_parameters.csv',index=False)
        baseline_columns=['numeric__'+name for name in NUMERIC_BASE]+['source__dataset_DS01','source__dataset_DS02']
        (temp/'baseline_columns.json').write_text(json.dumps(baseline_columns,indent=2)+'\n')
        manifest=dict(version_id=version_id,fingerprint=fingerprint,
            created_at=datetime.now(ZoneInfo('Europe/Berlin')).isoformat(),
            config=config,raw_files=raw_manifest,environment=versions,code=code_manifest,
            raw_readings=int(features.n_readings.sum()),processed_flights=len(features),engine_histories=int(features.engine_id.nunique()),
            numeric_features=len(numeric),model_columns=len(output_names),baseline_columns=len(baseline_columns),
            missing_numeric_features=int(features[numeric].isna().sum().sum()),
            missing_by_split={p:int(g[numeric].isna().sum().sum()) for p,g in features.groupby('split')},
            learned_missing_indicators=[numeric[i] for i in imputer.indicator_.features_],
            matrix_shapes=shapes,quarantined_flights=int((features.split=='quarantine_test_related').sum()),
            predictor_nonfinite=int(audit.predictor_nonfinite.sum()),
            impossible_predictor_values=int(audit.impossible_predictor_values.sum()),readings_removed=int(audit.readings_removed.sum()),
            fitting_rows=len(training),fitting_engine_groups=sorted(training.conservative_group.unique()),
            artifacts=[])
        manifest['fit_numeric_max_abs_mean']=float(np.abs(scaler.transform(imputer.transform(training[numeric])).mean(axis=0)).max())
        for path in sorted(temp.iterdir()):
            manifest['artifacts'].append(dict(file=path.name,bytes=path.stat().st_size,sha256=sha256(path)))
        (temp/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
        temp.rename(destination)
    except BaseException:
        shutil.rmtree(temp,ignore_errors=True)
        raise
    export_evidence(root,destination,manifest)
    print('Created immutable prepared version:',version_id,flush=True)
    return destination,manifest


def export_evidence(root,directory,manifest):
    """Only compact review evidence goes under reports, never full model tables."""
    evidence=Path(root)/'reports/results/task4';evidence.mkdir(parents=True,exist_ok=True)
    for name in ['manifest.json','feature_catalog.csv','split_summary.csv','engine_splits.csv',
                 'cleaning_audit.csv','scaling_parameters.csv','imputation_parameters.csv','baseline_columns.json']:
        shutil.copyfile(directory/name,evidence/name)
    preview=pd.read_csv(directory/'flights_features.csv',nrows=5)[
        ['dataset','unit','cycle','split','n_readings','alt_m_mean','T48_K_mean','T48_K_delta_prev','RUL']]
    preview.to_csv(evidence/'prepared_preview.csv',index=False)
