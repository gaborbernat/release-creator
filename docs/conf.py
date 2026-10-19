"""Sphinx project settings."""

from importlib.metadata import version as package_version

project = "release-creator"
release = package_version(project)
extensions = ["myst_parser", "sphinx_argparse_cli", "sphinx_copybutton", "sphinxcontrib.mermaid"]
html_theme = "furo"
html_title = project
html_static_path = ["_static"]
html_css_files = ["custom.css"]
nitpicky = True
exclude_patterns = ["_build"]
