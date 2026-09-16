# sane-workflows-action
GitHub Action for SANE Workflows

This is a simple action to facilitate running SANE Workflows, but can also be useful for seeing how one could run workflows themselves if they need more complex management of their environment.

See `actions.yml` file for inputs. Any list or dict is expected to be input as a JSON string

## Requirements
 * Your project uses [sane_workflows](https://github.com/islas/sane_workflows)
 * Your workflows can be initiated in a python environment that `venv` can support (e.g. `pyvenv` not supported)

## Usage
This is just a simplified wrapper on setting up a python virtual environment and then running a workflow. The only required inputs are `id` and `paths` to note where your workflow is. This will run `sane_runner` with `-r` by default and construct the remaining options based on any other inputs you provide.

## Outputs
Two output variables are provided: `save_location` is `.${{ inputs.id }}_saves` (a hidden directory), and `log_location` is `${{ inputs.id }}_logs`.

## CI

[The CI workflow](.github/workflows/ci.yml) runs on pushes, pull requests, and manual dispatch. It tests the local composite action on Python 3.10 and 3.13 using a sparse checkout of SANE's `demo/` directory from SANE's default branch. The composite action uses its default package version (`latest`). The action revision, upstream demo revision, and installed package version are independent.

Only `actual_workflow.py` is loaded, so the test needs no HPC scheduler or external services. CI selects `action_015` by ID and by regex in separate runs, verifies that its two dependencies also succeed, and checks dry-run behavior and the reported save/log paths. Failed jobs upload logs and saved state for diagnosis.
