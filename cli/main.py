import typer

from . import __version__, role_arn
from .commands import index, query, search, task, test

app = typer.Typer(
    name="rank",
    help="A CLI for measuring search relevance",
    no_args_is_help=True,
    add_completion=False,
)


@app.callback()
def callback(context: typer.Context):
    context.meta["role_arn"] = role_arn


app.add_typer(test.app)
app.add_typer(index.app)
app.add_typer(search.app)
app.add_typer(task.app)
app.add_typer(query.app)


@app.command()
def version():
    typer.echo(f"Rank CLI version {__version__}")
