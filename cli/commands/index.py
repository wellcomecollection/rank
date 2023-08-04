import json
import typer
from ..services.elasticsearch import get_rank_elastic_client
from ..services.aws import get_session
from .. import index_config_directory

app = typer.Typer(
    name="index",
    help="Manage indices in the rank cluster",
    no_args_is_help=True,
)

session = get_session(
    role_arn="arn:aws:iam::760097843905:role/platform-developer"
)

client = get_rank_elastic_client(session)


def index_name_callback(index: str):
    if not client.indices.exists(index=index):
        raise typer.BadParameter(f"{index} does not exist")
    elif index.startswith(".") or (index == "_all"):
        raise typer.BadParameter(f"{index} is a system index")
    return index


@app.command()
def list():
    """List the indices in the rank cluster"""
    valid_indices = [
        index["index"]
        for index in client.cat.indices(format="json", h="index", s="index")
        if not index["index"].startswith(".")
    ]
    typer.echo("\n".join(valid_indices))


@app.command()
def create(
    index: str = typer.Option(
        ...,
        help="The name of the index to create",
        prompt="The name of the index to create",
    ),
    config_path: str = typer.Option(
        None,
        "--config",
        "-c",
        help="Path to a json file containing the index settings and mappings",
    ),
):
    """Create an index in the rank cluster"""
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    if client.indices.exists(index=index):
        raise typer.BadParameter(f"{index} already exists")

    client.indices.create(
        index=index, mappings=config["mappings"], settings=config["settings"]
    )


@app.command()
def update(
    index: str = typer.Option(
        ...,
        help="The name of the index to update",
        prompt="The name of the index to update",
    ),
    config_path: str = typer.Option(
        None,
        "--config",
        "-c",
        help="Path to a json file containing the index settings and mappings",
    ),
):
    """Update an index in the rank cluster"""
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    if not client.indices.exists(index=index):
        raise typer.BadParameter(f"{index} does not exist")

    client.indices.put_settings(index=index, body=config["settings"])
    client.indices.put_mapping(index=index, body=config["mappings"])
    typer.echo(f"Index {index} updated")

    # Update the index to use the new mapping
    if typer.confirm(
        f"Do you want to update the documents in {index} to use the new mapping?"
    ):
        task = client.update_by_query(index=index, wait_for_completion=False)
        typer.echo(f"Update task {task['task']} started")
        typer.echo(
            f"Run `rank task status {task['task']}` to monitor its progress"
        )


@app.command(help="Delete an index")
def delete(
    index: str = typer.Argument(
        ...,
        help="The name of the index to delete",
        callback=index_name_callback,
    )
):
    """Delete an index from the rank cluster"""
    if typer.confirm(f"Are you sure you want to delete {index}?", abort=True):
        client.indices.delete(index=index)
        typer.echo(f"Index {index} deleted")


@app.command()
def get(
    index: str = typer.Argument(
        ...,
        help="The index to get the mappings and settings for",
        callback=index_name_callback,
    )
):
    """Get the mappings and settings for an index in the rank cluster"""
    config = dict(client.indices.get(index=index))[index]
    # only keep the analysis section of the settings
    config["settings"] = config["settings"]["index"]["analysis"]

    config_path = index_config_directory / f"{index}.json"
    with open(config_path, "w") as f:
        f.write(json.dumps(config, indent=2))
    typer.echo(f"Index config written to {config_path}")


@app.command()
def replicate():
    """Replicate an index from a production cluster to the rank cluster"""
    raise NotImplementedError
