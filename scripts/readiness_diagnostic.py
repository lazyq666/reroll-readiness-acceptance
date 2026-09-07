import json, re, sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import tests.test_live_collaboration_acceptance_cli as module
original=module.subprocess.run

def observed(*args,**kwargs):
 result=original(*args,**kwargs)
 if result.returncode and args and str(module.SCRIPT) in args[0]:
  try:
   directory=Path(json.loads(result.stdout)['report_directory'])
   summary=json.loads((directory/'summary.json').read_text())
   safe={key:summary.get(key) for key in ('status','robot_mutation_count','robot_ack_p95_ms','robot_ack_p99_ms','ack_p95_gate_ms','ack_p99_gate_ms','realtime_revision_gap_count','realtime_resync_count','final_node_projection_consistent','operation_ids_complete')}
   safe['reasons']=[reason if re.fullmatch(r'[a-z0-9_]+',reason) else 'unclassified' for reason in summary.get('reasons',[])]
   print('Failure metrics:',json.dumps(safe),flush=True)
  except (ValueError,KeyError,OSError):print('No structured CLI report',flush=True)
 return result
module.subprocess.run=observed
name='test_existing_service_runs_robot_mutations_without_generation_and_cleans_exact_objects'
for index in range(30):
 result=unittest.TestResult()
 module.LiveCollaborationAcceptanceCliTests(name).run(result)
 print('Probe',index+1,'passed' if result.wasSuccessful() else 'failed',flush=True)
 if not result.wasSuccessful():
  for _,trace in result.failures+result.errors:
   print('Failure location:',re.findall(r'line (\d+), in',trace)[-3:])
   print('Failure assertion:',trace.splitlines()[-1][:400].replace('admin-secret-value','<redacted>'))
  raise SystemExit(1)
