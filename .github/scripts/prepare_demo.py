"""Describe CI scenarios and create small workflows supplementing SANE's demo."""
import json
import os
from pathlib import Path


BASE = [ "action_000", "action_001", "action_015" ]
CASES = {
  "run" : {},
  "single-filter" : {
    "actions" : [],
    "actions_filter" : [ "^action_015$" ]
  },
  "complex-filters" : {
    "pre" : True,
    "actions" : [],
    "actions_filter" : [ r'''^(?:action_0(?:15|16))$(?#quotes"')''', r"^action_00\d$" ],
    "expected" : [ f"action_{i:03d}" for i in range( 10 ) ] + [ "action_015", "action_016" ]
  },
  "multiple-actions" : {
    "actions" : [ "action_015", "action_016" ],
    "expected" : BASE + [ "action_002", "action_016" ]
  },
  "multiple-filters" : {
    "pre" : True,
    "actions" : [],
    "actions_filter" : [ "^action_015$", "^action_016$" ],
    "expected" : BASE + [ "action_002", "action_016" ]
  },
  "mixed-selection" : {
    "pre" : True,
    "actions" : [ "action_015" ],
    "actions_filter" : [ "^action_015$", "^action_016$" ],
    "expected" : BASE + [ "action_002", "action_016" ]
  },
  "multiple-paths" : {
    "paths" : [ "sane-demo/demo", "ci-fixtures/extra" ],
    "actions" : [ "action_015", "extra_action" ],
    "expected" : BASE + [ "extra_action" ]
  },
  "defaults" : {
    "paths" : [ "ci-fixtures/defaults" ],
    "actions" : [],
    "host" : "",
    "args" : "",
    "expected" : [ "default_one", "default_two" ]
  },
  "dry-run" : { "dry_run" : True },
  "patch" : {
    "patch" : {
      "actions" : {
        "action_015" : { "config" : { "arguments" : [ "CI_PATCH_APPLIED" ] } }
      }
    }
  },
  "extra-args" : { "args" : "-s actual_workflow.py --new -ml custom-runner.log" },
  "failure-upload" : {
    "actions" : [ "ci_failure" ],
    "paths" : [ "ci-fixtures/failure" ],
    "args" : "",
    "upload" : True,
    "expected" : [ "ci_failure" ],
    "failure" : True
  },
  "failure-no-upload" : {
    "actions" : [ "ci_failure" ],
    "paths" : [ "ci-fixtures/failure" ],
    "args" : "",
    "expected" : [ "ci_failure" ],
    "failure" : True
  }
}


def scenario( name ):
  return dict(
                {
                  "paths" : [ "sane-demo/demo" ],
                  "actions" : [ "action_015" ],
                  "actions_filter" : [],
                  "host" : "generic",
                  "args" : "-s actual_workflow.py -s workflow.json -s patch.json",
                  "patch" : "",
                  "dry_run" : False,
                  "pre" : False,
                  "upload" : False,
                  "expected" : BASE,
                  "failure" : False
                },
                **CASES[name]
              )


def prepare():
  host = {
    "generic" : {
      "aliases" : [ "." ],
      "default_env" : "generic",
      "environments" : { "generic" : {} }
    }
  }
  for directory, actions in {
    "extra" : { "extra_action" : { "config" : { "command" : "echo", "arguments" : [ "extra_action" ] } } },
    "defaults" : {
      name : { "config" : { "command" : "echo", "arguments" : [ name ] } }
      for name in [ "default_one", "default_two" ]
    },
    "failure" : { "ci_failure" : { "config" : { "command" : "false" } } }
  }.items():
    path = Path( "ci-fixtures" ) / directory
    path.mkdir( parents=True, exist_ok=True )
    data = { "actions" : actions }
    if directory != "extra":
      data["hosts"] = host
    ( path / "workflow.json" ).write_text( json.dumps( data ) )


if __name__ == "__main__":
  prepare()
  config = scenario( os.environ.get( "MODE", "run" ) )
  with open( os.environ["GITHUB_OUTPUT"], "a" ) as output:
    for key, value in config.items():
      if not isinstance( value, str ):
        value = json.dumps( value )
      print( f"{key}={value}", file=output )
