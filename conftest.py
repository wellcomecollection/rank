from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--run-relevance",
        action="store_true",
        default=False,
        help=(
            "Run the integration-style relevance tests under cli/relevance_tests. "
            "These require external services/credentials and are skipped by default."
        ),
    )


def _should_run_relevance(config: pytest.Config) -> bool:
    if config.getoption("--run-relevance"):
        return True
    return os.environ.get("RANK_RUN_RELEVANCE") in {"1", "true", "True"}


def _is_relevance_test(item: Any) -> bool:
    # pytest items typically expose either .path (Path) or .fspath (py.path)
    path = getattr(item, "path", None) or getattr(item, "fspath", None)
    if path is None:
        return False

    try:
        p = Path(str(path)).resolve()
    except Exception:
        return False

    return "cli/relevance_tests" in p.as_posix()


def pytest_collection_modifyitems(
    config: pytest.Config, items: list[pytest.Item]
) -> None:
    if _should_run_relevance(config):
        return

    skip_marker = pytest.mark.skip(
        reason=(
            "Relevance tests are skipped by default. "
            "Use --run-relevance (or set RANK_RUN_RELEVANCE=1) to enable them."
        )
    )

    for item in items:
        if _is_relevance_test(item):
            item.add_marker(skip_marker)
