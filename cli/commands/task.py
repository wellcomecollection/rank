import time
from typing import Optional

import typer
from elasticsearch import Elasticsearch
from rich.progress import Progress

from ..services import aws, elasticsearch
from . import get_valid_tasks, prompt_user_to_choose_a_task

app = typer.Typer(
    name="task",
    help="Manage tasks running on the rank cluster",
    no_args_is_help=True,
)


@app.callback()
def callback(context: typer.Context):
    context.meta["session"] = aws.get_session(context.meta["role_arn"])
    context.meta["rank_client"] = elasticsearch.rank_client(
        context.meta["session"]
    )


@app.command(name="list")
def list_tasks(
    context: typer.Context,
):
    """List all tasks"""
    tasks = get_valid_tasks(context)
    for task in tasks:
        typer.echo(f'{task["task_id"]} | {task["action"]}')


@app.command()
def status(
    context: typer.Context,
    task_id: Optional[str] = typer.Option(
        None,
        help=(
            "Task ID. If not provided, you will be prompted to select an ID "
            "from a list of running tasks"
        ),
        callback=prompt_user_to_choose_a_task,
    ),
):
    """Get the status of a task"""
    rank_client: Elasticsearch = context.meta["rank_client"]
    task = rank_client.tasks.get(task_id=task_id)
    with Progress() as progress:
        task_progress = progress.add_task(
            task_id,
            total=task["task"]["status"]["total"],
            start=True,
        )
        while not progress.finished:
            created_or_updated = (
                task["task"]["status"]["created"]
                + task["task"]["status"]["updated"]
            )
            progress.update(task_progress, completed=created_or_updated)
            time.sleep(1)
            task = rank_client.tasks.get(task_id=task_id)
            if task["completed"]:
                progress.stop()
                break


@app.command()
def cancel(
    context: typer.Context,
    task: Optional[str] = typer.Option(
        None,
        help=(
            "Task ID. If not provided, you will be prompted to select an ID "
            "from a list of running tasks"
        ),
        callback=prompt_user_to_choose_a_task,
    ),
):
    """Cancel a task"""
    if typer.confirm(f"Are you sure you want to cancel {task}?", abort=True):
        rank_client: Elasticsearch = context.meta["rank_client"]
        rank_client.tasks.cancel(task_id=task)
