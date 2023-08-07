from typing import Optional
import json
import typer
from . import (
    get_valid_indices,
    prompt_user_to_choose_a_remote_index,
    prompt_user_to_choose_a_local_config,
    raise_if_index_already_exists,
    rank_client,
)
from .. import index_config_directory

app = typer.Typer(
    name="index",
    help="Manage indices in the rank cluster",
    no_args_is_help=True,
)


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
    source_index: Optional[str] = typer.Option(
        None,
        help=(
            "The name of an existing index to reindex from. If a source index "
            "is not provided, you will be prompted to select one from the "
            "rank cluster"
        ),
        callback=prompt_user_to_choose_a_remote_index,
    ),
):
    """Create an index in the rank cluster"""
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    rank_client.indices.create(
        index=index, mappings=config["mappings"], settings=config["settings"]
    )

    typer.echo(f"Created {index} with config {config_path}")

    if typer.confirm(
        f"Do you want to reindex {source_index} into {index}?",
        abort=True,
    ):
        task = rank_client.reindex(
            body={
                "source": {"index": source_index, "size": 100},
                "dest": {"index": index},
            },
            wait_for_completion=False,
        )
        typer.echo(f"Reindex task {task['task']} started")
        typer.echo(
            f"Run `rank task status {task['task']}` to monitor its progress"
        )


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
    ),
):
    """Update an index in the rank cluster"""
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    rank_client.indices.put_settings(index=index, body=config["settings"])
    rank_client.indices.put_mapping(index=index, body=config["mappings"])
    typer.echo(f"{index} updated")

    if typer.confirm(
        f"Do you want to update documents in {index} to use the new mapping?"
    ):
        task = rank_client.update_by_query(
            index=index, wait_for_completion=False
        )
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
        rank_client.indices.delete(index=index)
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
    config = dict(rank_client.indices.get(index=index))[index]
    # only keep the analysis section of the settings
    config["settings"] = {
        "index": {"analysis": config["settings"]["index"]["analysis"]}
    }

    config_path = index_config_directory / f"{index}.json"
    with open(config_path, "w") as f:
        f.write(json.dumps(config, indent=2))
    typer.echo(f"Index config written to {config_path}")


@app.command()
def replicate():
    """Replicate an index from a production cluster to the rank cluster"""
    raise NotImplementedError
