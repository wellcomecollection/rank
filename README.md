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

Install [`poetry`](https://python-poetry.org/docs/#installation), then run `poetry install` in the root of the repo. You can run the command with `poetry run rank`. 

For example to run the works test against the pipeline-prod cluster, you can run the following command:

```console
poetry run rank test \
  --content-type=works \
  --cluster=pipeline-prod \
  --query=https://api.wellcomecollection.org/catalogue/v2
```