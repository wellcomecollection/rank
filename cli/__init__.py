from enum import Enum
from pathlib import Path

root_test_directory = Path("cli/relevance_tests/")

# content types are all the relevant subdirectories in the root test directory
ContentType = Enum(
    "ContentType",
    {
        directory.name: directory.name
        for directory in root_test_directory.iterdir()
        if directory.is_dir()
        and not directory.name.startswith("__")
        and not directory.name.startswith(".")
    },
)

# make sure the contenttype plays nicely with paths and strings
ContentType.__str__ = lambda self: self.name
ContentType.__fspath__ = lambda self: self.name
