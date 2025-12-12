# Repository instructions for Copilot

## Project overview
- `rank` is a Python CLI used to test and compare search relevance for Wellcome Collection search services.
- The CLI entrypoint is `rank` (configured in `pyproject.toml` as `cli.main:app`).
- The CLI is built with Typer.

## Tech stack & tooling
- Python: 3.12 (see `.python-version` and `pyproject.toml`)
- Dependency management: **uv** (lockfile is `uv.lock`)
- Build backend: hatchling
- Lint/format: **ruff** (no black/isort)
- Type checking: **mypy** (configured to type-check `cli/`)
- Tests: **pytest**

## Repository layout
- `cli/`: main application code
- `cli/commands/`: Typer subcommands (`rank test`, `rank search`, `rank index`, …)
- `cli/relevance_tests/`: integration-style relevance tests (talk to external services)
- `tests/`: fast unit tests that should run in CI
- `docs/`: user docs and workflows

## Development workflow
- Prefer `uv run …` for running tools.
- If you change dependencies, update `pyproject.toml` and regenerate the lockfile.
- Avoid adding formatting/lint tooling that overlaps with ruff.

## Tests (important)
- `cli/relevance_tests/**` are **skipped by default** when running plain `pytest`.
  - This is intentional so `uv run pytest` can run in CI without AWS/Elasticsearch.
- To run relevance tests explicitly:
  - pass `--run-relevance`, or
  - set `RANK_RUN_RELEVANCE=1`.
- The `rank test` CLI command already enables relevance tests when it invokes pytest.

## Quality checks to run before opening a PR
Run these from the repo root:
- `uv run ruff format --check .`
- `uv run ruff check .`
- `uv run mypy .`
- `uv run pytest`

## Coding guidelines
- Make small, focused changes and keep diffs minimal.
- Keep unit tests hermetic (no network calls) unless a test is explicitly marked/gated as a relevance test.
- Prefer clear types over `Any`; when interacting with untyped third-party libraries, use narrow, well-placed ignores.
