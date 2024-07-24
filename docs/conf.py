# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Stub doc test"
copyright = "MIT"
author = "Jos Verlinde, Jim Mussared et al"
release = "1"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

import sys
import os

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
TOP_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(TOP_DIR, "extensions"))

extensions = [
    "autoapi.extension",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "restore_section",  # Jimmo's extension
]

templates_path = ["_templates"]
exclude_patterns = ["build", "Thumbs.db", ".DS_Store"]

# The suffix of source filenames.
source_suffix = ".rst"
# The master toctree document.
master_doc = "index"
default_role = "any"
pygments_style = "sphinx"
# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = "alabaster"
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
# -----------------------------------------------------------------------------
# Configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    "python": ("https://docs.python.org/3.5", None),
    "micropython": ("https://docs.micropython.org/en/latest", None),
    "typing": ("https://typing.readthedocs.io/en/latest/", None),
}

# -----------------------------------------------------------------------------
from pathlib import Path
from typing import Any, List

import sphinx

#  https://sphinx-autoapi.readthedocs.io/en/latest/reference/config.html#confval-autoapi_options
autoapi_options = [
    "members",
    "undoc-members",
    "private-members",  # _foo
    "special-members",  # __foo
    "show-inheritance",  # Display a list of base classes below the class signature.
    "show-module-summary",  # include autosummary directives in generated module documentation
    "noindex",
    # "inherited-members", # Display children of an object that have been inherited from a base class.
    # "imported-members", $# For objects imported into a package, display objects imported from the same top level package or module.
    # This option does not effect objects imported into a module.
]

# autoapi_python_class_content = "class"  # Use only the class docstring for the class documentation.
autoapi_member_order = "groupwise"
autoapi_root = "modules"
# Whether to generate API documentation. If this is False, documentation should be generated though the Directives.
autoapi_generate_api_docs = True

autoapi_add_toctree_entry = True

# Keep the AutoAPI generated files on the filesystem after the run. Useful for debugging.
autoapi_keep_files = True

# onfigure customizable templates for the AutoAPI extension.
autoapi_template_dir = (Path(__file__).parent / "autoapi_templates").absolute().as_posix()

if "exclude_patterns" not in globals():
    exclude_patterns = ["autoapi_templates"]
else:
    exclude_patterns.append("autoapi_templates")

# add all .pyi amd .py stubs to autoapi_dirs to be processed
SKIP_MODULES = [
    "__pycache__",
    "__builtins__",  # This module does not actually exists, is used by Pyright to resolve custom builtins
]

# -----------------------------------------------------------------------------
# add stubs/modulename/__init__.pyi
stub_path = Path(__file__).parent / "stubs"
temp_path = Path(__file__).parent / "stubs-temp"
stub_modules = sorted(
    [p for p in stub_path.glob("*") if p.stem not in SKIP_MODULES and p.is_dir()],
    key=lambda x: x.stem,
)
autoapi_dirs: List[Path] = stub_modules


def copy_mod_to_temp(mod_path: Path):
    """Copy a module to a temp folder with __init__.pyi"""
    with open(mod_path, "r") as f:
        lines = f.readlines()
    dest_path = temp_path / mod_path.stem / "__init__.pyi"
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    with open(dest_path, "w") as f:
        for line in lines:
            f.write(line)


# -----------------------------------------------------------------------------
# add stubs/modulename.pyi
if lone_pyi := [p for p in stub_path.glob("*.pyi") if p.stem not in SKIP_MODULES]:
    for p in lone_pyi:
        copy_mod_to_temp(p)
# -----------------------------------------------------------------------------


def temp_mods(lib_path):
    if lib_py := [p for p in lib_path.rglob("*.py") if p.stem == p.parent.stem]:
        for p in lib_py:
            copy_mod_to_temp(p)

    return sorted(
        [p for p in temp_path.glob("*") if p.stem not in SKIP_MODULES and p.is_dir()],
        key=lambda x: x.stem,
    )


# add lib/micropython-lib/micropython/folder/*.py

autoapi_dirs.extend(
    temp_mods(Path(__file__).parent.parent / "lib" / "micropython-lib" / "micropython")
)
autoapi_dirs.extend(
    temp_mods(Path(__file__).parent.parent / "lib" / "micropython-lib" / "python-stdlib")
)
autoapi_dirs.extend(
    temp_mods(Path(__file__).parent.parent / "lib" / "micropython-lib" / "python-ecosys")
)

# -----------------------------------------------------------------------------
# HTML post processing

from bs4 import BeautifulSoup  # BeautifulSoup is used for easier HTML parsing and manipulation
from sphinx.application import Sphinx


def replace_typeshed_incomplete(app: Sphinx, exception):
    """
    Replace all ocurrences of "_typeshed.Incomplete" with "Incomplete" in the generated HTML files.
    """
    if exception is None:  # Only proceed if the build completed successfully
        output_dir = Path(app.outdir)  # Get the output directory where the HTML files are located
        print(f"Replacing _typeshed.Incomplete in HTML files in {output_dir}")
        for file_path in output_dir.glob("**/*.html"):
            with open(file_path, "r", encoding="utf-8") as f:
                html_content = f.read()

            # Use BeautifulSoup to parse the HTML
            soup = BeautifulSoup(html_content, "html.parser")
            html_str = str(soup).replace("_typeshed.Incomplete", "Incomplete")

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html_str)
        print("Replacement complete")


def setup(app: Sphinx):
    app.connect("build-finished", replace_typeshed_incomplete)
