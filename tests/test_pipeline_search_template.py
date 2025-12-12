from __future__ import annotations

from typing import Any

import pytest

from cli import ContentType, get_pipeline_search_template


class _FakeResponse:
    def __init__(self, payload: dict[str, Any]):
        self._payload = payload

    def json(self) -> dict[str, Any]:
        return self._payload


def test_get_pipeline_search_template_extracts_index_date(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_get(url: str, timeout: int) -> _FakeResponse:  # noqa: ARG001
        return _FakeResponse(
            {
                "templates": [
                    {
                        "index": "works-indexed-2025-10-02",
                        "pipeline": "2025-10-02",
                        "query": '{"query": {"match_all": {}}}',
                    }
                ]
            }
        )

    monkeypatch.setattr("cli.requests.get", fake_get)

    tpl = get_pipeline_search_template(
        api_url="https://example.invalid/catalogue/v2",
        content_type=ContentType.works,
    )

    assert tpl["index"] == "works-indexed-2025-10-02"
    assert tpl["pipeline_date"] == "2025-10-02"
    assert tpl["index_date"] == "2025-10-02"


def test_get_pipeline_search_template_raises_on_unexpected_index_format(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_get(url: str, timeout: int) -> _FakeResponse:  # noqa: ARG001
        return _FakeResponse(
            {
                "templates": [
                    {
                        "index": "works-current",
                        "pipeline": "2025-10-02",
                        "query": "{}",
                    }
                ]
            }
        )

    monkeypatch.setattr("cli.requests.get", fake_get)

    with pytest.raises(ValueError, match="Unexpected index format"):
        get_pipeline_search_template(
            api_url="https://example.invalid/catalogue/v2",
            content_type=ContentType.works,
        )
