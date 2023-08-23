from enum import Enum
from pathlib import Path
import typer

catalogue_api_url = "https://api.wellcomecollection.org/catalogue/v2"


class ContentType(str, Enum):
    WORKS = "works"
    IMAGES = "images"


data_directory = Path(typer.get_app_dir("weco/rank"))
index_config_directory = data_directory / "index_config"
query_directory = data_directory / "queries"
term_directory = data_directory / "terms"
