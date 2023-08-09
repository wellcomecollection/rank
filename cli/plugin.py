import json
import re

import boto3
import chevron
import pytest
import requests
import typer
from elasticsearch import Elasticsearch

from . import catalogue_api_url
from .services import aws, elasticsearch


class SearchUnderTest:
    pipeline_date: str
    works_query_template: str
    works_index: str

    def __init__(self, catalogue_api_url: str):
        search_templates = requests.get(
            f"{catalogue_api_url}/search-templates.json"
        ).json()["templates"]

        works = next(
            template
            for template in search_templates
            if template["index"].startswith("works")
        )
        self.works_query_template = works["query"]
        self.works_index = works["index"]

        images = next(
            template
            for template in search_templates
            if template["index"].startswith("images")
        )
        self.images_query_template = images["query"]
        self.images_index = images["index"]

        self.pipeline_date = re.search(
            r"^works-indexed-(?P<date>\d{4}-\d{2}-\d{2}.?)", self.works_index
        ).group("date")


class RankPlugin:
    def __init__(self, *, context: typer.Context):
        self.role_arn = context.meta["role_arn"]
        self.sut = SearchUnderTest(catalogue_api_url)

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
