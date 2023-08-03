import typer


app = typer.Typer(
    name="search",
    help="Run searches against the rank cluster",
)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
):
    if ctx.invoked_subcommand is None:
        raise NotImplementedError


@app.command()
def get_terms():
    raise NotImplementedError


@app.command()
def compare():
    raise NotImplementedError
