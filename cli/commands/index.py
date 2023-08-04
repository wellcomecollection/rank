from typing import Optional
import json
import typer
from ..services.elasticsearch import get_rank_elastic_client
from ..services.aws import get_session
from .. import index_config_directory
import beaupy

app = typer.Typer(
    name="index",
    help="Manage indices in the rank cluster",
    no_args_is_help=True,
)

session = get_session(
    role_arn="arn:aws:iam::760097843905:role/platform-developer"
)

client = get_rank_elastic_client(session)

def get_valid_indices():
    return [
        index["index"]
        for index in client.cat.indices(format="json", h="index", s="index")
        if not index["index"].startswith(".")
    ]

def get_valid_configs():
    return [p for p in index_config_directory.glob("*.json")]


def prompt_user_to_choose_a_remote_index(index: Optional[str]) -> str:
    if index is None:
        typer.echo("Select an index")
        valid_indices = get_valid_indices()
        index = beaupy.select(valid_indices)
    else:
        if not client.indices.exists(index=index):
            raise typer.BadParameter(f"{index} does not exist")
        elif index.startswith(".") or (index == "_all"):
            raise typer.BadParameter(f"{index} is a system index")
    return index

def prompt_user_to_choose_a_local_config(config_path: Optional[str]) -> str:
    if config_path is None:
        typer.echo("Select a config file")
        valid_configs = get_valid_configs()
        config_path = beaupy.select(
            valid_configs,
            preprocessor=lambda x: x.stem,
        )
    return config_path

def raise_if_index_already_exists(index: str):
    if client.indices.exists(index=index):
        raise typer.BadParameter(f"{index} already exists")
    return index


@app.command()
def list():
    """List the indices in the rank cluster"""
    valid_indices = get_valid_indices()
    typer.echo("\n".join(valid_indices))


@app.command()
def create(
    index: str = typer.Option(
        None,
        help="The name of the index to create",
        prompt="The name of the index to create",
        callback=raise_if_index_already_exists,
    ),
    config_path: Optional[str] = typer.Option(
        None,
        help=(
            "Path to a json file containing the index settings and mappings. "
            "If a config file is not provided, you will be prompted to select "
            "one from the index config directory"
        ),
        callback=prompt_user_to_choose_a_local_config,
    ),
):
    """Create an index in the rank cluster"""
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    client.indices.create(
        index=index, mappings=config["mappings"], settings=config["settings"]
    )
    
    typer.echo(f"Created {index} with config {config_path}")

@app.command()
def update(
    index: str = typer.Option(
        None,
        help=(
            "The name of the index to update. If an index is not provided, you "
            "will be prompted to select one from the rank cluster"
        ),
        callback=prompt_user_to_choose_a_remote_index,
    ),
    config_path: Optional[str] = typer.Option(
        None,
        help=(
            "Path to a json file containing the index settings and mappings. "
            "If a config file is not provided, you will be prompted to select "
            "one from the index config directory"
        ),
        callback=prompt_user_to_choose_a_local_config,
    )
):
    """Update an index in the rank cluster"""
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    client.indices.put_settings(index=index, body=config["settings"])
    client.indices.put_mapping(index=index, body=config["mappings"])
    typer.echo(f"{index} updated")

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
    index: str = typer.Option(
        None,
        help=(
            "The name of the index to delete. If an index is not provided, you "
            "will be prompted to select one from the rank cluster"
        ),
        callback=prompt_user_to_choose_a_remote_index,
    ),
):
    """Delete an index from the rank cluster"""
    if typer.confirm(f"Are you sure you want to delete {index}?", abort=True):
        client.indices.delete(index=index)
        typer.echo(f"{index} deleted")


@app.command()
def get(
    index: str = typer.Option(
        None,
        help=(
            "The index to get the mappings and settings for. If an index is "
            "not provided, you will be prompted to select one from the rank "
            "cluster"
        ),
        callback=prompt_user_to_choose_a_remote_index,
    ),
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
