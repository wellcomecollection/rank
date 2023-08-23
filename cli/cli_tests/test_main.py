import toml
from typer.testing import CliRunner
from cli import __version__
from cli.main import app


def test_version_is_correct():
    pyproject = toml.load("pyproject.toml")
    assert __version__ == pyproject["tool"]["poetry"]["version"]


def test_version_command():
    result = CliRunner().invoke(app, ["version"])
    assert result.exit_code == 0
    assert __version__ in result.stdout


def test_help_with_flag():
    result = CliRunner().invoke(app, ["--help"])
    assert result.exit_code == 0
    assert all(
        [
            command in result.stdout
            for command in ["test", "index", "search", "task", "query"]
        ]
    )


def test_help_without_flag():
    result = CliRunner().invoke(app)
    assert result.exit_code == 0
    assert all(
        [
            command in result.stdout
            for command in ["test", "index", "search", "task", "query"]
        ]
    )
