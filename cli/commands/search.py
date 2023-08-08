import json
from datetime import datetime
from typing import Optional

import chevron
import rich
import typer

from .. import ContentType, term_directory
from ..services import aws, elasticsearch
from . import (
    prompt_user_to_choose_a_content_type,
    prompt_user_to_choose_a_local_query,
    prompt_user_to_choose_a_remote_index,
)

app = typer.Typer(
    name="search",
    help=(
        """
        Run a search against a candidate index, using a candidate query\n

        Useful when developing a new query or index and looking for qualitative
        feedback, rather than the quantitative feedback you get from running
        the full rank test suite.\n

        The command will output a table of results with the following columns:\n
        Score, ID, Title, Dates, Reference number
        """
    ),
)


def build_results_table(
    response: dict, content_type: ContentType
) -> rich.table.Table:
    builder = {
        ContentType.WORKS: build_works_results_table,
        ContentType.IMAGES: build_images_results_table,
    }
    return builder[content_type](response)


def build_works_results_table(response: dict) -> rich.table.Table:
    total = response["hits"]["total"]["value"]

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
        url = f"https://wellcomecollection.org/works/{hit['_id']}"

        score = str(hit["_score"])
        title = hit["_source"]["display"]["title"]

        if len(hit["_source"]["display"]["production"]) > 0:
            dates = ", ".join(
                [
                    date["label"]
                    for production in hit["_source"]["display"]["production"]
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

    return table


def build_images_results_table(response: dict) -> rich.table.Table:
    total = response["hits"]["total"]["value"]

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

    for i, hit in enumerate(response["hits"]["hits"]):
        score = str(hit["_score"])
        title = hit["_source"]["display"]["source"]["title"]
        url = (
            f"https://wellcomecollection.org/works/{hit['_source']['display']['source']['id']}"
            f"/images?id={hit['_id']}"
        )

        table.add_row(
            str(i + 1),
            score,
            f"[link={url}]{hit['_id']}[/link]",
            f"[link={url}]{title}[/link]",
        )
    return table


@app.callback(invoke_without_command=True)
def main(
    context: typer.Context,
    search_terms: Optional[str] = typer.Option(
        None,
        help="The search terms to use",
    ),
    index: Optional[str] = typer.Option(
        None,
        help="The index to search in",
    ),
    query_path: Optional[str] = typer.Option(
        None,
        help="The query to run",
    ),
    n: Optional[int] = typer.Option(
        10,
        help="The number of results to return",
        min=1,
        max=100,
    ),
):
    context.meta["session"] = aws.get_session(context.meta["role_arn"])
    context.meta["rank_client"] = elasticsearch.rank_client(
        context.meta["session"]
    )

    if context.invoked_subcommand is None:
        # We shouldn't use callbacks here, because the main() command itself is
        # a callback. If a user tries to run eg `rank search get-terms` with
        # callbacks specified in the parameters of main(), those callbacks
        # will be run before the subcommand is invoked. This means that the user
        # will be prompted to choose an index and query for subcommands that
        # don't need them. Instead, we'll just prompt the user here if they
        # haven't provided the necessary arguments.
        if search_terms is None:
            search_terms = typer.prompt("What are you looking for?")
        index = prompt_user_to_choose_a_remote_index(
            context=context, index=index
        )
        query_path = prompt_user_to_choose_a_local_query(
            context=context, query_path=query_path
        )

        content_type = ContentType(index.split("-")[0])

        with open(query_path, "r", encoding="utf-8") as f:
            query = json.dumps(json.load(f))

        rendered_query = chevron.render(query, {"query": search_terms})

        response = context.meta["rank_client"].search(
            index=index,
            query=json.loads(rendered_query),
            size=n,
            source=["display"],
        )

        table = build_results_table(response, content_type)
        rich.print(table)


@app.command()
def get_terms(
    context: typer.Context,
    content_type: Optional[ContentType] = typer.Option(
        None,
        help="The content type to find real search terms for",
        callback=prompt_user_to_choose_a_content_type,
    ),
):
    """Get a list of real search terms for a given content type"""
    reporting_client = elasticsearch.reporting_client(context.meta["session"])

    # Page names and content types are currently the same but we don't want to
    # rely on that
    page_name = {
        "works": "works",
        "images": "images",
    }[content_type.value]

    response = reporting_client.search(
        query={
            "bool": {
                "filter": [
                    {"exists": {"field": "page.query.query"}},
                    {"term": {"page.name": page_name}},
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
def compare(context: typer.Context):
    """Compare the speed of two queries against the same index"""
    raise NotImplementedError
