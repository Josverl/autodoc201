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

from dataclasses import dataclass
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
    "sphinx_copybutton",
]

templates_path = ["_templates"]
exclude_patterns = ["build", "Thumbs.db", ".DS_Store"]

# The suffix of source filenames.
source_suffix = {".rst": "restructuredtext"}
# The master toctree document.
master_doc = "index"
default_role = "any"
pygments_style = "sphinx"
# -- Options copy button -------------------------------------------------
# https://github.com/executablebooks/sphinx-copybutton/blob/master/docs/use.md
copybutton_exclude = ".linenos, .gp"
copybutton_prompt_text = ">>> "
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
    # "python": ("https://docs.python.org/3", None),
    "typing": ("https://typing.readthedocs.io/en/latest/", None),
    # add micropython as this PoC does not contain the full documentation,
    # this helps to resolve some references to the rest of the documentation.
    "micropython": ("https://docs.micropython.org/en/latest", None),
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
    # "inherited-members", # Display children of an object that have been inherited from a base class.
    # "imported-members", $# For objects imported into a package, display objects imported from the same top level package or module.
    # This option does not effect objects imported into a module.
]

# autoapi_python_class_content = "class"  # Use only the class docstring for the class documentation.
autoapi_member_order = "groupwise"  # by type, then alphabetically
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
    ModuleCollector,
    SKIP_MODULES,
    generate_library_index,
    DocstringProcessor,
    PythonObject,
    ModuleOrigin,
)

stub_path = Path(__file__).parent / "stubs"
temp_path = Path(__file__).parent / "stubs-temp"

mc = ModuleCollector(temp_path)
autoapi_dirs = mc.packages_from(stub_path)


# -----------------------------------------------------------------------------
# add lib/micropython-lib/micropython/folder/*.py

# mapping from the folders in micropython-lib to the folder in the destination folder
MPY_LIB_MAP = {
    "micropython": "micropython-lib",
    "python-stdlib": "micropython-stdlib",
    "python-ecosys": "micropython-ecosys",
}


def copy_modules_from_lib(dest_path: Path, mc: ModuleCollector) -> dict[str, ModuleOrigin]:
    """
    Copy all modules from the micropython-lib folder to a destination folder.

    returns a dict of module names and their origin to be used in process_docstring
    """
    mpy_lib_path = Path("../lib/micropython-lib")
    # TODO: copy info folder to avoid name conflicts with the stubs
    # there are a few modules in the micropython-lib that have the same name as the stubs but have a different implementation.
    # note sure what the side effects will be for the documentation and linking though ...
    # examples are : heapq
    mpy_lib = {}
    mpy_lib_modules = {}
    for folder_name, display_name in MPY_LIB_MAP.items():
        # copy the modules to a subfolder to avoid name conflicts with the stubs
        # and remember which module is copied from where, to be able to reference
        (dest_path / display_name).mkdir(exist_ok=True, parents=True)
        mpy_lib[folder_name] = mc.copy_modules(
            mpy_lib_path / folder_name, dest_path / display_name, ext=".py"
        )
        for mod in mpy_lib[folder_name]:
            mod.category = folder_name
            mod.repo = mod.github_url_from_path(mpy_lib_path)
            mpy_lib_modules[mod.name] = mod

        # Create an index.rst file for the modules in the micropython-lib
        # Disabled for now - re-use the autogenerated indexes for the micropython-lib 'compound modules'.
        # generate_library_index(mpy_lib[folder_name], display_name, f"mpy-lib/{display_name}.rst")

    return mpy_lib_modules


mpy_lib_modules = {}
mpy_lib_modules = copy_modules_from_lib(temp_path, mc)

for sub in MPY_LIB_MAP.values():
    # to avoid naming conflicts with the modules directly uses in micropython
    # the modules are copied to a subfolder and parsed as a submodule
    # this also causes a rename of the module to the subfolder name
    sub_path = temp_path / sub
    sub_path.mkdir(exist_ok=True)
    (sub_path / "__init__.py").touch()
    autoapi_dirs.append(sub_path)

ds_pp = DocstringProcessor(mpy_lib_modules)


# -----------------------------------------------------------------------------
from autoapi._objects import PythonPackage
import pathlib


# def autoapi_skip_hook(
#     app: sphinx, what: str, name: str, obj: PythonObject, skip: bool, options: dict
# ):
#     """`
#     Determine whether to skip a member in the AutoAPI documentation.

#     Return True to skip the member, False to include it, None to defer to the default implementation.
#     """

#     return None


# -----------------------------------------------------------------------------


# def process_signature(
#     app: Sphinx,
#     what: str,
#     name: str,
#     obj: PythonObject,
#     options: dict,
#     signature: str | None,
#     return_annotation: str | None,
# ):
#     pass


# -----------------------------------------------------------------------------
suppress_warnings = [
    # "ref.doc",
    "any",  #  WARNING: 'any' reference target not found,
    "unknown-document",  # WARNING: unknown document: 'foo' - Temporary for gradual build-up
]

# -----------------------------------------------------------------------------
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
    # several autodoc events also fire with autoapi :)
    sphinx.connect("autodoc-process-docstring", ds_pp.process_docstring)
    # sphinx.connect("autodoc-process-signature", process_signature) # not used
    # sphinx.connect("autoapi-skip-member", autoapi_skip_hook)

    sphinx.connect("missing-reference", on_missing_reference)
