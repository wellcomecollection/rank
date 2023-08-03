import typer

from .commands import index, test

app = typer.Typer(
    name="rank",
    help="A CLI for measuring search relevance",
    no_args_is_help=True,
    add_completion=False,
)

app.add_typer(test)
app.add_typer(index)
