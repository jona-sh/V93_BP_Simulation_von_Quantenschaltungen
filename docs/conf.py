"""Sphinx configuration for q_simulator."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "q_simulator"
copyright = "2026, Felix Gloistein, Jonas Höpker"
author = "Felix Gloistein, Jonas Höpker"
release = "0.0.1"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "myst_nb",
]
myst_enable_extensions = [
    "dollarmath",
]

autosummary_generate = True
napoleon_google_docstring = True
napoleon_numpy_docstring = False
nb_execution_mode = "off"

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_favicon = "_static/favicon.ico"
