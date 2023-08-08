from typing import Optional

import beaupy
import typer
from elasticsearch import Elasticsearch

from .. import ContentType, index_config_directory, query_directory


def get_valid_indices(context: typer.Context):
    rank_client: Elasticsearch = context.meta["rank_client"]
    return [
        index["index"]
        for index in rank_client.cat.indices(
            format="json", h="index", s="index"
        )
        if not index["index"].startswith(".")
    ]


def get_valid_configs(context: typer.Context):
    """
    Returns a list of the files containing index config (ie mappings/settings)
    in the /data directory
    """
    if not index_config_directory.exists():
        raise FileNotFoundError(
            f"A local index config directory ({index_config_directory}) does "
            "not exist. You can create it and add config files by running "
            "`rank index get`"
        )

    valid_configs = [p for p in index_config_directory.glob("*.json")]

    if len(valid_configs) == 0:
        raise FileNotFoundError(
            f"No config files found in {index_config_directory}"
        )

    return valid_configs


def get_valid_queries(context: typer.Context):
    """
    Returns a list of the files containing queries in the /data directory
    """
    if not query_directory.exists():
        raise FileNotFoundError(
            f"A local query directory ({query_directory}) does not exist. You "
            "can create it and add the current prod queries by running "
            "`rank query get`."
        )

    valid_queries = [p for p in query_directory.glob("*.json")]

    if len(valid_queries) == 0:
        raise FileNotFoundError(f"No config files found in {query_directory}")
    return valid_queries


def get_valid_tasks(context: typer.Context):
    rank_client: Elasticsearch = context.meta["rank_client"]
    actions = [
        "indices:data/write/reindex",
        "indices:data/write/update/byquery",
    ]
    nodes = rank_client.tasks.list(detailed=True, actions=actions)["nodes"]
    return [
        {"task_id": task_id, **task}
        for node_id, node in nodes.items()
        for task_id, task in node["tasks"].items()
    ]


def prompt_user_to_choose_a_remote_index(
    context: typer.Context, index: Optional[str]
) -> str:
    if index is None:
        typer.echo("Select an index")
        valid_indices = get_valid_indices(context)
        index = beaupy.select(valid_indices)
    else:
        rank_client: Elasticsearch = context.meta["rank_client"]
        if not rank_client.indices.exists(index=index):
            raise typer.BadParameter(f"{index} does not exist")
        elif index.startswith(".") or (index == "_all"):
            raise typer.BadParameter(f"{index} is a system index")
    return index


def prompt_user_to_choose_a_local_config(
    context: typer.Context, config_path: Optional[str]
) -> str:
    if config_path is None:
        typer.echo("Select a config file")
        valid_configs = get_valid_configs(context)
        config_path = beaupy.select(
            valid_configs,
            preprocessor=lambda x: x.stem,
        )
    return config_path


def prompt_user_to_choose_a_local_query(
    context: typer.Context, query_path: Optional[str]
) -> str:
    if query_path is None:
        typer.echo("Select a query file")
        valid_queries = get_valid_queries(context)
        query_path = beaupy.select(
            valid_queries,
            preprocessor=lambda x: x.stem,
        )
    return query_path


def raise_if_index_already_exists(context: typer.Context, index: str):
    rank_client: Elasticsearch = context.meta["rank_client"]
    if rank_client.indices.exists(index=index):
        raise typer.BadParameter(f"{index} already exists")
    return index


def prompt_user_to_choose_a_content_type(
    content_type: Optional[ContentType],
) -> ContentType:
    valid_content_types = [content_type.value for content_type in ContentType]
    if content_type is None:
        typer.echo("Select a content type")
        index = beaupy.select(valid_content_types)
    else:
        if content_type not in valid_content_types:
            raise typer.BadParameter(
                f"{content_type} is not a valid content type"
            )
    return index


def prompt_user_to_choose_a_task(
    context: typer.Context, task_id: Optional[str]
) -> str:
    valid_tasks = get_valid_tasks(context)
    if len(valid_tasks) == 0:
        raise typer.BadParameter("No tasks running")
    if task_id is None:
        typer.echo("Select a task")
        task = beaupy.select(
            valid_tasks,
            preprocessor=lambda x: f'{x["task_id"]} | {x["action"]}',
        )
        task_id = task["task_id"]
    else:
        valid_task_ids = [task["task_id"] for task in valid_tasks]
        if task_id not in valid_task_ids:
            raise typer.BadParameter(f"{task_id} does not exist")
    return task_id
