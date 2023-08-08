import os
from enum import Enum
from pathlib import Path

catalogue_api_url = "https://api.wellcomecollection.org/catalogue/v2"

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


data_directory = Path("data/")
index_config_directory = data_directory / "index_config"
query_directory = data_directory / "queries"
term_directory = data_directory / "terms"
