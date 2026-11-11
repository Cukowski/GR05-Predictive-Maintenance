"""Task 5 reproducible descriptive inputs and training-only interpretation.

No predictor selection, regression fitting, or test-label interpretation occurs.
"""
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd
from src.preprocessing import CHANNELS, engineer_features, assign_splits, verify_version


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def reconstruct_flights(root):
    """Reconstruct available means/history from audited Task 3 aggregates.

    Within-flight standard deviations cannot be recovered from means. This table
    intentionally is NOT a replacement for the full Task 4 model representation.
    """
    root=Path(root)
    cycles=pd.read_csv(root/'reports/results/cycles.csv')
    expected=pd.read_csv(root/'reports/results/task4/engine_splits.csv')
    config=json.loads((root/'config/preprocessing.json').read_text())
    keys=['dataset','partition','unit','cycle']
    if cycles.duplicated(keys).any():raise ValueError('Duplicate flight keys')
    if (cycles.RUL_min!=cycles.RUL_max).any() or (cycles.Fc_min!=cycles.Fc_max).any():
        raise ValueError('Inconsistent flight metadata or target')
    flights=cycles[['dataset','partition','unit','cycle','readings','Fc_min','RUL_min']].rename(
        columns={'partition':'source_partition','readings':'n_readings','Fc_min':'flight_class','RUL_min':'RUL'}).copy()
    flights[['unit','cycle','n_readings','flight_class','RUL']]=flights[['unit','cycle','n_readings','flight_class','RUL']].astype(int)
    for source,(stem,_,factor) in CHANNELS.items():flights[stem+'_mean']=cycles[source+'_mean']*factor
    flights=assign_splits(engineer_features(flights,config['rolling_window_flights']),config['validation_unit_ids'])
    check=flights.merge(expected[['dataset','source_partition','unit','split']],on=['dataset','source_partition','unit'],
                        suffixes=('','_expected'),how='left',validate='many_to_one')
    if not (check.split==check.split_expected).all():raise ValueError('Reconstructed split differs from Task 4 assignments')
    out=root/'reports/results/task5';out.mkdir(parents=True,exist_ok=True)
    path=out/'flights_features_from_cycles.csv'
    flights.to_csv(path,index=False,float_format='%.12g')
    return flights


def load_flights(root,source='reconstructed'):
    root=Path(root)
    manifest=json.loads((root/'reports/results/task4/manifest.json').read_text())
    if source=='reconstructed':
        flights=reconstruct_flights(root)
        source_path=root/'reports/results/task5/flights_features_from_cycles.csv'
        label='Task 3 cycle aggregates; reconstructed means and causal history, not full Task 4 variances'
    elif source=='full_task4':
        folder=root/'data/processed'/manifest['version_id']
        verify_version(folder)
        source_path=folder/'flights_features.csv';flights=pd.read_csv(source_path)
        label='Hash-verified full local Task 4 prepared features'
    else:raise ValueError('Choose reconstructed or full_task4 explicitly')
    if len(flights)!=manifest['processed_flights']:raise ValueError('Unexpected flight count')
    active=flights[flights.split!='quarantine_test_related']
    if (active.groupby('conservative_group').split.nunique()>1).any():raise ValueError('Engine groups cross active splits')
    provenance=dict(source=source,description=label,source_path=str(source_path.relative_to(root)),
        sha256=digest(source_path),task4_version=manifest['version_id'],
        cycle_export_sha256=digest(root/'reports/results/cycles.csv'),
        split_export_sha256=digest(root/'reports/results/task4/engine_splits.csv'),
        row_count=len(flights),training_flights=int((flights.split=='train').sum()),
        analysis_scope='Training hypotheses; fixed descriptive validation check; no test/quarantine hypothesis development',
        independence='Seven training source histories, six conservative unit-ID groups; cross-subset independence unresolved')
    return flights,provenance


def training_insights(train):
    """Compute only from explicitly labelled training rows."""
    if train.empty or not train.split.eq('train').all():raise ValueError('Insights require training rows only')
    sensors=['T48_K_mean','Nc_rpm_mean','Wf_kg_s_mean']
    correlations=[]
    for eid,group in train.groupby('engine_id'):
        for sensor in sensors:
            correlations.append(dict(engine_id=eid,sensor=sensor,r=float(group[['RUL',sensor]].corr().iloc[0,1])))
    corr=pd.DataFrame(correlations)
    stages=pd.cut(train.RUL,[-1,20,50,np.inf],labels=['Late','Middle','Early'])
    per_engine=train.assign(life_stage=stages).groupby(['engine_id','life_stage'],observed=True)[sensors].median()
    paired=per_engine['T48_K_mean'].unstack('life_stage')
    difference=paired['Late']-paired['Early']
    conditions=train.assign(life_stage=stages).groupby('life_stage',observed=True)[['alt_m_mean','Mach_mean','TRA_pct_mean']].median()
    t48=corr[corr.sensor=='T48_K_mean']
    deltas=['T48_K_delta_prev','Nc_rpm_delta_prev','Wf_kg_s_delta_prev']
    return dict(training_flights=len(train),source_histories=int(train.engine_id.nunique()),
        conservative_groups=int(train.conservative_group.nunique()),
        rul_mean=float(train.RUL.mean()),rul_min=int(train.RUL.min()),rul_max=int(train.RUL.max()),
        t48_r_min=float(t48.r.min()),t48_r_max=float(t48.r.max()),t48_negative_histories=int((t48.r<0).sum()),
        late_minus_early_T48_K_median=float(difference.median()),
        late_minus_early_T48_K_min=float(difference.min()),late_minus_early_T48_K_max=float(difference.max()),
        paired_T48_histories=int(difference.notna().sum()),
        delta_nonmissing_counts={name:int(train[name].notna().sum()) for name in deltas},
        delta_rul_correlations={name:float(train[['RUL',name]].corr().iloc[0,1]) for name in deltas},
        condition_stage_medians=json.loads(conditions.reset_index().to_json(orient='records')),
        sensor_correlation_ranges={name:dict(min=float(g.r.min()),max=float(g.r.max())) for name,g in corr.groupby('sensor')},
        limitations=['Correlations are descriptive, not causal or hypothesis-test p-values',
                     'Flights within histories are dependent; shared IDs are conservatively linked',
                     'Operating-stage summaries are flight weighted',
                     'RUL stages are retrospective target groups, never prediction inputs',
                     'Validation has already been inspected during branch review; this is not a blinded confirmation'])


def insight_markdown(info):
    ranges=info['sensor_correlation_ranges']
    return f'''### Training findings recorded before the validation output
- **H1 — sensor association:** T48–RUL Pearson r is negative in {info['t48_negative_histories']}/{info['source_histories']} training histories, ranging from {info['t48_r_min']:.3f} to {info['t48_r_max']:.3f}. This is exploratory association, not proof of wear causality or validated prediction.
- **Retrospective grouping:** paired late-minus-early T48 engine medians are higher by a median {info['late_minus_early_T48_K_median']:.2f} K across {info['paired_T48_histories']} histories (range {info['late_minus_early_T48_K_min']:.2f}–{info['late_minus_early_T48_K_max']:.2f} K). Groups use true RUL (0–20, 21–50, >50), so they cannot be deployed as known inputs.
- **H2 — historical changes:** each difference has {next(iter(info['delta_nonmissing_counts'].values()))} observed training values; the first flight in each history has no previous observation. Differences describe short-term changes; added predictive value is untested.
- **H3 — operating context:** altitude/Mach/throttle vary across flights and groups. Displayed medians document context; they do not establish a causal or adjusted effect. Whole-flight summaries mix phases.
- **H4 — heterogeneity:** Nc–RUL r ranges from {ranges['Nc_rpm_mean']['min']:.3f} to {ranges['Nc_rpm_mean']['max']:.3f}, including both signs. T48 association also varies in magnitude. A universal sensor threshold is not justified.

**Business interpretation:** temperature context and recent history are candidates for later RUL modeling. Overestimating RUL could delay an intervention; underestimating could prompt premature maintenance. We have not demonstrated forecast accuracy, costs, savings, or operational suitability.

**Evidence scope:** {info['training_flights']} flights; {info['source_histories']} dataset-scoped histories but only {info['conservative_groups']} conservative unit-ID groups. No independent-observation significance tests. These data had already been examined during the integration review; this write-up is not a preregistered or blinded hypothesis test.'''
