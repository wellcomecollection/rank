import time
from typing import Optional
import typer
import beaupy
from . import rank_client
from rich.progress import Progress


app = typer.Typer(
    name="task",
    help="Manage tasks running on the rank cluster",
    no_args_is_help=True,
)


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


@app.command()
def list():
    """List all tasks"""
    tasks = get_valid_tasks()
    for task in tasks:
        typer.echo(f'{task["task_id"]} | {task["action"]}')


@app.command()
def status(
    task_id: Optional[str] = typer.Argument(
        None,
        help="Task ID. If not provided, you will be prompted to select an ID from a list of running tasks",
        callback=prompt_user_to_choose_a_task,
    )
):
    """Get the status of a task"""
    task = rank_client.tasks.get(task_id=task_id)
    # set up a progress bar
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
    task: Optional[str] = typer.Argument(
        None,
        help="Task ID. If not provided, you will be prompted to select an ID from a list of running tasks",
        callback=prompt_user_to_choose_a_task,
    )
):
    """Cancel a task"""
    if typer.confirm(f"Are you sure you want to cancel {task}?", abort=True):
        rank_client.tasks.cancel(task_id=task)
