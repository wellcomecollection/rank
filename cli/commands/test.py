import json
from typing import Optional
from pathlib import Path

import pytest
import typer

from .. import ContentType, Environment, get_pipeline_search_templates
from . import (
    prompt_user_to_choose_an_environment,
    prompt_user_to_choose_a_local_query,
    prompt_user_to_choose_an_index,
    prompt_user_to_choose_a_content_type,
)
from ..services import aws, elasticsearch
from ..plugin import RankPlugin

app = typer.Typer(name="test", help="Run relevance tests")

root_test_dir = Path("cli/relevance_tests/")


@app.callback(invoke_without_command=True)
def main(
    context: typer.Context,
    test_id: Optional[str] = typer.Option(
        help="The ID of an individual test (or group of tests) to run.",
        case_sensitive=False,
        default=None,
    ),
    content_type: Optional[ContentType] = typer.Option(
        help="The content type to run tests for",
        case_sensitive=False,
        show_choices=True,
        default=None,
    ),
    environment: Optional[Environment] = typer.Option(
        help="The environment to run tests against",
        case_sensitive=False,
        show_choices=True,
        default="development",
    ),
    index: Optional[str] = typer.Option(
        help="The index to run tests against",
        case_sensitive=False,
        default=None,
    ),
):
    """Run relevance tests"""
    if context.invoked_subcommand is None:
        context.meta["session"] = aws.get_session(context.meta["role_arn"])
        context.meta["environment"] = prompt_user_to_choose_an_environment(
            environment
        )
        context.meta["content_type"] = prompt_user_to_choose_a_content_type(
            content_type
        )

        if context.meta["environment"] == Environment.DEVELOPMENT:
            context.meta["client"] = elasticsearch.rank_client(context)
            query_template_path = prompt_user_to_choose_a_local_query(
                context=context,
                content_type=context.meta["content_type"],
            )
            with open(query_template_path) as f:
                context.meta["query_template"] = json.load(f)

            context.meta["index"] = prompt_user_to_choose_an_index(
                context, index, content_type=context.meta["content_type"]
            )
        else:
            context.meta["client"] = elasticsearch.pipeline_client(context)
            search_templates = get_pipeline_search_templates(
                context.meta["catalogue_api_url"]
            )
            context.meta["query_template"] = json.loads(
                search_templates[context.meta["content_type"]]["query"]
            )
            context.meta["index"] = search_templates[
                context.meta["content_type"]
            ]["index"]

        rank_plugin = RankPlugin(context=context)

        test_dir = root_test_dir / context.meta["content_type"].value

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
    pytest.main(["--collect-only", "--quiet", root_test_dir])
