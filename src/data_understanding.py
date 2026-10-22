"""Read-only, bounded-memory N-CMAPSS inspection for the Task 3 notebook.

No models are fitted and no raw file is changed. The audit scans every numeric
cell; distribution plots and duplicate checks explicitly state their scope.
"""
from pathlib import Path
import hashlib
import importlib.metadata
import platform
import numpy as np
import pandas as pd
import h5py

GROUPS = ('W', 'X_s', 'X_v', 'T', 'Y', 'A')
PREDICTORS = ('W', 'X_s')
PARTITIONS = ('dev', 'test')

# Definitions from the supplied 2020 dataset description, Tables 1–4.
# P2 is absent from that older table: mark its interpretation for confirmation.
DEFINITIONS = {
    'alt': ('Altitude', 'ft', 'ratio'),
    'Mach': ('Flight Mach number', 'dimensionless', 'ratio'),
    'TRA': ('Throttle-resolver angle', '%', 'ratio'),
    'T2': ('Total temperature at fan inlet', '°R (Rankine)', 'ratio'),
    'T24': ('Total temperature at LPC outlet', '°R (Rankine)', 'ratio'),
    'T30': ('Total temperature at HPC outlet', '°R (Rankine)', 'ratio'),
    'T48': ('Total temperature at HPT outlet', '°R (Rankine)', 'ratio'),
    'T50': ('Total temperature at LPT outlet', '°R (Rankine)', 'ratio'),
    'P15': ('Total pressure in bypass duct', 'psia', 'ratio'),
    'P2': ('Inlet pressure; interpretation/unit require source confirmation', 'not confirmed', 'continuous; confirm'),
    'P21': ('Total pressure at fan outlet', 'psia', 'ratio'),
    'P24': ('Total pressure at LPC outlet', 'psia', 'ratio'),
    'Ps30': ('Static pressure at HPC outlet', 'psia', 'ratio'),
    'P40': ('Total pressure at burner outlet', 'psia', 'ratio'),
    'P50': ('Total pressure at LPT outlet', 'psia', 'ratio'),
    'Nf': ('Physical fan speed', 'rpm', 'ratio'),
    'Nc': ('Physical core speed', 'rpm', 'ratio'),
    'Wf': ('Fuel flow', 'lb/s (source: pps)', 'ratio'),
    'T40': ('Total temperature at burner outlet', '°R (Rankine)', 'ratio'),
    'P30': ('Total pressure at HPC outlet', 'psia', 'ratio'),
    'P45': ('Total pressure at HPT outlet', 'psia', 'ratio'),
    'W21': ('Fan flow', 'lb/s (source: pps)', 'ratio'),
    'W22': ('Flow out of LPC', 'lbm/s', 'ratio'),
    'W25': ('Flow into HPC', 'lbm/s', 'ratio'),
    'W31': ('HPT coolant bleed', 'lbm/s', 'ratio'),
    'W32': ('HPT coolant bleed', 'lbm/s', 'ratio'),
    'W48': ('Flow out of HPT', 'lbm/s', 'ratio'),
    'W50': ('Flow out of LPT', 'lbm/s', 'ratio'),
    'SmFan': ('Fan stall margin', 'dimensionless', 'continuous'),
    'SmLPC': ('LPC stall margin', 'dimensionless', 'continuous'),
    'SmHPC': ('HPC stall margin', 'dimensionless', 'continuous'),
    'phi': ('Ratio of fuel flow to Ps30', 'pps/psi', 'ratio'),
    'RUL': ('Remaining useful life until simulated end-of-life', 'flight cycles', 'discrete ratio; target'),
    'unit': ('Engine identifier; unique only within a dataset', 'identifier', 'nominal'),
    'cycle': ('Flight-cycle index within an engine history', 'flight cycle', 'ordered index'),
    'Fc': ('Flight class: 1 short, 2 medium, 3 long', 'class code', 'ordinal category'),
    'hs': ('Health state: 1 healthy, 0 degraded (example notebook interpretation)', 'binary code', 'nominal category'),
}


def column_names(hdf, group):
    if group == 'Y':
        return ['RUL']
    return [x.decode('utf-8') if isinstance(x, bytes) else str(x) for x in hdf[group + '_var'][:]]


def file_inventory(paths):
    """Inspect HDF5 metadata without materializing the large arrays."""
    records = []
    for path in paths:
        with h5py.File(path, 'r') as hdf:
            for name, array in hdf.items():
                records.append(dict(dataset=path.stem.split('_')[1].split('-')[0], file=path.name,
                                    file_bytes=path.stat().st_size, array=name,
                                    shape=str(array.shape), rows=array.shape[0],
                                    columns=array.shape[1] if array.ndim == 2 else 1,
                                    dtype=str(array.dtype), array_bytes=array.nbytes))
    return pd.DataFrame(records)


def feature_dictionary(path):
    records = []
    with h5py.File(path, 'r') as hdf:
        for group in GROUPS:
            for name in column_names(hdf, group):
                if group == 'T':
                    component, kind, _ = name.split('_')
                    description = f'{component} {"efficiency" if kind == "eff" else "flow"} modifier (simulator health parameter)'
                    unit, scale = 'modifier', 'continuous'
                else:
                    description, unit, scale = DEFINITIONS[name]
                role = ('candidate predictor' if group in PREDICTORS else
                        'target; never a predictor' if group == 'Y' else
                        'simulator-only; exclude from baseline' if group in ('T', 'X_v') else
                        'grouping/diagnostic metadata; exclude from baseline')
                scale_info = measurement_scale(name, group)
                records.append(dict(group=group, feature=name, dtype=str(hdf[group + '_dev'].dtype),
                                    description=description, unit=unit, role=role, **scale_info))
    return pd.DataFrame(records)


def measurement_scale(name, group):
    """Domain overrides, following the lecturer's scales/example notebook.

    Discrete/continuous and nominal/ordinal/interval/ratio are separate axes.
    Do not infer nominal from high uniqueness or ratio merely from numeric dtype.
    """
    variability = 'continuous'
    kind = 'quantitative (metric)'
    if name in ('unit', 'hs'):
        scale, kind, variability = 'Nominal', 'qualitative (categorical)', 'categorical'
        reason = 'Identifier/label only; arithmetic on codes is not meaningful.'
    elif name == 'Fc':
        scale, kind, variability = 'Ordinal', 'qualitative (categorical)', 'ordered categorical'
        reason = 'Short < medium < long; gaps between class codes are not equal quantities.'
    elif name == 'cycle':
        scale, variability = 'Interval', 'discrete'
        reason = 'Sequential index with a chosen origin; cycle differences count flights, ratios of index labels are not interpreted.'
    elif name == 'RUL':
        scale, variability = 'Ratio', 'discrete'
        reason = 'Count of remaining flight cycles; zero means no cycles remain under the verified label convention.'
    elif name == 'alt':
        scale = 'Interval'
        reason = 'Altitude uses a reference datum; sea-level zero does not mean absence of distance.'
    elif name == 'TRA':
        scale = 'Interval'
        reason = 'Working classification: control-position scale; source does not justify a physical twice-as-much interpretation.'
    elif name == 'P2' or name.startswith('Sm'):
        scale = 'Unconfirmed'
        reason = 'Confirm source definition/zero-point convention before interpreting ratios.'
    elif group == 'T':
        scale = 'Interval'
        reason = 'Working classification for baseline-relative simulator modifiers; zero is nominal setting, not absence of health.'
    else:
        scale = 'Ratio'
        reason = 'Absolute temperature, speed, flow, pressure, or physical ratio with meaningful zero; source units apply.'
    operators = {'Nominal': '==, !=', 'Ordinal': '==, !=, <, <=, >, >=',
                 'Interval': '==, !=, <, <=, >, >=, +, -',
                 'Ratio': '==, !=, <, <=, >, >=, +, -, *, /',
                 'Unconfirmed': 'Confirm semantics first'}[scale]
    return dict(attribute_type=kind, variability=variability, scale=scale,
                operators=operators, scale_reason=reason)


def lecturer_feature_table(dictionary, stats, sample):
    """Lecturer-style summary; exact counts/ranges vs sample uniques labelled."""
    result = stats.merge(dictionary, on=['group', 'feature'], validate='many_to_one')
    uniques = sample.groupby(['dataset', 'partition']).agg(
        {name: 'nunique' for name in dictionary.feature}).reset_index().melt(
            id_vars=['dataset', 'partition'], var_name='feature', value_name='Unique (sample)')
    result = result.merge(uniques, on=['dataset', 'partition', 'feature'], validate='one_to_one')
    result['Non-Null (full)'] = result.rows - result.missing
    result['Null Values'] = np.where(result.missing > 0, 'Yes', 'No')
    result['Value Range (full)'] = result.apply(lambda r: f'{r.minimum:.6g} – {r.maximum:.6g}', axis=1)
    result = result.rename(columns={'feature': 'Column Name', 'dtype': 'Dtype', 'scale': 'Scale',
                                    'operators': 'Operators', 'scale_reason': 'Notes'})
    return result[['dataset', 'partition', 'group', 'Column Name', 'Dtype',
                   'Non-Null (full)', 'Unique (sample)', 'attribute_type', 'variability',
                   'Scale', 'Operators', 'Value Range (full)', 'Null Values', 'Notes']]


def scan_file(path, chunk_rows=100_000, sample_rows=12_000):
    """Full scan + bounded, evenly spaced diagnostic sample per partition.

    Exact totals/min/max/non-finite counts cover every numeric array. Per-cycle
    means cover every reading of W and X_s. No entire raw partition is loaded.
    A repeated (unit, cycle) is expected: a cycle contains many readings.
    """
    dataset = path.stem.split('_')[1].split('-')[0]
    stats, cycles, samples, checks = [], [], [], []
    with h5py.File(path, 'r') as hdf:
        names = {g: column_names(hdf, g) for g in GROUPS}
        for part in PARTITIONS:
            n = len(hdf['A_' + part])
            arrays = {g: hdf[g + '_' + part] for g in GROUPS}
            assert all(a.shape == (n, len(names[g])) for g, a in arrays.items()), 'Misaligned arrays'
            assert all(np.issubdtype(a.dtype, np.number) for a in arrays.values()), 'Non-numeric data'
            accum = {g: dict(count=np.zeros(len(names[g]), dtype=np.int64),
                            missing=np.zeros(len(names[g]), dtype=np.int64),
                            infinite=np.zeros(len(names[g]), dtype=np.int64),
                            mean=np.zeros(len(names[g])), m2=np.zeros(len(names[g])),
                            minimum=np.full(len(names[g]), np.inf), maximum=np.full(len(names[g]), -np.inf)) for g in GROUPS}
            parts, previous, adjacent_duplicates, invalid_categories, invalid_indices, reversals = [], None, 0, 0, 0, 0
            previous_key = None
            for start in range(0, n, chunk_rows):
                blocks = {g: a[start:start + chunk_rows] for g, a in arrays.items()}
                # Parallel variance update (stable, unlike E[x²] - E[x]²).
                for g, block in blocks.items():
                    a = accum[g]
                    finite = np.isfinite(block)
                    count = finite.sum(axis=0)
                    safe = np.where(finite, block, 0.0)
                    mean = np.divide(safe.sum(axis=0), count, out=np.zeros(len(count)), where=count > 0)
                    m2 = np.where(finite, block - mean, 0.0)
                    m2 = (m2 * m2).sum(axis=0)
                    total = a['count'] + count
                    delta = mean - a['mean']
                    a['m2'] += m2 + np.divide(delta**2 * a['count'] * count, total, out=np.zeros(len(count)), where=total > 0)
                    a['mean'] += np.divide(delta * count, total, out=np.zeros(len(count)), where=total > 0)
                    a['count'] = total
                    a['missing'] += np.isnan(block).sum(axis=0)
                    a['infinite'] += np.isinf(block).sum(axis=0)
                    a['minimum'] = np.minimum(a['minimum'], np.where(finite, block, np.inf).min(axis=0))
                    a['maximum'] = np.maximum(a['maximum'], np.where(finite, block, -np.inf).max(axis=0))
                all_values = np.column_stack([blocks[g] for g in GROUPS])
                adjacent_duplicates += int(np.all(all_values[1:] == all_values[:-1], axis=1).sum())
                if previous is not None:
                    adjacent_duplicates += int(np.array_equal(previous, all_values[0]))
                previous = all_values[-1].copy()
                aux = blocks['A']
                invalid_categories += int((~np.isin(aux[:, 2], [1, 2, 3])).sum() + (~np.isin(aux[:, 3], [0, 1])).sum())
                invalid_indices += int(((aux[:, :2] < 1) | (aux[:, :2] != np.floor(aux[:, :2]))).sum())
                keys = aux[:, :2]
                if previous_key is not None:
                    keys = np.vstack([previous_key, keys])
                reversals += int(((keys[1:, 0] == keys[:-1, 0]) & (keys[1:, 1] < keys[:-1, 1])).sum())
                previous_key = aux[-1, :2].copy()
                frame = pd.DataFrame(np.column_stack([aux, blocks['Y'], blocks['W'], blocks['X_s']]),
                                     columns=names['A'] + ['RUL'] + names['W'] + names['X_s'])
                grouped = frame.groupby(['unit', 'cycle'], sort=False)
                # Keep only small per-cycle aggregates after each chunk.
                aggregations = {'RUL': ['min', 'max'], 'Fc': ['min', 'max'], 'hs': ['min', 'max']}
                aggregations.update({v: ['sum', 'count'] for v in names['W'] + names['X_s']})
                agg = grouped.agg(aggregations)
                agg.columns = ['_'.join(c) for c in agg.columns]
                agg['readings'] = grouped.size()
                parts.append(agg.reset_index())
            combined = pd.concat(parts, ignore_index=True)
            how = {c: ('min' if c.endswith('_min') else 'max' if c.endswith('_max') else 'sum') for c in combined if c not in ('unit', 'cycle')}
            cycle = combined.groupby(['unit', 'cycle'], as_index=False).agg(how)
            for v in names['W'] + names['X_s']:
                cycle[v + '_mean'] = cycle.pop(v + '_sum') / cycle.pop(v + '_count')
            cycle.insert(0, 'partition', part)
            cycle.insert(0, 'dataset', dataset)
            cycle[['unit', 'cycle']] = cycle[['unit', 'cycle']].astype(int)
            cycles.append(cycle)
            # A diagnostic sample, NOT random training/test splitting.
            indices = np.unique(np.linspace(0, n - 1, min(sample_rows, n), dtype=np.int64))
            sample = pd.DataFrame(np.column_stack([arrays[g][indices] for g in GROUPS]),
                                  columns=sum([names[g] for g in GROUPS], []))
            duplicate_sample = int(sample.duplicated().sum())
            sample.insert(0, 'row_in_partition', indices)
            sample.insert(0, 'partition', part)
            sample.insert(0, 'dataset', dataset)
            samples.append(sample)
            for g, a in accum.items():
                for i, variable in enumerate(names[g]):
                    stats.append(dict(dataset=dataset, partition=part, group=g, feature=variable,
                                      rows=n, finite=int(a['count'][i]), missing=int(a['missing'][i]),
                                      infinite=int(a['infinite'][i]), minimum=a['minimum'][i], maximum=a['maximum'][i],
                                      mean=a['mean'][i], std=np.sqrt(a['m2'][i] / max(a['count'][i] - 1, 1))))
            checks.append(dict(dataset=dataset, partition=part, rows=n, aligned=True,
                               invalid_categories=invalid_categories, invalid_indices=invalid_indices,
                               within_unit_cycle_reversals=reversals, adjacent_exact_duplicates=adjacent_duplicates,
                               diagnostic_sample_rows=len(sample), sample_exact_duplicates=duplicate_sample))
            print(f'{dataset} / {part}: scanned {n:,} rows across all 47 fields', flush=True)
    return dict(stats=pd.DataFrame(stats), cycles=pd.concat(cycles, ignore_index=True),
                sample=pd.concat(samples, ignore_index=True), checks=pd.DataFrame(checks))


def engine_summary(cycles):
    engines = cycles.groupby(['dataset', 'partition', 'unit'], as_index=False).agg(
        readings=('readings', 'sum'), cycles=('cycle', 'nunique'), first_cycle=('cycle', 'min'),
        last_cycle=('cycle', 'max'), rul_min=('RUL_min', 'min'), rul_max=('RUL_max', 'max'),
        flight_class=('Fc_min', 'min'), flight_class_max=('Fc_max', 'max'),
        healthy_cycles=('hs_max', 'sum'), mean_altitude=('alt_mean', 'mean'))
    return engines


def consistency_report(cycles):
    """Per-engine label and cycle logic; failure cycle is observed retrospectively."""
    records = []
    for (ds, part, unit), rows in cycles.groupby(['dataset', 'partition', 'unit']):
        rows = rows.sort_values('cycle')
        expected = rows.cycle.max() - rows.cycle
        records.append(dict(dataset=ds, partition=part, unit=int(unit),
            inconsistent_rul_cycles=int((rows.RUL_min != rows.RUL_max).sum()),
            rul_formula_violations=int(((rows.RUL_min != expected) | (rows.RUL_max != expected)).sum()),
            noncontiguous_cycles=int((rows.cycle.diff().dropna() != 1).sum()),
            health_switch_back=int((rows.hs_min.diff().dropna() > 0).sum()),
            mixed_health_cycles=int((rows.hs_min != rows.hs_max).sum()),
            mixed_flight_class_cycles=int((rows.Fc_min != rows.Fc_max).sum())))
    return pd.DataFrame(records)


def outlier_screen(sample):
    """Tukey fences on DEVELOPMENT samples only; flags are not proof of errors."""
    records = []
    columns = [k for k in DEFINITIONS if k not in ('unit', 'cycle', 'Fc', 'hs', 'RUL')]
    for ds, rows in sample[sample.partition == 'dev'].groupby('dataset'):
        for col in columns:
            q1, q3 = rows[col].quantile([.25, .75])
            iqr = q3 - q1
            flagged = (rows[col] < q1 - 1.5 * iqr) | (rows[col] > q3 + 1.5 * iqr)
            records.append(dict(dataset=ds, feature=col, sample_rows=len(rows), q1=q1, q3=q3,
                                iqr=iqr, flagged=int(flagged.sum()), flagged_pct=100 * flagged.mean()))
    return pd.DataFrame(records)


def first_flight(path, partition='dev'):
    """Read only the first contiguous flight; preserves its original ordering."""
    with h5py.File(path, 'r') as hdf:
        first = hdf['A_' + partition][0, :2]
        # Flights are far smaller than this bound in the verified files.
        aux = hdf['A_' + partition][:100_000]
        match = (aux[:, :2] == first).all(axis=1)
        stop = np.flatnonzero(~match)
        end = int(stop[0]) if len(stop) else len(aux)
        assert end < 100_000, 'Increase first-flight bound explicitly'
        frame = pd.DataFrame(hdf['W_' + partition][:end], columns=column_names(hdf, 'W'))
        for i, name in enumerate(column_names(hdf, 'X_s')):
            frame[name] = hdf['X_s_' + partition][:end, i]
        return frame, int(first[0]), int(first[1])


def source_manifest(paths):
    """SHA-256 gives byte identity, not proof of upstream provenance or licensing."""
    records = []
    for path in paths:
        digest = hashlib.sha256()
        with path.open('rb') as stream:
            for block in iter(lambda: stream.read(8 * 1024 * 1024), b''):
                digest.update(block)
        records.append(dict(file=path.name, bytes=path.stat().st_size, sha256=digest.hexdigest()))
    return records


def environment_versions():
    return dict(python=platform.python_version(), **{name: importlib.metadata.version(name) for name in
        ['numpy', 'pandas', 'h5py', 'matplotlib', 'jupyterlab', 'nbclient', 'nbformat']})
