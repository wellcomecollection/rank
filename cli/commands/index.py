import beaupy
import json
from typing import Optional

import typer
from elasticsearch import Elasticsearch

from .. import index_config_directory
from ..services import aws, elasticsearch
from ..plugin import get_pipeline_search_templates
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
    valid_indices = get_valid_indices(client=context.meta["rank_client"])
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

    rank_client: Elasticsearch = context.meta["rank_client"]
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
        rank_client: Elasticsearch = context.meta["rank_client"]
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
def replicate(
    context: typer.Context,
    source_index: str = typer.Option(
        None,
        help=(
            "The name of the index to replicate. If an index is not provided, "
            "you will be prompted to select one from the production cluster"
        ),
    ),
    dest_index: str = typer.Option(
        None,
        help=(
            "The name of the index to create in the rank cluster. If an index "
            "is not provided, you will be prompted to select one from the rank "
            "cluster. The default is to use the same name as the source index"
        ),
    ),
):
    """Reindex an index from a production cluster to the rank cluster"""
    pipeline_search_templates = get_pipeline_search_templates(
        catalogue_api_url=context.meta["catalogue_api_url"]
    )
    pipeline_date = pipeline_search_templates["works"]["index_date"]
    pipeline_client = elasticsearch.pipeline_client(
        session=context.meta["session"],
        pipeline_date=pipeline_date,
    )

    if source_index is None:
        valid_indices = get_valid_indices(client=pipeline_client)
        source_index = beaupy.select(valid_indices)
    if not pipeline_client.indices.exists(index=source_index):
        raise typer.BadParameter(f"{source_index} does not exist")
    elif source_index.startswith(".") or (source_index == "_all"):
        raise typer.BadParameter(f"{source_index} is a system index")

    if dest_index is None:
        dest_index = typer.prompt(
            "What do you want to call the index in the rank cluster?",
            default=source_index,
        )
    raise_if_index_already_exists(context=context, index=dest_index)

    if typer.confirm(
        text=(
            "Warning! Reindexing from the production cluster will put some "
            "extra pressure on it, and could affect production services like "
            "the API. The reindex settings have been configured to minimise "
            "this, but if you're worried, you might want to add capacity to "
            "the production cluster before proceeding.\n\n"
            "Are you sure you want to proceed?"
        ),
        abort=True,
    ):
        secrets = aws.get_secrets(
            session=context.meta["session"],
            secret_prefix=f"elasticsearch/pipeline_storage_{pipeline_date}/",
            secret_ids=[
                "es_password",
                "es_username",
                "protocol",
                "public_host",
                "port",
            ],
        )
        pipeline_host = f"{secrets['protocol']}://{secrets['public_host']}:{secrets['port']}"
        pipeline_username = secrets["es_username"]
        pipeline_password = secrets["es_password"]
        rank_client: Elasticsearch = context.meta["rank_client"]
        task = rank_client.reindex(
            body={
                "source": {
                    "remote": {
                        "host": pipeline_host,
                        "username": pipeline_username,
                        "password": pipeline_password,
                    },
                    "index": source_index,
                },
                "dest": {"index": dest_index},
            },
            wait_for_completion=False,
            # minimise the impact on the production cluster by only indexing
            # 500 documents at a time, and only issuing 5 requests per second
            size=500,
            requests_per_second=5,
        )

        task_id = task["task"]
        typer.echo(f"Reindex task {task_id} started")
        typer.echo(
            f"Run `rank task status --task-id={task_id}` to monitor its progress"
        )
