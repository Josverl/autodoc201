# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "API documentation test"
copyright = "2024, Jos Verlinde"
author = "Jos Verlinde"
release = "1"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "autoapi.extension",
    "sphinx.ext.intersphinx",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# The suffix of source filenames.
source_suffix = ".rst"
# The master toctree document.
master_doc = "index"
default_role = "any"
pygments_style = "sphinx"
# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"
html_static_path = ["_static"]
# -----------------------------------------------------------------------------
# Configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    "python": ("https://docs.python.org/3.5", None),
    "micropython": ("https://docs.micropython.org/en/latest", None),
}

# -----------------------------------------------------------------------------
from pathlib import Path
from typing import Any, List

#  https://sphinx-autoapi.readthedocs.io/en/latest/reference/config.html#confval-autoapi_options
autoapi_options = [
    "members",
    "undoc-members",
    # "inherited-members", # Display children of an object that have been inherited from a base class.
    "private-members",  # _foo
    "special-members",  # __foo
    "show-inheritance",  # Display a list of base classes below the class signature.
    "show-module-summary",  # include autosummary directives in generated module documentation
    # "imported-members", $# For objects imported into a package, display objects imported from the same top level package or module.
    # This option does not effect objects imported into a module.
]
autoapi_python_class_content = "class"  # Use only the class docstring for the class documentation.
autoapi_member_order = "bysource"

autoapi_generate_api_docs = True
# Whether to generate API documentation. If this is False, documentation should be generated though the Directives.

autoapi_keep_files = (
    True  # Keep the AutoAPI generated files on the filesystem after the run. Useful for debugging.
)

if "exclude_patterns" not in globals():
    exclude_patterns = ["autoapi_templates"]
else:
    exclude_patterns.append("autoapi_templates")

# add all stubs to the autoapi_dirs
stub_path = Path(__file__).parent / "stubs"
autoapi_dirs: List[Path] = []
autoapi_dirs.extend(
    [p for p in stub_path.glob("*") if p.is_dir() and p.stem not in ["__pycache__"]]
)
