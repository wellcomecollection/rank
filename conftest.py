"""Project-level pytest configuration.

Important: this file is *not* included in the built wheel.

To ensure options like `--run-relevance` work both in-repo and when the package is
installed (e.g. inside the published Docker image), the logic lives in a packaged
pytest plugin: `cli.pytest_plugin`.
"""

# Intentionally empty: the plugin is auto-loaded via the `pytest11` entry point.
