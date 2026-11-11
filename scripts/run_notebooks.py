"""Execute the project's Task 3–5 notebooks reproducibly, from any directory.

Run: python scripts/run_notebooks.py --tasks 3 4 5
A local Jupyter kernel requires loopback access. Large raw files are read only.
"""
from pathlib import Path
import argparse,os,sys
import nbformat
from nbclient import NotebookClient
ROOT=Path(__file__).resolve().parents[1]
NOTEBOOKS={3:'01-data-understanding.ipynb',4:'02-preprocessing.ipynb',5:'03-descriptive-analysis.ipynb'}

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--tasks',nargs='+',type=int,choices=NOTEBOOKS,default=[3,4,5])
 parser.add_argument('--timeout',type=int,default=600,help='Seconds per code cell')
 args=parser.parse_args()
 cache=ROOT/'.cache';cache.mkdir(exist_ok=True)
 for key,sub in [('MPLCONFIGDIR','matplotlib'),('IPYTHONDIR','ipython'),('JUPYTER_DATA_DIR','jupyter/data'),('JUPYTER_CONFIG_DIR','jupyter/config'),('JUPYTER_RUNTIME_DIR','jupyter/runtime')]:
  path=cache/sub;path.mkdir(parents=True,exist_ok=True);os.environ.setdefault(key,str(path))
 for task in sorted(set(args.tasks)):
  path=ROOT/'notebooks'/NOTEBOOKS[task];nb=nbformat.read(path,as_version=4)
  nbformat.validate(nb)
  print(f'Task {task}: executing {path.name}',flush=True)
  def progress(cell,cell_index,**kwargs):print(f'  executed code cell at position {cell_index}',flush=True)
  client=NotebookClient(nb,timeout=args.timeout,kernel_name='python3',resources={'metadata':{'path':str(ROOT)}},on_cell_executed=progress)
  try:client.execute()
  finally:nbformat.write(nb,path)
  print(f'Task {task}: saved executed notebook',flush=True)
 return 0

if __name__=='__main__':sys.exit(main())
