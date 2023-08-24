import json
import os
import re

import boto3
import chevron
import pytest
import requests
import typer
from elasticsearch import Elasticsearch

from .services import aws, elasticsearch


def get_pipeline_search_templates(catalogue_api_url: str) -> dict:
    search_templates = requests.get(
        f"{catalogue_api_url}/search-templates.json",
        timeout=10,
    ).json()["templates"]

    works = next(
        template
        for template in search_templates
        if template["index"].startswith("works")
    )
    images = next(
        template
        for template in search_templates
        if template["index"].startswith("images")
    )

    return {
        "works": {
            "index": works["index"],
            "index_date": re.search(
                r"^works-indexed-(?P<date>\d{4}-\d{2}-\d{2}.?)",
                works["index"],
            ).group("date"),
            "query": works["query"],
        },
        "images": {
            "index": images["index"],
            "index_date": re.search(
                r"^images-indexed-(?P<date>\d{4}-\d{2}-\d{2}.?)",
                images["index"],
            ).group("date"),
            "query": images["query"],
        },
    }


class SearchUnderTest:
    pipeline_date: str
    works_query_template: str
    works_index: str
    images_query_template: str
    images_index: str

    def __init__(self, catalogue_api_url: str):
        search_templates = get_pipeline_search_templates(catalogue_api_url)
        self.pipeline_date = search_templates["works"]["index_date"]
        self.works_query_template = search_templates["works"]["query"]
        self.works_index = search_templates["works"]["index"]
        self.images_query_template = search_templates["images"]["query"]
        self.images_index = search_templates["images"]["index"]


class RankPlugin:
    def __init__(self, *, context: typer.Context):
        self.role_arn = context.meta["role_arn"]
        self.catalogue_api_url = context.meta["catalogue_api_url"]
        self.sut = SearchUnderTest(self.catalogue_api_url)

    # This is a hack to rewrite test names in the output, excluding their
    # common prefix. This is useful in particular for when rank is installed
    # as a package (ie in the Docker images), where without this hack every
    # test name is prefixed with the `site-packages` location
    common_path_key = pytest.StashKey[str]()

    @pytest.hookimpl()
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

    @pytest.hookimpl(tryfirst=True)
    def pytest_collection_modifyitems(self, session, config, items):
        commonpath = os.path.commonpath([item.path for item in items])
        config.stash[RankPlugin.common_path_key] = commonpath

    @pytest.fixture(scope="session")
    def aws_session(self) -> boto3.session.Session:
        return aws.get_session(self.role_arn)

    @pytest.fixture(scope="session")
    def pipeline_client(self, aws_session) -> Elasticsearch:
        return elasticsearch.pipeline_client(
            aws_session, pipeline_date=self.sut.pipeline_date
        )

    @pytest.fixture()
    def works_search(self):
        def _get_search_params(search_terms: str):
            rendered = chevron.render(
                self.sut.works_query_template, {"query": search_terms}
            )
            return {
                "query": json.loads(rendered),
                "index": self.sut.works_index,
            }

        return _get_search_params

    @pytest.fixture()
    def images_search(self):
        def _get_search_params(search_terms: str):
            rendered = chevron.render(
                self.sut.images_query_template, {"query": search_terms}
            )
            return {
                "query": json.loads(rendered),
                "index": self.sut.images_index,
            }

        return _get_search_params
