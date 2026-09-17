# sane-workflows-action
GitHub Action for SANE Workflows

This is a simple action to facilitate running SANE Workflows, but can also be useful for seeing how one could run workflows themselves if they need more complex management of their environment.

See `actions.yml` file for inputs. Any list or dict is expected to be input as a JSON string

## Requirements
 * Your project uses [sane_workflows](https://github.com/islas/sane_workflows)
 * Your workflows can be initiated in a python environment that `venv` can support (e.g. `pyvenv` not supported)

## Usage
This is just a simplified wrapper on setting up a python virtual environment and then running a workflow. The only required inputs are `id` and `paths` to note where your workflow is. This will run `sane_runner` with `-r` by default and construct the remaining options based on any other inputs you provide.

## Log uploads

Set `upload` to one of these strings (`none`, `always`, `on_failure`) to control when workflow artifacts are uploaded


## Outputs
Two output variables are provided: `save_location` is `.${{ inputs.id }}_saves` (a hidden directory), and `log_location` is `${{ inputs.id }}_logs`.

## CI

[The CI workflow](.github/workflows/ci.yml) runs on pushes, pull requests, and manual dispatch on Python 3.10 and 3.13. It sparse-checks out SANE's `demo/` directory from its default branch, independently of the composite action revision and installed package version.

The scenario matrix covers:

- Single and multiple action IDs, single and multiple regex filters (including quotes, groups, and backslashes), and overlapping IDs/filters.
- Multiple workflow paths, with an additional action that exists only in the second path.
- Default action selection and automatic host discovery, plus explicit host selection.
- Dry runs, JSON patches, extra runner arguments, and save/log outputs.
- All three upload policies on both successful and failed runs; CI downloads expected artifacts and checks that no artifact was created otherwise. Invalid policies (including the old boolean values) must fail before installation.

Only `actual_workflow.py` is loaded from the upstream demo. Small generated local workflows provide additional-path, default-selection, and failure cases without HPC dependencies. Assertions check the exact action set (including dependencies), saved status, and actual command output.

Environment jobs cover custom virtual environments, multiple Python dependencies, `upgrade` on/off, `pre`, an explicit package version, and cache misses/hits with both default and custom cache IDs. Each job resolves the explicit version from its initial installation, without tying it to a repository revision. Cache tests save the environment, move the local copy away, and require restoration to run successfully without installing deliberately invalid dependencies.

Ordinary scenarios install the default latest stable package. Multiple-filter and mixed-selection scenarios enable `pre`, because SANE 1.1.0 only honors one filter and multiple-filter support is currently in the prerelease. Failed jobs retain logs and saved state for diagnosis.

Filter JSON is decoded and joined in the step environment before Bash prefixes `-f`. Quotes and regex metacharacters are preserved as data, and filename expansion is disabled. Filters must not contain literal whitespace with this scalar argument approach; use regex escapes such as `\s` or `\x20` to match spaces.
