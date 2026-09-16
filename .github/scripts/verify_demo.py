"""Verify selected actions, persisted state, command output, and dry-run behavior."""
import json
import os
from pathlib import Path

from prepare_demo import scenario


mode   = os.environ["MODE"]
config = scenario( mode )
run_id = os.environ["RUN_ID"]
assert os.environ["OUTCOME"] == ( "failure" if config["failure"] else "success" )
# Expected failures must be tolerated by the workflow, not just match SANE's state.
if "CONCLUSION" in os.environ:
  assert os.environ["CONCLUSION"] == "success", os.environ["CONCLUSION"]

# Failed composite steps may not publish outputs; still inspect their saved results.
if not config["failure"]:
  assert os.environ["SAVE_LOCATION"] == f".{run_id}_saves"
  assert os.environ["LOG_LOCATION"] == f"{run_id}_logs"

save_dir = Path( f".{run_id}_saves" )
log_dir  = Path( f"{run_id}_logs" )
state    = json.loads( ( save_dir / "orchestrator.json" ).read_text() )
assert set( state["actions"] ) == set( config["expected"] ), state["actions"]
assert state["host"] == "generic", state["host"]
assert state["dry_run"] is config["dry_run"]
assert Path( state["save_location"] ).resolve() == save_dir.resolve()
assert Path( state["log_location"] ).resolve() == log_dir.resolve()

runner_log = "custom-runner.log" if mode == "extra-args" else "runner.log"
assert ( log_dir / runner_log ).stat().st_size > 0
if mode == "complex-filters":
  runner_output = ( log_dir / runner_log ).read_text()
  for pattern in config["actions_filter"]:
    assert f"Using action filter '{pattern}'" in runner_output, runner_output

for action_id, result in state["actions"].items():
  assert result["state"] == "finished", ( action_id, result )
  assert result["status"] == ( "failure" if config["failure"] else "success" ), result
  runlog = log_dir / f"{action_id}.runlog"
  if config["dry_run"]:
    assert not runlog.exists(), f"Dry run launched {action_id}"
  elif not config["failure"]:
    marker = "CI_PATCH_APPLIED" if mode == "patch" and action_id == "action_015" else action_id
    output = runlog.read_text()
    assert any( "STDOUT" in line and marker in line for line in output.splitlines() ), output

print( f"Verified {mode}: {len(state['actions'])} expected actions." )
