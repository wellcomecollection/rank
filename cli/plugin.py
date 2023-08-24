import json
import os
import re

import chevron
import typer
from elasticsearch import Elasticsearch
from pytest import fixture, hookimpl


class RankPlugin:
    def __init__(self, *, context: typer.Context):
        self._client = context.meta["client"]
        self._index = context.meta["index"]
        self._query_template = json.dumps(context.meta["query_template"])

    # This is a hack to rewrite test names in the output, excluding their
    # common prefix. This is useful in particular for when rank is installed
    # as a package (ie in the Docker images), where without this hack every
    # test name is prefixed with the `site-packages` location
    common_path_key = pytest.StashKey[str]()

    @hookimpl()
    def pytest_configure(self, config):
        terminal = config.pluginmanager.getplugin("terminal")

        class ShortPathReporter(terminal.TerminalReporter):
            # This modifies the implementation at
            # https://github.com/pytest-dev/pytest/blob/7.4.0/src/_pytest/terminal.py#L426
            def write_fspath_result(
                self, nodeid: str, res, **markup: bool
            ) -> None:
                fspath = self.config.rootpath / nodeid.split("::")[0]
                if self.currentfspath is None or fspath != self.currentfspath:
                    if (
                        self.currentfspath is not None
                        and self._show_progress_info
                    ):
                        self._write_progress_information_filling_space()
                    self.currentfspath = fspath
                    commonpath = self.config.stash[RankPlugin.common_path_key]
                    shortpath = str(fspath.relative_to(commonpath))
                    self._tw.line()
                    self._tw.write(shortpath + " ")
                self._tw.write(res, flush=True, **markup)

        terminal.TerminalReporter = ShortPathReporter

    @hookimpl(tryfirst=True)
    def pytest_collection_modifyitems(self, session, config, items):
        commonpath = os.path.commonpath([item.path for item in items])
        config.stash[RankPlugin.common_path_key] = commonpath

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
