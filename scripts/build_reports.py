"""Regenerate current static reports/pages from executed evidence.

python scripts/build_reports.py [--presentation]
Run scripts/run_notebooks.py first when source data or analysis changed.
"""
from pathlib import Path
import argparse,os,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--presentation',action='store_true');args=parser.parse_args()
    env=os.environ.copy();env.setdefault('MPLCONFIGDIR',str(ROOT/'.cache/matplotlib'))
    commands=['build_task3_report.py','build_task4_report.py','build_task5_report.py','build_progress_report.py']
    if args.presentation:commands.append('build_milestone_presentation.py')
    for name in commands:subprocess.run([sys.executable,str(ROOT/'scripts'/name)],cwd=ROOT,env=env,check=True)
