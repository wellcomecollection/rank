import pytest
import typer
from typing_extensions import Annotated
from pathlib import Path
import importlib.util

from .. import ContentType, catalogue_api_url

from ..plugin import RankPlugin

app = typer.Typer(name="test", help="Run relevance tests")

root_test_directory = Path(
    importlib.util.find_spec("cli.relevance_tests").submodule_search_locations[0]
)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
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
    if ctx.invoked_subcommand is None:
        rank_plugin = RankPlugin(
            role_arn="arn:aws:iam::760097843905:role/platform-developer",
            catalogue_api_url=catalogue_api_url,
        )

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


@app.command()
def list():
    """List all tests that can be run"""
    pytest.main(["--collect-only", "--quiet", root_test_directory])
