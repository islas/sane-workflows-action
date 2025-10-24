# sane-workflows-action
GitHub Action for SANE Workflows

This is a simple action to facilitate running SANE Workflows, but can also be useful for seeing how one could run workflows themselves if they need more complex management of their environment.

See `actions.yml` file for inputs. Any list or dict is expected to be input as a JSON string

## Requirements
 * Your project uses [sane_workflows](https://github.com/islas/sane_workflows)
 * Your workflows can be initiated in a python environment that `venv` can support (e.g. `pyvenv` not supported)

## Usage
This is just a simplified wrapper on setting up a python virtual environment and then running a workflow. The only required inputs are `id` and `paths` to note where your workflow is. This will run `sane_runner` with `-r` and construct the remaining options based on any other inputs you provide.
