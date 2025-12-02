import typer
from time import sleep

from elasticsearch import Elasticsearch

from .aws import get_secrets
from .. import (
    Cluster,
    get_pipeline_search_template,
    production_api_url,
    stage_api_url
)


common_es_client_config = {
    "timeout": 30,
    "retry_on_timeout": True,
    "max_retries": 3,
}


def pipeline_client(
    context: typer.Context, pipeline_date: str
) -> Elasticsearch:
    secrets = get_secrets(
        session=context.meta["session"],
        secret_prefix=f"elasticsearch/pipeline_storage_{pipeline_date}/",
        secret_ids=[
            "es_password",
            "es_username",
            "protocol",
            "public_host",
            "port",
        ],
    )

    client = Elasticsearch(
        f"{secrets['protocol']}://{secrets['public_host']}:{secrets['port']}",
        basic_auth=(secrets["es_username"], secrets["es_password"]),
        **common_es_client_config,
    )
    wait_for_client(client)
    return client


def rank_client(context: typer.Context) -> Elasticsearch:
    secrets = get_secrets(
        session=context.meta["session"],
        secret_prefix="elasticsearch/rank/",
        secret_ids=["ES_RANK_PASSWORD", "ES_RANK_USER", "ES_RANK_CLOUD_ID"],
    )

    client = Elasticsearch(
        cloud_id=secrets["ES_RANK_CLOUD_ID"],
        basic_auth=(secrets["ES_RANK_USER"], secrets["ES_RANK_PASSWORD"]),
        **common_es_client_config,
    )
    wait_for_client(client)
    return client


def reporting_client(context: typer.Context) -> Elasticsearch:
    secrets = get_secrets(
        session=context.meta["session"],
        secret_prefix="reporting/",
        secret_ids=[
            "es_host",
            "read_only/es_password",
            "read_only/es_username",
        ],
    )

    reporting_es_client = Elasticsearch(
        hosts=f"https://{secrets['es_host']}:443",
        basic_auth=(
            secrets["read_only/es_username"],
            secrets["read_only/es_password"],
        ),
        **common_es_client_config,
    )
    wait_for_client(reporting_es_client)
    return reporting_es_client


def wait_for_client(client: Elasticsearch):
    while True:
        try:
            client.ping()
            break
        except Exception:
            sleep(3)


def _get_index_name(pipeline_date: str | None, cluster: Cluster | None, content_type: str):
    if pipeline_date:
        index_date = pipeline_date
    else:
        api_url = production_api_url if cluster == Cluster.pipeline_prod else stage_api_url
        template = get_pipeline_search_template(api_url, content_type)
        index_date = template['index_date']

    return f"{content_type}-indexed-{index_date}"


def _get_client(context: typer.Context, pipeline_date: str | None, cluster: Cluster | None, content_type: str) -> Elasticsearch:
    if pipeline_date:
        return pipeline_client(context=context, pipeline_date=pipeline_date)

    if cluster == Cluster.rank:
        return rank_client(context)

    api_url = production_api_url if cluster == Cluster.pipeline_prod else stage_api_url
    template = get_pipeline_search_template(api_url, content_type)
    client = pipeline_client(context=context, pipeline_date=template["pipeline_date"])

    return client
