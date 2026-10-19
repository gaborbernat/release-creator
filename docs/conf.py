"""Sphinx project settings."""

from importlib.metadata import version as package_version

project = "release-creator"
release = package_version(project)
extensions = ["sphinx_argparse_cli", "sphinx_copybutton"]
html_theme = "furo"
html_title = project
nitpicky = True
exclude_patterns = ["_build"]
