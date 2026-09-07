import json, re, sys, unittest, os
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
   print('READINESS_DIAGNOSTIC='+json.dumps(safe),flush=True)
  except (ValueError,KeyError,OSError):print('No structured CLI report',flush=True)
 return result
module.subprocess.run=observed
import scripts.readiness_tests as runner
raise SystemExit(runner.main())
