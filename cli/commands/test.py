from pathlib import Path

import pytest
import typer
import importlib.util
from typing_extensions import Annotated

from .. import ContentType
from ..plugin import RankPlugin

app = typer.Typer(name="test", help="Run relevance tests")

# This ensures that we get the right path for the relevance tests directory
# regardless of where we are running the tool
relevance_tests_spec = importlib.util.find_spec("cli.relevance_tests")
root_test_directory = Path(relevance_tests_spec.submodule_search_locations[0])


@app.callback(invoke_without_command=True)
def main(
    context: typer.Context,
    test_id: Annotated[
        str,
        typer.Option(
            "--id",
            "--group",
            "-g",
            help="The ID of an individual test (or group of tests) to run.",
            case_sensitive=False,
        ),
    ] = None,
    content_type: Annotated[
        ContentType,
        typer.Option(
            "--content-type",
            "-c",
            help="The content type to run tests for",
            case_sensitive=False,
            show_choices=True,
        ),
    ] = None,
):
    """Run relevance tests"""
    if context.invoked_subcommand is None:
        rank_plugin = RankPlugin(context=context)
        test_directory = root_test_directory
        if content_type:
            test_directory = test_directory / content_type

        if test_id:
            return_code = pytest.main(
                [test_directory, "-k", test_id], plugins=[rank_plugin]
            )
        else:
            return_code = pytest.main([test_directory], plugins=[rank_plugin])
        raise typer.Exit(code=return_code)


@app.command(name="list")
def list_tests():
    """List all tests that can be run"""
    pytest.main(["--collect-only", "--quiet", root_test_directory])
