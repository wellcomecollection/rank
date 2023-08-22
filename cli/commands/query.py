import json

import beaupy
import requests
import typer
from typing import Optional
from .. import query_directory, Environment
from . import get_valid_queries, prompt_user_to_choose_an_environment

app = typer.Typer(
    name="query",
    help="Manage local queries",
    no_args_is_help=True,
)


@app.command(name="list")
def list_queries(
    context: typer.Context,
):
    """List the queries in the query directory"""
    queries = get_valid_queries(context)
    for query in queries:
        typer.echo(query.name)


@app.command()
def get(
    context: typer.Context,
    environment: Optional[Environment] = typer.Option(
        default=Environment.PRODUCTION,
        help="The environment to get queries from",
        show_choices=True,
        case_sensitive=False,
    ),
):
    """
    Get the prod queries from the API

    Useful when you're working on a new relevance requirement, but don't
    want to start completely from scratch

    N.B. This command will overwrite any existing queries in the query
    directory `data/queries`
    """
    environment = prompt_user_to_choose_an_environment(environment)
    if environment == Environment.DEVELOPMENT:
        raise ValueError(
            "You can only get queries from the production or staging "
            "environments"
        )

    search_templates = requests.get(
        f"{context.meta['api_url']}/search-templates.json"
    ).json()["templates"]

    selected = beaupy.select_multiple(
        search_templates, preprocessor=lambda template: template["index"]
    )

    query_directory.mkdir(exist_ok=True)
    for template in selected:
        query = json.loads(template["query"])
        content_type = template["index"].split("-")[0]
        file_name = f"{content_type}-candidate.json"
        with open(query_directory / file_name, "w", encoding="utf-8") as f:
            json.dump(query, f, indent=2)
        typer.echo(f"Saved {template['index']} to {query_directory/file_name}")
