import json
import os
from typing import Optional
from urllib.parse import urlparse
from pathlib import Path

import pytest
import typer
import importlib.util

from .. import (
    ContentType,
    Cluster,
    get_pipeline_search_template,
    production_api_url,
    stage_api_url,
)
from . import (
    prompt_user_to_choose_a_local_query,
    prompt_user_to_choose_an_index,
)
from ..services import aws, elasticsearch
from ..plugin import RankPlugin

app = typer.Typer(name="test", help="Run relevance tests")

# This ensures that we get the right path for the relevance tests directory
# regardless of where we are running the tool
relevance_tests_spec = importlib.util.find_spec("cli.relevance_tests")
root_test_directory = Path(relevance_tests_spec.submodule_search_locations[0])


@app.callback(invoke_without_command=True)
def main(
    context: typer.Context,
    test_id: Optional[str] = typer.Option(
        help="The ID of an individual test (or group of tests) to run.",
        case_sensitive=False,
        default=None,
    ),
    content_type: ContentType = typer.Option(
        help="The content type to run tests for",
        show_choices=True,
        case_sensitive=False,
        prompt=True,
        default=None,
    ),
    query: Optional[str] = typer.Option(
        help="The query to test: a local file path or a URL of catalogue API search templates",
        default=None,
    ),
    index: Optional[str] = typer.Option(
        help="The index to run tests against",
        case_sensitive=False,
        default=None,
    ),
    cluster: Optional[Cluster] = typer.Option(
        help="The ElasticSearch cluster on which to run test queries",
        show_choices=True,
        case_sensitive=False,
        default=None,
    ),
    pipeline_date: Optional[str] = typer.Option(
        help="An override for the pipeline date when a pipeline cluster is selected",
        default=None,
    ),
):
    """Run relevance tests"""
    if context.invoked_subcommand is None:
        context.meta["session"] = aws.get_session(context.meta["role_arn"])
        context.meta["content_type"] = content_type
        if str(urlparse(query).scheme).startswith("http"):
            search_template = get_pipeline_search_template(
                api_url=query, content_type=context.meta["content_type"]
            )
            index = search_template["index"]
            query = search_template["query"]
        elif query and os.path.isfile(query):
            with open(query) as file_contents:
                query = file_contents.read()
        else:
            query_path = prompt_user_to_choose_a_local_query(
                query, content_type=context.meta["content_type"]
            )
            with open(query_path, "r", encoding="utf-8") as f:
                query = f.read()

        if pipeline_date:
            index = (
                index if index else f"{content_type}-indexed-{pipeline_date}"
            )
            context.meta["client"] = elasticsearch.pipeline_client(
                context=context, pipeline_date=pipeline_date
            )
        elif cluster == Cluster.pipeline_prod:
            prod_template = get_pipeline_search_template(
                production_api_url, context.meta["content_type"]
            )
            index = (
                index
                if index
                else f"{content_type}-indexed-{prod_template['index_date']}"
            )
            context.meta["client"] = elasticsearch.pipeline_client(
                context=context, pipeline_date=prod_template["index_date"]
            )
        elif cluster == Cluster.pipeline_stage:
            stage_template = get_pipeline_search_template(
                stage_api_url, context.meta["content_type"]
            )
            index = (
                index
                if index
                else f"{content_type}-indexed-{stage_template['index_date']}"
            )
            context.meta["client"] = elasticsearch.pipeline_client(
                context=context, pipeline_date=stage_template["index_date"]
            )
        elif cluster == Cluster.rank:
            context.meta["client"] = elasticsearch.rank_client(context)

        context.meta["index"] = prompt_user_to_choose_an_index(
            client=context.meta["client"],
            index=index,
            content_type=context.meta["content_type"],
        )

        try:
            context.meta["query_template"] = json.loads(query)
        except json.JSONDecodeError:
            raise ValueError("The query did not contain valid JSON")

        rank_plugin = RankPlugin(context=context)
        test_dir = root_test_directory / context.meta["content_type"].value

        if test_id:
            return_code = pytest.main(
                [test_dir, "-k", test_id], plugins=[rank_plugin]
            )

        else:
            return_code = pytest.main([test_dir], plugins=[rank_plugin])

        raise typer.Exit(code=return_code)


@app.command(name="list")
def list_tests():
    """List all tests that can be run"""
    pytest.main(["--collect-only", "--quiet", root_test_directory])
