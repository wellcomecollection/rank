import json

import beaupy
import requests
import typer
from typing import Optional
from .. import query_directory, production_api_url
from . import get_local_query_files

app = typer.Typer(
    name="query",
    help="Manage local queries",
    no_args_is_help=True,
)


@app.command(name="list")
def list_queries():
    """List the queries in the query directory"""
    queries = get_local_query_files()
    for query in queries:
        typer.echo(query.name)


@app.command()
def get(
    context: typer.Context,
    api_url: Optional[str] = typer.Option(
        default=production_api_url,
        help="The target API to get queries from",
        show_choices=True,
        case_sensitive=False,
    ),
    all: bool = typer.Option(
        default=False,
        help="Get all queries from the target",
    ),
):
    """
    Get the queries from the API

    Useful when you're working on a new relevance requirement, but don't
    want to start completely from scratch

    N.B. This command will overwrite any existing queries in the query
    directory `data/queries`
    """
    search_templates = requests.get(f"{api_url}/search-templates.json").json()[
        "templates"
    ]

    if all:
        selected = search_templates
    else:
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
