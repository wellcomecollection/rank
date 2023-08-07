from enum import Enum
from pathlib import Path

catalogue_api_url = "https://api.wellcomecollection.org/catalogue/v2"

ContentType = Enum("ContentType", ["works", "images"])

# make sure that `ContentType`s play nicely with paths and strings
ContentType.__str__ = lambda self: self.name
ContentType.__fspath__ = lambda self: self.name

data_directory = Path("data/")
index_config_directory = data_directory / "index_config"
query_directory = data_directory / "queries"
term_directory = data_directory / "terms"
