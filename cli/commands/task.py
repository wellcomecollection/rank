import typer


app = typer.Typer(
    name="task",
    help="Manage tasks running on the rank cluster",
    no_args_is_help=True,
)


@app.command()
def check():
    raise NotImplementedError


@app.command()
def delete():
    raise NotImplementedError
