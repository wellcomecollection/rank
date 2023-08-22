import json

import chevron
from pytest import fixture

import typer
from elasticsearch import Elasticsearch


class RankPlugin:
    def __init__(self, *, context: typer.Context):
        self._client = context.meta["client"]
        self._index = context.meta["index"]
        self._query_template = json.dumps(context.meta["query_template"])

    @fixture(scope="session")
    def client(self) -> Elasticsearch:
        return self._client

    @fixture(scope="session")
    def index(self) -> str:
        return self._index

    @fixture()
    def render_query(self):
        def _render_query(search_terms: str):
            rendered = chevron.render(
                self._query_template, {"query": search_terms}
            )
            return json.loads(rendered)

        return _render_query
