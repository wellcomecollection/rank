from time import sleep

from elasticsearch import Elasticsearch

from .config import pipeline_date
from .secrets import get_secret


def get_pipeline_elastic_client() -> Elasticsearch:
    secret_prefix = f"elasticsearch/pipeline_storage_{pipeline_date}/"
    es_password = get_secret(secret_prefix + "es_password")
    es_username = get_secret(secret_prefix + "es_username")
    protocol = get_secret(secret_prefix + "protocol")
    public_host = get_secret(secret_prefix + "public_host")
    port = get_secret(secret_prefix + "port")

    client = Elasticsearch(
        f"{protocol}://{public_host}:{port}",
        basic_auth=(es_username, es_password),
    )
    wait_for_client(client)
    return client


def get_rank_elastic_client() -> Elasticsearch:
    secret_prefix = "elasticsearch/rank/"
    es_password = get_secret(secret_prefix + "ES_RANK_PASSWORD")
    es_username = get_secret(secret_prefix + "ES_RANK_USER")
    cloud_id = get_secret(secret_prefix + "ES_RANK_CLOUD_ID")
    client = Elasticsearch(
        cloud_id=cloud_id,
        basic_auth=(es_username, es_password),
    )
    wait_for_client(client)
    return client


def get_reporting_es_client():
    host = get_secret("reporting/es_host")
    es_password = get_secret("reporting/read_only/es_password")
    es_username = get_secret("reporting/read_only/es_username")
    reporting_es_client = Elasticsearch(
        hosts=f"https://{host}:443",
        basic_auth=(es_username, es_password),
        timeout=30,
        retry_on_timeout=True,
        max_retries=10,
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
