import typer


index_app = typer.Typer(
    name="index",
    help="Manage the rank cluster and its indexes",
    no_args_is_help=True,
)

@index_app.command(help="hello world")
def hello():
    typer.echo("hello world")
