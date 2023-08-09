import json
from typing import Optional

import typer
from elasticsearch import Elasticsearch

from .. import index_config_directory
from ..services import aws, elasticsearch
from . import (
    get_valid_indices,
    prompt_user_to_choose_a_local_config,
    prompt_user_to_choose_a_remote_index,
    raise_if_index_already_exists,
)

app = typer.Typer(
    name="index",
    help="Manage indices in the rank cluster",
    no_args_is_help=True,
    add_completion=False,
)


@app.callback()
def callback(context: typer.Context):
    context.meta["session"] = aws.get_session(context.meta["role_arn"])
    context.meta["rank_client"] = elasticsearch.rank_client(
        context.meta["session"]
    )


@app.command(name="list")
def list_indices(context: typer.Context):
    """List the indices in the rank cluster"""
    valid_indices = get_valid_indices(context)
    typer.echo("\n".join(valid_indices))


@app.command()
def create(
    context: typer.Context,
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
    ),
    source_index: Optional[str] = typer.Option(
        None,
        help=(
            "The name of an existing index to reindex from. If a source index "
            "is not provided, you will be prompted to select one from the "
            "rank cluster"
        ),
    ),
):
    """Create an index in the rank cluster"""
    source_index = prompt_user_to_choose_a_remote_index(context, source_index)
    config_path = prompt_user_to_choose_a_local_config(context, config_path)

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
        task_id = task["task"]
        typer.echo(f"Reindex task {task_id} started")
        typer.echo(
            f"Run `rank task status --task-id={task_id}` to monitor its progress"
        )


@app.command()
def update(
    context: typer.Context,
    index: str = typer.Option(
        None,
        help=(
            "The name of the index to update. If an index is not provided, you "
            "will be prompted to select one from the rank cluster"
        ),
    ),
    config_path: Optional[str] = typer.Option(
        None,
        help=(
            "Path to a json file containing the index settings and mappings. "
            "If a config file is not provided, you will be prompted to select "
            "one from the index config directory"
        ),
    ),
):
    """Update an index in the rank cluster"""
    index = prompt_user_to_choose_a_remote_index(context, index)
    config_path = prompt_user_to_choose_a_local_config(context, config_path)

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    rank_client: Elasticsearch = context.meta["rank_client"]
    rank_client.indices.put_settings(index=index, body=config["settings"])
    rank_client.indices.put_mapping(index=index, body=config["mappings"])
    typer.echo(f"{index} updated")

    if typer.confirm(
        f"Do you want to update documents in {index} to use the new mapping?"
    ):
        task = rank_client.update_by_query(
            index=index, wait_for_completion=False
        )
        task_id = task["task"]
        typer.echo(f"Update task {task_id} started")
        typer.echo(
            f"Run `rank task status --task-id={task_id}` to monitor its progress"
        )


@app.command(help="Delete an index")
def delete(
    context: typer.Context,
    index: str = typer.Option(
        None,
        help=(
            "The name of the index to delete. If an index is not provided, you "
            "will be prompted to select one from the rank cluster"
        ),
    ),
):
    """Delete an index from the rank cluster"""
    index = prompt_user_to_choose_a_remote_index(context, index)
    if typer.confirm(f"Are you sure you want to delete {index}?", abort=True):
        rank_client.indices.delete(index=index)
        typer.echo(f"{index} deleted")


@app.command()
def get(
    context: typer.Context,
    index: str = typer.Option(
        None,
        help=(
            "The index to get the mappings and settings for. If an index is "
            "not provided, you will be prompted to select one from the rank "
            "cluster"
        ),
    ),
):
    """Get the mappings and settings for an index in the rank cluster"""
    index = prompt_user_to_choose_a_remote_index(context, index)
    rank_client: Elasticsearch = context.meta["rank_client"]
    config = dict(rank_client.indices.get(index=index))[index]
    # only keep the analysis section of the settings
    config["settings"] = {
        "index": {"analysis": config["settings"]["index"]["analysis"]}
    }

    config_path = index_config_directory / f"{index}.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, "w") as f:
        f.write(json.dumps(config, indent=2))
    typer.echo(f"Index config written to {config_path}")


@app.command()
def replicate():
    """Replicate an index from a production cluster to the rank cluster"""
    raise NotImplementedError
