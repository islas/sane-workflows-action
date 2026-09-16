"""Check observable results of the SANE demo integration test."""

import json
import os
from pathlib import Path


mode = os.environ["MODE"]
save_output = os.environ["SAVE_LOCATION"]
log_output = os.environ["LOG_LOCATION"]
assert save_output == f".demo-{mode}_saves", save_output
assert log_output == f"demo-{mode}_logs", log_output
save_dir = Path(save_output)
log_dir = Path(log_output)
state = json.loads((save_dir / "orchestrator.json").read_text())

expected = {"action_000", "action_001", "action_015"}
assert set(state["actions"]) == expected, state["actions"]
assert state["host"] == "generic", state["host"]
assert state["dry_run"] is (mode == "dry-run"), state["dry_run"]
assert Path(state["save_location"]).resolve() == save_dir.resolve()
assert Path(state["log_location"]).resolve() == log_dir.resolve()
assert (log_dir / "runner.log").stat().st_size > 0

for action_id, result in state["actions"].items():
    assert result["state"] == "finished", (action_id, result)
    assert result["status"] == "success", (action_id, result)
    runlog = log_dir / f"{action_id}.runlog"
    if mode == "dry-run":
        assert not runlog.exists(), f"Dry run launched {action_id}"
    else:
        # Require actual command output, not just a successful planning pass.
        output = runlog.read_text()
        assert any("STDOUT" in line and action_id in line
                   for line in output.splitlines()), output

print(f"Verified {mode}: selected action and both dependencies succeeded.")
