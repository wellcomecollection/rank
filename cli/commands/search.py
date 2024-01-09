import json
import os
from datetime import datetime
from typing import Optional
from urllib.parse import urlparse

import chevron
import rich
import typer

from .. import (
    ContentType,
    Cluster,
    term_directory,
    get_pipeline_search_template,
    production_api_url,
    stage_api_url,
)
from ..services import aws, elasticsearch
from . import (
    prompt_user_to_choose_a_local_query,
    prompt_user_to_choose_an_index,
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

        If you want to run the search against the production/staging index,
        you should specify eg --target=production. In this case, index and
        query selection will be handled automatically.
        """
    ),
)


def build_results_table(
    response: dict, content_type: ContentType
) -> rich.table.Table:
    builder = {
        ContentType.works: build_works_results_table,
        ContentType.images: build_images_results_table,
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
    table.add_column("Contributors", justify="left", no_wrap=False)
    table.add_column("Dates", justify="left", no_wrap=True)
    table.add_column("Reference number", justify="left", no_wrap=True)

    for i, hit in enumerate(response["hits"]["hits"]):
        url = f"https://wellcomecollection.org/works/{hit['_id']}"

        score = str(hit["_score"])
        title = hit["_source"]["display"]["title"]
        contributors = ", ".join(
            [
                contributor["agent"]["label"]
                for contributor in hit["_source"]["display"]["contributors"]
            ]
        )
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
            contributors,
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
        default=None,
        help="The search terms to use",
    ),
    content_type: ContentType = typer.Option(
        help="The content type to search in",
        show_choices=True,
        case_sensitive=False,
        prompt=True,
        default=None,
    ),
    query: Optional[str] = typer.Option(
        help="The query to test: a local file path or a URL of catalogue API search templates",
        default=None,
    ),
    index: Optional[str] = typer.Option(
        help="The index to run tests against",
        case_sensitive=False,
        default=None,
    ),
    cluster: Cluster = typer.Option(
        help="The ElasticSearch cluster on which to run test queries",
        show_choices=True,
        case_sensitive=False,
        prompt=True,
        default=None,
    ),
    pipeline_date: Optional[str] = typer.Option(
        help="An override for the pipeline date when a pipeline cluster is selected",
        default=None,
    ),
    n: Optional[int] = typer.Option(
        default=10,
        help="The number of results to return",
        min=1,
        max=100,
    ),
    stable_sort_key: Optional[str] = typer.Option(
        default="query.id",
        help="A document property that can be used as a stable sort key",
    ),
):
    if context.invoked_subcommand is None:
        context.meta["session"] = aws.get_session(context.meta["role_arn"])
        context.meta["content_type"] = content_type

        if str(urlparse(query).scheme).startswith("http"):
            search_template = get_pipeline_search_template(
                api_url=query, content_type=context.meta["content_type"]
            )
            index = index if index else search_template["index"]
            query = search_template["query"]
        elif query and os.path.isfile(query):
            with open(query) as file_contents:
                query = file_contents.read()
        else:
            query_path = prompt_user_to_choose_a_local_query(
                query, content_type=context.meta["content_type"]
            )
            with open(query_path, "r", encoding="utf-8") as f:
                query = f.read()

        if pipeline_date:
            index = (
                index if index else f"{content_type}-indexed-{pipeline_date}"
            )
            context.meta["client"] = elasticsearch.pipeline_client(
                context=context, pipeline_date=pipeline_date
            )
        elif cluster == Cluster.pipeline_prod:
            prod_template = get_pipeline_search_template(
                production_api_url, context.meta["content_type"]
            )
            index = (
                index
                if index
                else f"{content_type}-indexed-{prod_template['index_date']}"
            )
            context.meta["client"] = elasticsearch.pipeline_client(
                context=context, pipeline_date=prod_template["index_date"]
            )
        elif cluster == Cluster.pipeline_stage:
            stage_template = get_pipeline_search_template(
                stage_api_url, context.meta["content_type"]
            )
            index = (
                index
                if index
                else f"{content_type}-indexed-{stage_template['index_date']}"
            )
            context.meta["client"] = elasticsearch.pipeline_client(
                context=context, pipeline_date=stage_template["index_date"]
            )
        elif cluster == Cluster.rank:
            context.meta["client"] = elasticsearch.rank_client(context)

        context.meta["index"] = prompt_user_to_choose_an_index(
            client=context.meta["client"],
            index=index,
            content_type=context.meta["content_type"],
        )

        if search_terms is None:
            search_terms = typer.prompt("What are you looking for?")

        rendered_query = chevron.render(query, {"query": search_terms})

        response = context.meta["client"].search(
            index=context.meta["index"],
            query=json.loads(rendered_query),
            sort=[{"_score": "desc"}, {stable_sort_key: "asc"}],
            size=n,
            source=["display"],
        )

        table = build_results_table(response, context.meta["content_type"])
        rich.print(table)


@app.command()
def get_terms(
    context: typer.Context,
    content_type: ContentType = typer.Option(
        default=None,
        show_choices=True,
        prompt=True,
        help="The content type to find real search terms for",
    ),
):
    """Get a list of real search terms for a given content type"""
    context.meta["session"] = aws.get_session(context.meta["role_arn"])
    reporting_client = elasticsearch.reporting_client(context=context)

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
def compare():
    """Compare the speed of two queries against the same index"""
    raise NotImplementedError
