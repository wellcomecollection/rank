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
    context.meta["client"] = elasticsearch.rank_client(context)


@app.command(name="list")
def list_tasks(context: typer.Context):
    """List all tasks"""
    tasks = get_valid_tasks(client=context.meta["client"])
    for task in tasks:
        typer.echo(f"{task['task_id']} | {task['action']}")


@app.command()
def status(
    context: typer.Context,
    task_id: Optional[str] = typer.Option(
        default=None,
        help=(
            "Task ID. If not provided, you will be prompted to select an ID "
            "from a list of running tasks"
        ),
    ),
):
    """Get the status of a task"""
    client: Elasticsearch = context.meta["client"]
    task_id = prompt_user_to_choose_a_task(client=client, task_id=task_id)
    task = client.tasks.get(task_id=task_id)
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
            task = client.tasks.get(task_id=task_id)
            if task["completed"]:
                progress.stop()
                break


@app.command()
def cancel(
    context: typer.Context,
    task_id: Optional[str] = typer.Option(
        default=None,
        help=(
            "Task ID. If not provided, you will be prompted to select an ID "
            "from a list of running tasks"
        ),
    ),
):
    """Cancel a task"""
    task_id = prompt_user_to_choose_a_task(
        client=context.meta["client"], task_id=task_id
    )
    if typer.confirm(f"Are you sure you want to cancel {task_id}?", abort=True):
        client: Elasticsearch = context.meta["client"]
        client.tasks.cancel(task_id=task_id)
