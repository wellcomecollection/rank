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

## Usage

Note that the tools uses the Wellcome Collection Catalogue `_elasticConfig` endpoint to determine which index to query against. The `--query` parameter should point to the base URL of the API you want to test against.

See: https://api.wellcomecollection.org/catalogue/v2/_elasticConfig

To run the works test against the pipeline-prod cluster, you can run the following command:

```console
uv run rank test \
  --content-type=works \
  --cluster=pipeline-prod \
  --query=https://api.wellcomecollection.org/catalogue/v2
```

Or to taret a specific pipeline date:

```console
uv run rank test \
  --content-type=works \
  --pipeline-date=2025-10-02 \
  --query=https://api.wellcomecollection.org/catalogue/v2
```