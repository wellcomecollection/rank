import os
import re
from enum import Enum
from pathlib import Path

import requests
import typer

production_api_url = "https://api.wellcomecollection.org/catalogue/v2"
staging_api_url = "https://api-stage.wellcomecollection.org/catalogue/v2"


role_arn = (
    # Don't assume a role when running in CI.
    # Instead, the role should be assumed by the buildkite instance
    None
    if os.environ.get("BUILDKITE") is not None
    else "arn:aws:iam::760097843905:role/platform-developer"
)


class ContentType(str, Enum):
    WORKS = "works"
    IMAGES = "images"


class Target(str, Enum):
    """
    The target context/environment to run tests against.

    Using production will use the production API to find the and the production
    Elasticsearch cluster, the appropriate index, and the query template to
    search with.

    Staging will do the same using the staging API.

    Development will use the rank cluster, allowing users to specify the remote
    index (in the rank cluster) and a locally defined query template.
    """

    PRODUCTION = "production"
    STAGING = "staging"
    DEVELOPMENT = "development"


data_directory = Path(typer.get_app_dir("weco/rank"))
index_config_directory = data_directory / "index_config"
query_directory = data_directory / "queries"
term_directory = data_directory / "terms"

# make sure that the directories exist
for directory in [
    data_directory,
    index_config_directory,
    query_directory,
    term_directory,
]:
    directory.mkdir(parents=True, exist_ok=True)


def get_pipeline_search_templates(api_url: str) -> dict:
    search_templates = requests.get(
        f"{api_url}/search-templates.json",
        timeout=10,
    ).json()["templates"]

    works = next(
        template
        for template in search_templates
        if template["index"].startswith("works")
    )
    images = next(
        template
        for template in search_templates
        if template["index"].startswith("images")
    )

    return {
        "works": {
            "index": works["index"],
            "index_date": re.search(
                r"^works-indexed-(?P<date>\d{4}-\d{2}-\d{2}.?)",
                works["index"],
            ).group("date"),
            "query": works["query"],
        },
        "images": {
            "index": images["index"],
            "index_date": re.search(
                r"^images-indexed-(?P<date>\d{4}-\d{2}-\d{2}.?)",
                images["index"],
            ).group("date"),
            "query": images["query"],
        },
    }
