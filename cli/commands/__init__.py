from typing import Optional

import beaupy
import typer
from elasticsearch import Elasticsearch

from .. import (
    ContentType,
    index_config_directory,
    query_directory,
)


def get_valid_indices(client: Elasticsearch):
    return [
        index["index"]
        for index in client.cat.indices(format="json", h="index", s="index")
        if not index["index"].startswith(".")
    ]


def get_valid_configs():
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


def get_local_query_files():
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


def get_valid_tasks(client: Elasticsearch):
    actions = [
        "indices:data/write/reindex",
        "indices:data/write/update/byquery",
    ]
    nodes = client.tasks.list(detailed=True, actions=actions)["nodes"]
    return [
        {"task_id": task_id, **task}
        for node_id, node in nodes.items()
        for task_id, task in node["tasks"].items()
    ]


def prompt_user_to_choose_an_index(
    client: Elasticsearch,
    index: Optional[str],
    content_type: Optional[ContentType] = None,
) -> str:
    if index is None:
        valid_indices = get_valid_indices(client)
        if content_type is not None:
            valid_indices = [
                index
                for index in valid_indices
                if index.startswith(content_type.value)
            ]
        if len(valid_indices) == 0:
            raise ValueError(
                f"No valid indices found in for content type: {content_type}"
            )
        elif len(valid_indices) == 1:
            index = valid_indices[0]
        else:
            typer.echo("Select an index")
            index = beaupy.select(valid_indices)
    else:
        if not client.indices.exists(index=index):
            raise typer.BadParameter(f"{index} does not exist")
        elif index.startswith(".") or (index == "_all"):
            raise typer.BadParameter(f"{index} is a system index")
    typer.echo(f"Using index: {index}")
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


def prompt_user_to_choose_a_local_query(
    query_path: Optional[str] = None,
    content_type: Optional[ContentType] = None,
) -> str:
    if query_path is None:
        query_files = [
            path for path in get_local_query_files()
            if content_type is None or path.stem.startswith(content_type.value)
        ]
        if len(query_files) == 0:
            raise FileNotFoundError(
                f"No valid queries found in {query_directory} "
                f"for content type: {content_type}"
            )
        elif len(query_files) == 1:
            query_path = query_files[0]
        else:
            typer.echo("Select a query file")
            query_path = beaupy.select(
                query_files,
                preprocessor=lambda x: x.stem,
            )
    typer.echo(f"Using query: {query_path}")
    return query_path


def raise_if_index_already_exists(client: Elasticsearch, index: str):
    if client.indices.exists(index=index):
        raise typer.BadParameter(f"{index} already exists")
    return index


def prompt_user_to_choose_a_task(
        client: Elasticsearch, task_id: Optional[str]
) -> str:
    valid_tasks = get_valid_tasks(client)
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
