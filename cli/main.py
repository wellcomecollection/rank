import pytest
import typer

app = typer.Typer(
    name="rank",
    help="A CLI for measuring search relevance",
    no_args_is_help=True,
    add_completion=False,
)


@app.command()
def hello(name: str):
    print(f"Hello {name}")


@app.command()
def test():
    return_code = pytest.main(["cli/relevance_tests/"])
    raise typer.Exit(code=return_code)
