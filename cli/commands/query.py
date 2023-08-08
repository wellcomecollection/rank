import json
import beaupy
import requests
import typer
from .. import query_directory, catalogue_api_url
from . import get_valid_queries

app = typer.Typer(
    name="query",
    help="Manage local queries",
    no_args_is_help=True,
)


@app.command()
def list():
    """List the queries in the query directory"""
    queries = get_valid_queries()
    for query in queries:
        typer.echo(query.name)


@app.command()
def get():
    """
    Get the prod queries from the API

    Useful when you're working on a new relevance requirement, but don't
    want to start completely from scratch

    N.B. This command will overwrite any existing queries in the query
    directory `data/queries`
    """
    search_templates = requests.get(
        f"{catalogue_api_url}/search-templates.json"
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
