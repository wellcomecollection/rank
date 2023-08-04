import json

from .. import ContentType, term_directory
from . import prompt_user_to_choose_a_content_type
import typer
from typing import Optional
from datetime import datetime
from ..services.elasticsearch import (
    get_rank_elastic_client,
    get_reporting_elastic_client,
    get_pipeline_elastic_client,
)
from ..services.aws import get_session

session = get_session(
    role_arn="arn:aws:iam::760097843905:role/platform-developer"
)

app = typer.Typer(
    name="search",
    help="Run searches against production and candidate indices",
)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
):
    if ctx.invoked_subcommand is None:
        raise NotImplementedError


@app.command()
def get_terms(
    content_type: Optional[ContentType] = typer.Option(
        None,
        help="The content type to find real search terms for",
        callback=prompt_user_to_choose_a_content_type,
    ),
):
    client = get_reporting_elastic_client(session)
    response = client.search(
        query={
            "bool": {
                "filter": [
                    {"exists": {"field": "page.query.query"}},
                    {"term": {"page.name": content_type.value}},
                ],
                "must_not": [
                    {"match": {"properties.looksLikeSpam": "true"}},
                ],
            }
        },
        size=5000,
        _source=["page.query.query"],
        sort=[
            {"@timestamp": {"order": "desc"}},
        ],
    )

    terms = [
        hit["_source"]["page"]["query"]["query"]
        for hit in response["hits"]["hits"]
    ]
    unique_terms = list(set(terms))

    iso_date_without_time = datetime.now().date().isoformat()
    filename = f"{content_type.value}_{iso_date_without_time}.json"
    path = term_directory / filename
    with open(path, "w", encoding="utf-8") as f:
        f.write(json.dumps(unique_terms, indent=2))

    typer.echo(f"Saved {len(unique_terms)} terms to {path}")


@app.command()
def compare():
    raise NotImplementedError
