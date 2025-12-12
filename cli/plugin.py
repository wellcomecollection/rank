import json
import os
from typing import Any, cast

import chevron
import typer
from elasticsearch import Elasticsearch
from pytest import StashKey, fixture, hookimpl

from _pytest.terminal import TerminalReporter


class RankPlugin:
    def __init__(self, *, context: typer.Context):
        self._client = context.meta["client"]
        self._index = context.meta["index"]
        self._query_template = json.dumps(context.meta["query_template"])

    # This is a hack to rewrite test names in the output, excluding their
    # common prefix. This is useful in particular for when rank is installed
    # as a package (ie in the Docker images), where without this hack every
    # test name is prefixed with the `site-packages` location
    common_path_key = StashKey[str]()

    @hookimpl()
    def pytest_configure(self, config):
        terminal_plugin = config.pluginmanager.getplugin("terminal")
        if terminal_plugin is None:
            return

        terminal = cast(Any, terminal_plugin)

        # pytest's stubs mark TerminalReporter as @final, but we intentionally
        # monkeypatch it here. Keeping the base class as Any avoids mypy
        # complaining about subclassing a final class.
        class ShortPathReporter(TerminalReporter):  # type: ignore[misc]
            currentfspath: Any | None
            _show_progress_info: Any
            _tw: Any

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
        commonpath = os.path.commonpath([str(item.path) for item in items])
        config.stash[RankPlugin.common_path_key] = commonpath

    @fixture(scope="session")
    def client(self) -> Elasticsearch:
        return self._client

    @fixture(scope="session")
    def index(self) -> str:
        return self._index

    @fixture()
    def stable_sort_key(self):
        return "query.id"

    @fixture()
    def render_query(self):
        def _render_query(search_terms: str):
            rendered = chevron.render(
                self._query_template, {"query": search_terms}
            )
            return json.loads(rendered)

        return _render_query
