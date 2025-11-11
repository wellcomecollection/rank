# rank

A tool for testing search relevance.

## Installation

_Python 3.10_ ([`pyenv`](https://github.com/pyenv/pyenv) recommended) is a prerequisite.

#### For use
You can install with `pip` (or [`pipx`](https://pypa.github.io/pipx/)) just by doing
```
pip install git+https://github.com/wellcomecollection/rank.git
```

#### For development

Install [`uv`](https://docs.astral.sh/uv/getting-started/installation/), then run `uv sync` in the root of the repo. This creates a local `.venv/` with the project and development dependencies.

Either activate the virtual environment (`source .venv/bin/activate`) or prefix commands with `uv run`.

For example to run the works test against the pipeline-prod cluster, you can run the following command:

```console
uv run rank test \
  --content-type=works \
  --cluster=pipeline-prod \
  --query=https://api.wellcomecollection.org/catalogue/v2
```