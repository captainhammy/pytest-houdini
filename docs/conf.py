# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys

from dunamai import Pattern, Version
from sphinx_pyproject import SphinxConfig

sys.path.insert(0, os.path.abspath("../src"))

config = SphinxConfig("../pyproject.toml", globalns=globals())

project = config.name
copyright = f'%Y, {author}'
version = Version.from_git(Pattern.DefaultUnprefixed).serialize()

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx_rtd_theme",
    "sphinx_copybutton",
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    "hou": ("https://www.sidefx.com/docs/houdini/hom/hou", "objects_hou.inv"),
    "pytest": ("https://docs.pytest.org/en/stable", None),
}

autodoc_mock_imports = ["hou"]
autodoc_member_order = "bysource"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
