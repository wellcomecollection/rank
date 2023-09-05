import os
import re
from enum import Enum
from pathlib import Path

import requests
import typer

production_api_url = "https://api.wellcomecollection.org/catalogue/v2"
stage_api_url = "https://api-stage.wellcomecollection.org/catalogue/v2"

role_arn = (
    # Don't assume a role when running in CI.
    # Instead, the role should be assumed by the buildkite instance
    None
    if os.environ.get("BUILDKITE") is not None
    else "arn:aws:iam::760097843905:role/platform-developer"
)


class ContentType(str, Enum):
    works = "works"
    images = "images"


class Cluster(str, Enum):
    pipeline_prod = "pipeline-prod"
    pipeline_stage = "pipeline-stage"
    rank = "rank"


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


def get_pipeline_search_template(
    api_url: str, content_type: ContentType
) -> dict:
    search_templates = requests.get(
        f"{api_url}/search-templates.json",
        timeout=10,
    ).json()["templates"]

    docs = next(
        template
        for template in search_templates
        if template["index"].startswith(content_type)
    )

    return {
        "index": docs["index"],
        "index_date": re.search(
            rf"^{content_type}-indexed-(?P<date>\d{{4}}-\d{{2}}-\d{{2}}.?)",
            docs["index"],
        ).group("date"),
        "query": docs["query"],
    }
