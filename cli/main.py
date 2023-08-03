import typer

from .commands import index, search, task, test

app = typer.Typer(
    name="rank",
    help="A CLI for measuring search relevance",
    no_args_is_help=True,
    add_completion=False,
)

app.add_typer(test.app)
app.add_typer(index.app)
app.add_typer(search.app)
app.add_typer(task.app)
