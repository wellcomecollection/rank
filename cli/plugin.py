import json
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
