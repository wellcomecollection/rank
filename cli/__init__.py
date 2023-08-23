import os
import re
from enum import Enum
from pathlib import Path

import requests

__version__ = "0.1.0"

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


class Environment(str, Enum):
    PRODUCTION = "production"
    STAGING = "staging"
    DEVELOPMENT = "development"


data_directory = Path("data/")
index_config_directory = data_directory / "index_config"
query_directory = data_directory / "queries"
term_directory = data_directory / "terms"


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
