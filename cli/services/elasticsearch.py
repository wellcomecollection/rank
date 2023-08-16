from time import sleep

import boto3
from elasticsearch import Elasticsearch

from .aws import get_secrets


def pipeline_client(
    session: boto3.session.Session, *, pipeline_date: str
) -> Elasticsearch:
    secrets = get_secrets(
        session=session,
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
    )
    wait_for_client(client)
    return client


def rank_client(session: boto3.session.Session) -> Elasticsearch:
    secrets = get_secrets(
        session=session,
        secret_prefix="elasticsearch/rank/",
        secret_ids=["ES_RANK_PASSWORD", "ES_RANK_USER", "ES_RANK_CLOUD_ID"],
    )

    client = Elasticsearch(
        cloud_id=secrets["ES_RANK_CLOUD_ID"],
        basic_auth=(secrets["ES_RANK_USER"], secrets["ES_RANK_PASSWORD"]),
    )
    wait_for_client(client)
    return client


def reporting_client(
    session: boto3.session.Session,
) -> Elasticsearch:
    secrets = get_secrets(
        session=session,
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
