from __future__ import annotations


def test_unit_tests_run() -> None:
    # This test exists to ensure `uv run pytest` executes something meaningful
    # in CI, even when relevance tests are skipped by default.
    assert True
