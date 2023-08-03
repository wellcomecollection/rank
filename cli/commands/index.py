import typer


app = typer.Typer(
    name="index",
    help="Manage the rank cluster and its indexes",
    no_args_is_help=True,
)


@app.command()
def list():
    raise NotImplementedError


@app.command()
def create():
    raise NotImplementedError


@app.command()
def update():
    raise NotImplementedError


@app.command()
def delete():
    raise NotImplementedError


@app.command()
def get():
    raise NotImplementedError


@app.command()
def replicate():
    raise NotImplementedError
