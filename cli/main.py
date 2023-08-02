import pytest
import typer
from typing_extensions import Annotated

from . import ContentType, root_test_directory

app = typer.Typer(
    name="rank",
    help="A CLI for measuring search relevance",
    no_args_is_help=True,
    add_completion=False,
)


@app.command()
def hello(name: str):
    print(f"Hello {name}")


@app.command(help="Run the relevance tests")
def test(
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
    test_directory = root_test_directory
    if content_type:
        test_directory = test_directory / content_type

    if test_id:
        return_code = pytest.main([test_directory, "-k", test_id])
    else:
        return_code = pytest.main([test_directory])

    raise typer.Exit(code=return_code)
