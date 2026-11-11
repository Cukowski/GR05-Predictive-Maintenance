"""Repeatable Task 1–5 progress checks; never trains a predictive model.

Run python scripts/check_project.py --raw-hashes --write-report for a full local
check. Without --raw-hashes, full raw-byte hashing is skipped explicitly.
Use --skip-local-data for a cloned repository without ignored HDF5/processed data.
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import argparse,hashlib,json,re,sys,zipfile,subprocess,xml.etree.ElementTree as ET
from datetime import datetime
from zoneinfo import ZoneInfo
import nbformat
import numpy as np
import pandas as pd
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from src.preprocessing import verify_version,sha256
from src.descriptive_analysis import training_insights

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True);self.ids=set();self.links=[];self.stack=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:
            if a['id'] in self.ids:raise ValueError('Duplicate HTML id: '+a['id'])
            self.ids.add(a['id'])
        if tag=='img' and not a.get('alt'):raise ValueError('Image missing alt text')
        for key in ('href','src'):
            if key in a:self.links.append(a[key])
        if tag not in {'meta','link','br','hr','img','input','source','area','base','embed','param','track','wbr'}:self.stack.append(tag)
    def handle_endtag(self,tag):
        if not self.stack or self.stack.pop()!=tag:raise ValueError('Unbalanced HTML tag: '+tag)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--raw-hashes',action='store_true')
    parser.add_argument('--skip-local-data',action='store_true')
    parser.add_argument('--write-report',action='store_true')
    parser.add_argument('--http-check',action='store_true',help='Briefly serve five pages on loopback and check HTTP responses; server is closed afterwards')
    args=parser.parse_args()
    results=[]
    def record(name,detail):
        results.append(dict(check=name,status='passed',detail=detail));print('PASS:',name,'—',detail)
    required=['docs/01-project-definition.md','docs/02-business-case.md','docs/03-data-inventory-access.md',
      'docs/05-data-understanding.md','docs/06-data-preparation.md','docs/07-task5-descriptive-analysis.md',
      'docs/glossary.md','docs/decisions.md','docs/references.md','docs/literature-notes.md','docs/08-progress-audit.md',
      'src/preprocessing.py','src/descriptive_analysis.py','scripts/run_notebooks.py',
      'reports/results/source_metadata.json','progress.html','analysis.html']
    for name in required:assert (ROOT/name).is_file(),name
    record('Task 1–5 required evidence files',f'{len(required)} explicit paths exist')
    tests=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-v'],cwd=ROOT,capture_output=True,text=True)
    assert tests.returncode==0,tests.stdout+tests.stderr
    count=re.search(r'Ran (\d+) tests?',tests.stderr)
    record('Automated unit tests',(count.group(1) if count else 'All')+' tests passed: chunk statistics, semantics, causality, split safety, transforms and version integrity')
    pages={}
    for name in ['index.html','findings.html','preparation.html','analysis.html','progress.html']:
        p=Page();p.feed((ROOT/name).read_text());assert not p.stack,name;pages[name]=p
    links=0
    for name,p in pages.items():
        for ref in p.links:
            target=urlsplit(ref)
            if target.scheme or target.netloc:continue
            dest=ROOT/unquote(target.path) if target.path else ROOT/name
            assert dest.exists() or (args.write_report and dest==ROOT/'reports/results/progress_check.json'),(name,ref)
            if target.fragment and dest.name in pages:assert target.fragment in pages[dest.name].ids,(name,ref)
            links+=1
    for path in [ROOT/'README.md',ROOT/'data/README.md',*(ROOT/'docs').glob('*.md'),*(ROOT/'presentations').rglob('*.md')]:
        for ref in re.findall(r'\[[^\]]*\]\(([^)]+)\)',path.read_text()):
            if '://' not in ref and not ref.startswith('#'):
                dest=path.parent/unquote(ref.split('#')[0])
                assert dest.exists() or (args.write_report and dest.resolve()==ROOT/'reports/results/progress_check.json'),(str(path.relative_to(ROOT)),ref)
                links+=1
    record('HTML and documentation links',f'{links} local references checked; HTML tags/IDs and image alternatives valid')
    notebook_data=[]
    for name in ['01-data-understanding.ipynb','02-preprocessing.ipynb','03-descriptive-analysis.ipynb']:
        nb=nbformat.read(ROOT/'notebooks'/name,as_version=4);nbformat.validate(nb)
        codes=[c for c in nb.cells if c.cell_type=='code']
        assert all(c.execution_count is not None for c in codes),name
        assert all(o.output_type!='error' for c in codes for o in c.outputs),name
        figures=sum('image/png' in o.get('data',{}) for c in codes for o in c.outputs)
        notebook_data.append(dict(file=name,executed_code_cells=len(codes),embedded_charts=figures))
    record('Executed notebooks',str(sum(n['executed_code_cells'] for n in notebook_data))+' code cells; '+str(sum(n['embedded_charts'] for n in notebook_data))+' embedded figures; no errors')
    summary=json.loads((ROOT/'reports/results/task3_summary.json').read_text())
    cycles=pd.read_csv(ROOT/'reports/results/cycles.csv');eng=pd.read_csv(ROOT/'reports/results/engines.csv')
    stats=pd.read_csv(ROOT/'reports/results/statistics.csv');dictionary=pd.read_csv(ROOT/'reports/results/feature_dictionary.csv')
    assert len(cycles)==summary['totals']['flights']==1542
    assert eng.readings.sum()==cycles.readings.sum()==summary['totals']['readings']==14159058
    assert len(eng)==summary['totals']['engines']==19
    assert stats.rows.sum()==14159058*47
    assert len(stats)==188 and len(dictionary)==47
    assert dictionary.set_index('feature').loc['P2','unit']=='psia'
    assert stats.missing.sum()==stats.infinite.sum()==0
    record('Task 3 full-scan reconciliation','14,159,058 readings, 1,542 flights, 47 fields; no NaN/inf; P2 source corrected')
    manifest=json.loads((ROOT/'reports/results/task4/manifest.json').read_text())
    assert summary['files']==manifest['raw_files'],'Raw identity differs between task exports'
    for name,digest in manifest['code'].items():assert sha256(ROOT/name)==digest,('Code fingerprint stale',name)
    splits=pd.read_csv(ROOT/'reports/results/task4/engine_splits.csv')
    active=splits[splits.split!='quarantine_test_related']
    assert (active.groupby('conservative_group').split.nunique()==1).all()
    assert manifest['matrix_shapes']=={'train':[574,50],'validation':[343,50],'test':[543,50]}
    record('Task 4 policy and fingerprints','Current code/config matched; conservative groups separate; splits 574/343/543 and 82 quarantine')
    if not args.skip_local_data:
        import joblib
        folder=ROOT/'data/processed'/manifest['version_id'];assert verify_version(folder)==manifest
        f=pd.read_csv(folder/'flights_features.csv');catalog=pd.read_csv(folder/'feature_catalog.csv');names=catalog.feature.tolist()
        pipeline=joblib.load(folder/'preprocessor.joblib')
        for split,shape in manifest['matrix_shapes'].items():
            x=pd.read_csv(folder/f'X_{split}.csv');y=pd.read_csv(folder/f'y_{split}.csv');rows=pd.read_csv(folder/f'rows_{split}.csv');selected=f[f.split==split]
            assert list(x.shape)==shape and len(x)==len(y)==len(rows)
            assert np.isfinite(x.to_numpy()).all()
            np.testing.assert_array_equal(y.RUL,selected.RUL)
            np.testing.assert_array_equal(rows[['dataset','unit','cycle']],selected[['dataset','unit','cycle']])
            np.testing.assert_allclose(x,pipeline.transform(selected[names+['dataset']]),atol=1e-8,rtol=1e-8)
        train=f[f.split=='train'];numeric=pipeline.named_transformers_['numeric']
        np.testing.assert_allclose(numeric.named_steps['imputer'].statistics_,train[names].median(),rtol=1e-8,atol=1e-8)
        assert f[names].isna().sum().sum()==57
        record('Local model-ready artifacts','All artifact hashes valid; finite/ordered X,y,rows; train medians verified; matrix transforms reproduced')
        for raw in manifest['raw_files']:
            path=ROOT/'data/raw'/raw['file'];assert path.stat().st_size==raw['bytes']
            if args.raw_hashes:assert sha256(path)==raw['sha256'],path
        record('Raw file identity','Full SHA-256 and sizes match' if args.raw_hashes else 'Sizes match; full hashing explicitly not requested')
    else:results.append(dict(check='Ignored local data',status='skipped',detail='Use a local checkout with raw/prepared files for artifact validation'))
    info=json.loads((ROOT/'reports/results/task5/training_insights.json').read_text())
    prov=json.loads((ROOT/'reports/results/task5/analysis_provenance.json').read_text())
    assert sha256(ROOT/prov['source_path'])==prov['sha256']
    assert sha256(ROOT/'reports/results/cycles.csv')==prov['cycle_export_sha256']
    assert sha256(ROOT/'reports/results/task4/engine_splits.csv')==prov['split_export_sha256']
    assert prov['task4_version']==manifest['version_id']
    reconstructed=pd.read_csv(ROOT/prov['source_path']);actual=training_insights(reconstructed[reconstructed.split=='train'])
    for key in ['rul_mean','t48_r_min','t48_r_max','late_minus_early_T48_K_median']:assert np.isclose(actual[key],info[key],atol=1e-8)
    assert info['training_flights']==574 and info['conservative_groups']==6
    assert len(list((ROOT/'reports/figures/task5').glob('0*.svg')))==6
    record('Task 5 provenance and findings','Tracked source hashes and current Task 4 version match; training insights recalculated; six analysis charts present')
    deck=ROOT/'presentations/milestone/GR05-milestone-draft.pptx'
    ns={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
    with zipfile.ZipFile(deck) as z:
        parts=[n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml',n)]
        assert len(parts)==40
        for part in parts:
            text=' '.join(t.text or '' for t in ET.fromstring(z.read(part)).iter('{'+ns['a']+'}t'))
            assert 'Creators: GR05' in text and 'Presenter proposed:' in text
        assert len([n for n in z.namelist() if re.fullmatch(r'ppt/notesSlides/notesSlide\d+\.xml',n)])==40
    assert len(PdfReader(ROOT/'presentations/milestone/GR05-milestone-draft.pdf').pages)==40
    assert len(PdfReader(ROOT/'presentations/milestone/GR05-milestone-short-route.pdf').pages)==22
    spec=json.loads((ROOT/'presentations/milestone/slide-specification.json').read_text())
    assert '12 Nov: progress/preparation; 19 Nov: milestone presentation.' in spec[2]['bullets']
    forbidden=['Milestone: 12 Nov working date','Working presentation date: **12 November','presentation is tomorrow','P2 definition/unit requires source confirmation']
    for path in [ROOT/'README.md',ROOT/'presentations/milestone/readiness-guide.md',*(ROOT/'docs').glob('*.md'),*(ROOT).glob('*.html')]:
        for phrase in forbidden:assert phrase not in path.read_text(),(path,phrase)
    record('Progress/milestone dates and presentation artifacts','12 Nov progress; 19 Nov milestone; 40 slides with notes/attribution, full and short PDFs')
    for name in ['docs/06-data-preparation.md','docs/08-progress-audit.md','preparation.html']:
        assert manifest['version_id'] in (ROOT/name).read_text(),('Stale generated version',name)
    if args.http_check:
        from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
        from functools import partial
        from threading import Thread
        import urllib.request
        class QuietHandler(SimpleHTTPRequestHandler):
            def log_message(self,*values):pass
        handler=partial(QuietHandler,directory=str(ROOT))
        with ThreadingHTTPServer(('127.0.0.1',0),handler) as server:
            thread=Thread(target=server.serve_forever,daemon=True);thread.start()
            try:
                for name in [*pages,'assets/site.css','assets/findings.css','assets/site.js','assets/findings.js','assets/favicon.svg']:
                    with urllib.request.urlopen(f'http://127.0.0.1:{server.server_port}/{name}',timeout=10) as response:
                        assert response.status==200,name
                        assert response.read(),name
            finally:server.shutdown();thread.join()
        record('Local website HTTP smoke check','Five current pages plus styles/scripts/favicon returned HTTP 200; temporary loopback server closed')
    report=dict(checked_at=datetime.now(ZoneInfo('Europe/Berlin')).isoformat(),status='passed',raw_hashes_checked=args.raw_hashes and not args.skip_local_data,
        local_data_checked=not args.skip_local_data,http_checked=args.http_check,checker_sha256=sha256(Path(__file__)),prepared_version=manifest['version_id'],results=results,notebooks=notebook_data,
        tasks_1_to_5='technical deliverables available for progress review',
        human_actions=['Confirm working roles and speaking allocation','Review explanations and rehearse for 19 November','Preview PPTX in presentation application'],
        limitations=['Original local download-version match/upstream reference checksum not established','Cross-subset independence unresolved','No predictive model trained or operational/business outcomes measured','Static website source checked locally; external deployment not performed'])
    if args.write_report:
        dest=ROOT/'reports/results/progress_check.json';dest.write_text(json.dumps(report,indent=2)+'\n')
        print('Wrote',dest.relative_to(ROOT))
    return 0

if __name__=='__main__':sys.exit(main())
