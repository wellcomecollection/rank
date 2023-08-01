import typer

app = typer.Typer()


@app.command()
def hello(name: str):
    print(f"Hello {name}")


# This is here temporarily while there is only one command
# https://typer.tiangolo.com/tutorial/commands/one-or-multiple/#one-command-and-one-callback
@app.callback()
def callback():
    pass
