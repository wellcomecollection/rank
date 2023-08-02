import json
import re

import boto3
import chevron
import pytest
import requests
from elasticsearch import Elasticsearch

from .services.aws import get_session
from .services.elasticsearch import get_pipeline_elastic_client


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
        self.pipeline_date = re.search(
            r"^works-indexed-(?P<date>\d{4}-\d{2}-\d{2}.?)", self.works_index
        ).group("date")


class RankPlugin:
    def __init__(self, *, role_arn: str, catalogue_api_url: str):
        self.role_arn = role_arn
        self.sut = SearchUnderTest(catalogue_api_url)

    @pytest.fixture(scope="session")
    def aws_session(self) -> boto3.session.Session:
        return get_session(role_arn=self.role_arn)

    @pytest.fixture(scope="session")
    def pipeline_client(self, aws_session) -> Elasticsearch:
        return get_pipeline_elastic_client(
            aws_session, pipeline_date=self.sut.pipeline_date
        )

    @pytest.fixture()
    def works_search(self):
        def _get_search_params(query: str):
            rendered = chevron.render(
                self.sut.works_query_template, {"query": query}
            )
            return {
                "query": json.loads(rendered),
                "index": self.sut.works_index,
            }

        return _get_search_params
