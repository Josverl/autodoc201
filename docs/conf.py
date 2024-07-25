# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Stub doc test"
copyright = "Nah"
author = "Jos Verlinde, Jim Mussared et al"
release = "1"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

import sys
import os
import sphinx.util.logging

LOGGER = sphinx.util.logging.getLogger(__name__)
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
TOP_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path[:0] = [os.path.join(TOP_DIR, "extensions"), TOP_DIR]

extensions = [
    "autoapi.extension",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "restore_section",  # Jimmo's extension
]

templates_path = ["_templates"]
exclude_patterns = ["build", "Thumbs.db", ".DS_Store"]

# The suffix of source filenames.
source_suffix = {".rst": "restructuredtext"}
# The master toctree document.
master_doc = "index"
default_role = "any"
pygments_style = "sphinx"
# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = "alabaster"
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

# Global include files. Sphinx docs suggest using rst_epilog in preference
# of rst_prolog, so we follow. Absolute paths below mean "from the base
# of the doctree".
rst_epilog = """
.. include:: /templates/replace.inc
"""
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
from sphinx.application import Sphinx

#  https://sphinx-autoapi.readthedocs.io/en/latest/reference/config.html#confval-autoapi_options
autoapi_options = [
    "members",
    "undoc-members",
    "private-members",  # _foo
    "special-members",  # __foo
    "show-inheritance",  # Display a list of base classes below the class signature.
    "show-module-summary",  # include autosummary directives in generated module documentation
    # "no-index",
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

# Configure customizable templates for the AutoAPI extension.
autoapi_template_dir = (Path(__file__).parent / "autoapi_templates").absolute().as_posix()

if "exclude_patterns" not in globals():
    exclude_patterns = ["autoapi_templates"]
else:
    exclude_patterns.append("autoapi_templates")

# add all .pyi amd .py stubs to autoapi_dirs to be processed

# -----------------------------------------------------------------------------
# add stubs/modulename/__init__.pyi
from stub_docs import (
    copy_module_to_path,
    copy_modules,
    packages_from,
    SKIP_MODULES,
    generate_library_index,
)

stub_path = Path(__file__).parent / "stubs"
temp_path = Path(__file__).parent / "stubs-temp"

autoapi_dirs = packages_from(stub_path)

# -----------------------------------------------------------------------------
# add stubs/modulename.pyi
if lone_pyi := [p for p in stub_path.glob("*.pyi") if p.stem not in SKIP_MODULES]:
    for p in lone_pyi:
        copy_module_to_path(p, temp_path)
# -----------------------------------------------------------------------------

# add lib/micropython-lib/micropython/folder/*.py

mpylib_micropython = copy_modules(Path("../lib/micropython-lib/micropython"), temp_path, ext=".py")
mpylib_cpython_stdlib = copy_modules(
    Path("../lib/micropython-lib/python-stdlib"), temp_path, ext=".py"
)
mpylib_cpython_ecosys = copy_modules(
    Path("../lib/micropython-lib/python-ecosys"), temp_path, ext=".py"
)

# create a dict of module names and their origin to be used in process_docstring
mpy_lib_modules = {}
for m in mpylib_micropython:
    mpy_lib_modules[m.stem] = "micropython-lib"
for m in mpylib_cpython_stdlib:
    mpy_lib_modules[m.stem] = "micropython-stdlib"
for m in mpylib_cpython_ecosys:
    mpy_lib_modules[m.stem] = "micropython-ecosys"

autoapi_dirs.extend(packages_from(temp_path))

# use the jinja2 template to generate the index.rst file based on mpylib_micropython
generate_library_index(
    mpylib_micropython,
    "micropython-lib",
    "library/lib-micropython.rst",
)
generate_library_index(
    mpylib_cpython_stdlib,
    "micropython-stdlib",
    "library/lib-python-stdlib.rst",
)
generate_library_index(
    mpylib_cpython_ecosys,
    "micropython-ecosys",
    "library/lib-python-community.rst",
)

# -----------------------------------------------------------------------------
# # HTML post processing


from bs4 import BeautifulSoup  # BeautifulSoup is used for easier HTML parsing and manipulation


def replace_typeshed_incomplete(app: Sphinx, exception):
    """
    Replace all occurrences of "_typeshed.Incomplete" with "Incomplete" in the generated HTML files.
    """
    if exception is None:  # Only proceed if the build completed successfully
        output_dir = Path(app.outdir)  # Get the output directory where the HTML files are located
        LOGGER.info(f"Replacing _typeshed.Incomplete in HTML files in {output_dir}")
        for file_path in output_dir.glob("**/*.html"):
            with open(file_path, "r", encoding="utf-8") as f:
                html_content = f.read()

            # Use BeautifulSoup to parse the HTML
            soup = BeautifulSoup(html_content, "html.parser")
            html_str = str(soup).replace("_typeshed.Incomplete", "Incomplete")

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html_str)
        LOGGER.info("Replacement complete")


# TODO - make nice / explain
from autoapi._objects import TopLevelPythonPythonMapper

PythonObject = TopLevelPythonPythonMapper


def process_docstring(
    app: Sphinx,
    what: str,  # "module", "class", "exception", "function", "method", "attribute" ( "package", 'data' with autoapi)
    name: str,
    obj: PythonObject,  # Always None with autoapi
    options: dict,  # Always None with autoapi
    lines: List[str],
):

    # sourcery skip: merge-nested-ifs
    if what in {"package", "module"}:
        if name in mpy_lib_modules:
            lines.extend(
                (
                    "",
                    f".. seealso:: This is a {mpy_lib_modules[name]} module from the ``micropython-lib`` repository.",
                )
            )


def process_signature(
    app: Sphinx,
    what: str,
    name: str,
    obj: PythonObject,
    options: dict,
    signature: str | None,
    return_annotation: str | None,
):
    pass


# -----------------------------------------------------------------------------
suppress_warnings = [
    # "ref.doc",
    "any",  #  WARNING: 'any' reference target not found,
    "unknown-document",  # WARNING: unknown document: 'foo' - Temporary for gradual build-up
]
#  WARNING: duplicate object description of <foo>, other instance in
#  WARNING: 'any' reference target not found
#  WARNING: more than one target found for 'any' cross-reference
# :<autosummary>:1: WARNING: more than one target found for 'any' cross-reference
# WARNING: unknown document: 'asyncio'

#  WARNING: more than one target found for 'any' cross-reference 'PIO.IN_LOW': could be :py:attr:`_rp2.PIO.IN_LOW` or :py:attr:`rp2.PIO.PIO.IN_LOW`

# Q&D FIX For  WARNING: toctree contains reference to nonexisting document

from sphinx.environment import BuildEnvironment
from docutils.nodes import inline
from sphinx.addnodes import pending_xref


def on_missing_reference(
    app: Sphinx,
    env: BuildEnvironment,
    node: pending_xref,
    contnode: inline,
):
    """
    Handle/suppress missing `any` references.
    This allows us to use `any` as a type hint without sphinx complaining.
    """
    # https://www.sphinx-doc.org/en/master/extdev/event_callbacks.html#event-missing-reference
    # https://github.com/sphinx-doc/sphinx/issues/2709
    if node["reftype"] == "any":
        return contnode
    else:
        return None


# -----------------------------------------------------------------------------


def setup(sphinx: Sphinx):
    sphinx.connect("autodoc-process-docstring", process_docstring)  # also fires with autoapi :)
    sphinx.connect("autodoc-process-signature", process_signature)  # also fires with autoapi :)
    sphinx.connect("missing-reference", on_missing_reference)
    sphinx.connect("build-finished", replace_typeshed_incomplete)  # clean up html files
