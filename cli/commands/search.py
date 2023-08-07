import rich
import json
import chevron
from .. import ContentType, term_directory
from . import (
    prompt_user_to_choose_a_content_type,
    session,
    rank_client,
    prompt_user_to_choose_a_remote_index,
    prompt_user_to_choose_a_local_query,
)
import typer
from typing import Optional
from datetime import datetime
from ..services import elasticsearch


app = typer.Typer(
    name="search",
    help="Run searches against candidate indices with candidate queries",
)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    search_terms: Optional[str] = typer.Option(
        None,
        help="The search terms to use",
        prompt="What are you looking for?",
    ),
    index: Optional[str] = typer.Option(
        None,
        help="The index to search in",
        callback=prompt_user_to_choose_a_remote_index,
    ),
    query_path: Optional[str] = typer.Option(
        None,
        help="The query to run",
        callback=prompt_user_to_choose_a_local_query,
    ),
    n: Optional[int] = typer.Option(
        10,
        help="The number of results to return",
    ),
):
    if ctx.invoked_subcommand is None:
        content_type = ContentType(index.split("-")[0])

        with open(query_path, "r", encoding="utf-8") as f:
            query = json.dumps(json.load(f))

        rendered_query = chevron.render(query, {"query": search_terms})
        response = rank_client.search(
            index=index,
            query=json.loads(rendered_query),
            size=n,
            source=[
                "display.referenceNumber",
                "display.title",
                "display.production",
            ],
        )

        total = response["hits"]["total"]["value"]

        # Use rich tables to display the output
        table = rich.table.Table(
            caption=f"Found {total} results",
            caption_justify="left",
            show_header=True,
            show_footer=False,
            box=rich.box.HEAVY_EDGE,
            leading=1,
        )
        table.add_column("i", justify="right", no_wrap=True)
        table.add_column("Score", justify="right", no_wrap=True)
        table.add_column("ID", justify="left", no_wrap=True)
        table.add_column("Title", justify="left", no_wrap=False)
        table.add_column("Dates", justify="left", no_wrap=True)
        table.add_column("Reference number", justify="left", no_wrap=True)

        for i, hit in enumerate(response["hits"]["hits"]):
            url = f"https://wellcomecollection.org/{content_type}/{hit['_id']}"

            score = str(hit["_score"])
            title = hit["_source"]["display"]["title"]

            if len(hit["_source"]["display"]["production"]) > 0:
                dates = ", ".join(
                    [
                        date["label"]
                        for production in hit["_source"]["display"][
                            "production"
                        ]
                        for date in production["dates"]
                    ]
                )
            else:
                dates = None

            try:
                reference_number = hit["_source"]["display"]["referenceNumber"]
            except KeyError:
                reference_number = None

            table.add_row(
                str(i + 1),
                score,
                f"[link={url}]{hit['_id']}[/link]",
                f"[link={url}]{title}[/link]",
                dates,
                reference_number,
            )

        rich.print(table)


@app.command()
def get_terms(
    content_type: Optional[ContentType] = typer.Option(
        None,
        help="The content type to find real search terms for",
        callback=prompt_user_to_choose_a_content_type,
    ),
):
    """Get a list of real search terms for a given content type"""
    reporting_client = elasticsearch.reporting_client(session)
    response = reporting_client.search(
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

    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(json.dumps(unique_terms, indent=2))

    typer.echo(f"Saved {len(unique_terms)} terms to {path}")


@app.command()
def compare():
    """Compare the speed of two queries against the same index"""
    raise NotImplementedError
