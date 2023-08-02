import pytest
import typer

from .rank_plugin import RankPlugin

app = typer.Typer(
    name="rank",
    help="A CLI for measuring search relevance",
    no_args_is_help=True,
    add_completion=False,
)

test_app = typer.Typer(no_args_is_help=True)
app.add_typer(test_app, name="test")


@test_app.command()
def run():
    rank_plugin = RankPlugin(
        role_arn="arn:aws:iam::760097843905:role/platform-developer",
        catalogue_api_url="https://api.wellcomecollection.org/catalogue/v2",
    )
    return_code = pytest.main(["cli/relevance_tests/"], plugins=[rank_plugin])
    raise typer.Exit(code=return_code)


@test_app.command()
def list():
    pytest.main(["--collect-only", "--quiet", "cli/relevance_tests/"])
