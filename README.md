# rank

A tool for testing search relevance.

## Installation

_Python 3.12_ ([`pyenv`](https://github.com/pyenv/pyenv) recommended) is a prerequisite.

#### For use
You can install with `pip` (or [`pipx`](https://pypa.github.io/pipx/)) just by doing
```
pip install git+https://github.com/wellcomecollection/rank.git
```

#### For development

Install [`uv`](https://docs.astral.sh/uv/getting-started/installation/), then run `uv sync` in the root of the repo. This creates a local `.venv/` with the project and development dependencies.

Either activate the virtual environment (`source .venv/bin/activate`) or prefix commands with `uv run`.

## Usage

Note that the tool uses the Wellcome Collection Catalogue `_elasticConfig` endpoint to determine which index to query against. The `--query` parameter should point to the base URL of the API you want to test against.

See: https://api.wellcomecollection.org/catalogue/v2/_elasticConfig

To run the works test against the pipeline-prod cluster, you can run the following command:

```console
uv run rank test \
  --content-type=works \
  --cluster=pipeline-prod \
  --query=https://api.wellcomecollection.org/catalogue/v2
```

Or to target a specific pipeline date:

```console
uv run rank test \
  --content-type=works \
  --pipeline-date=2025-10-02 \
  --query=https://api.wellcomecollection.org/catalogue/v2
```

## Deploying the Docker image (for local testing)

`rank` is also published as a Docker image in our private ECR registry. There’s a helper script to build and push an image tag for you:

```console
./scripts/deploy_image.sh
```

By default this pushes the tag `dev`:

- `756629837203.dkr.ecr.eu-west-1.amazonaws.com/weco/rank:dev`

To push a different tag:

```console
./scripts/deploy_image.sh --tag my-tag
```

### Important: the `latest` tag is used by CI in other projects

Other projects run `rank` in CI using the image tag `latest`:

- `756629837203.dkr.ecr.eu-west-1.amazonaws.com/weco/rank:latest`

Only push `latest` when you intentionally want to update what those projects will run in CI.

### Prerequisites

- Docker (with `buildx` available)
- AWS credentials with access to the ECR repositories
- The AWS CLI profile `catalogue-developer` (as referenced in `scripts/deploy_image.sh`)
