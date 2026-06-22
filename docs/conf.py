"""Configure documentation for Sphinx."""

# Standard Library
import pathlib
import sys

# Third Party
from dunamai import Pattern, Version
from sphinx_pyproject import SphinxConfig

# Add package source path to the sys.path for autodoc purposes.
sys.path.insert(0, pathlib.Path("../src").resolve().as_posix())

config = SphinxConfig(
    "../pyproject.toml",
    globalns=globals(),
    config_overrides={"version":  Version.from_git(Pattern.DefaultUnprefixed).serialize()}
)

project = config.name
copyright = f'%Y, {config.author}'

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
