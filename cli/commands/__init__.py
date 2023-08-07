from .. import ContentType
import typer
import beaupy
from typing import Optional
from .. import index_config_directory, query_directory
from ..services import aws, elasticsearch

session = aws.get_session(
    role_arn="arn:aws:iam::760097843905:role/platform-developer"
)
rank_client = elasticsearch.rank_client(session)


def get_valid_indices():
    return [
        index["index"]
        for index in rank_client.cat.indices(
            format="json", h="index", s="index"
        )
        if not index["index"].startswith(".")
    ]


def get_valid_configs():
    return [p for p in index_config_directory.glob("*.json")]


def get_valid_queries():
    return [p for p in query_directory.glob("*.json")]


def get_valid_tasks():
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


def prompt_user_to_choose_a_remote_index(index: Optional[str]) -> str:
    if index is None:
        typer.echo("Select an index")
        valid_indices = get_valid_indices()
        index = beaupy.select(valid_indices)
    else:
        if not rank_client.indices.exists(index=index):
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


def prompt_user_to_choose_a_local_query(query_path: Optional[str]) -> str:
    if query_path is None:
        typer.echo("Select a query file")
        valid_queries = get_valid_queries()
        query_path = beaupy.select(
            valid_queries,
            preprocessor=lambda x: x.stem,
        )
    return query_path


def raise_if_index_already_exists(index: str):
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


def prompt_user_to_choose_a_task(task_id: Optional[str]) -> str:
    valid_tasks = get_valid_tasks()
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
