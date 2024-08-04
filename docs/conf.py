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
# -------------------
# The MICROPY_VERSION env var should be "vX.Y.Z" (or unset).
micropy_version = os.getenv("MICROPY_VERSION") or "latest"
micropy_all_versions = (os.getenv("MICROPY_ALL_VERSIONS") or "latest").split(",")
url_pattern = "%s/en/%%s" % (os.getenv("MICROPY_URL_PREFIX") or "/",)

# The members of the html_context dict are available inside topindex.html
html_context = {
    "cur_version": micropy_version,
    "all_versions": [(ver, url_pattern % ver) for ver in micropy_all_versions],
    "downloads": [
        ("PDF", url_pattern % micropy_version + "/micropython-docs.pdf"),
    ],
    "is_release": micropy_version != "latest",
}

# -------------------

extensions = [
    "autoapi.extension",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "restore_section",  # Jimmo's extension
    "sphinx_copybutton",
]

templates_path = ["templates"]
exclude_patterns = ["build", "Thumbs.db", ".DS_Store"]

# The suffix of source filenames.
source_suffix = {
    ".rst": "restructuredtext",
    # ".md": "markdown",
}
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


# TODO: avoid name conflicts with the stubs
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
# mpy_lib_modules = copy_modules_from_lib(temp_path, mc)

# for sub in MPY_LIB_MAP.values():
#     # to avoid naming conflicts with the modules directly uses in micropython
#     # the modules are copied to a subfolder and parsed as a submodule
#     # this also causes a rename of the module to the subfolder name
#     sub_path = temp_path / sub
#     sub_path.mkdir(exist_ok=True)
#     (sub_path / "__init__.py").touch()
#     autoapi_dirs.append(sub_path)

ds_pp = DocstringProcessor(mpy_lib_modules)


# -----------------------------------------------------------------------------
from autoapi._objects import PythonPackage
import pathlib


def autoapi_skip_hook(
    app: sphinx, what: str, name: str, obj: PythonObject, skip: bool, options: dict
):
    """`
    Determine whether to skip a member in the AutoAPI documentation.

    Return True to skip the member, False to include it, None to defer to the default implementation.
    """

    return None


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
# https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-suppress_warnings
suppress_warnings = [
    # "ref.doc",
    "any",  #  WARNING: 'any' reference target not found,
    "unknown-document",  # WARNING: unknown document: 'foo' - Temporary for gradual build-up
]

# types display with a short, PEP 604-inspired syntax, i.e.:
#   serve_food(item: "egg" | "spam" | "lobster thermidor") -> None
python_display_short_literal_types = True

# Wrap long / complex parameter signatures in the Python domain
# not activated during the PoC as this makes it harder to compare the generated documentation with the current HTML pages
# python_maximum_signature_line_length = 100

# This helps to avoid _typeshed.Incomplete in the documentation
# but not in all cases
python_use_unqualified_type_names = True  # Experimental

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


# -- Options for HTML output ----------------------------------------------

# on_rtd is whether we are on readthedocs.org
# on_rtd = os.environ.get("READTHEDOCS", None) == "True"

# if not on_rtd:  # only import and set the theme if we're building docs locally
#     try:
#         import sphinx_rtd_theme

#         html_theme = "sphinx_rtd_theme"
#         html_theme_path = [sphinx_rtd_theme.get_html_theme_path(), "."]
#     except:
#         html_theme = "default"
#         html_theme_path = ["."]
# else:
#     html_theme_path = ["."]

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
# html_theme_options = {}

# Add any paths that contain custom themes here, relative to this directory.
# html_theme_path = ['.']

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
# html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
# html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
# html_logo = '../../logo/trans-logo.png'

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = "static/favicon.ico"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["static"]

# Add a custom CSS file for HTML generation
html_css_files = [
    "custom.css",
]
# Add any extra paths that contain custom files (such as robots.txt or
# .htaccess) here, relative to this directory. These files are copied
# directly to the root of the documentation.
# html_extra_path = []

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = "%d %b %Y"

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
# html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
# html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
html_additional_pages = {"index": "topindex.html"}

# If false, no module index is generated.
# html_domain_indices = True

# If false, no index is generated.
# html_use_index = True

# If true, the index is split into individual pages for each letter.
# html_split_index = False

# If true, links to the reST sources are added to the pages.
# html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
# html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
# html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
# html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
# html_file_suffix = None

# Output file base name for HTML help builder.
htmlhelp_basename = "MicroPythondoc"
# -----------------------------------------------------------------------------


def setup(sphinx: Sphinx):
    # several autodoc events also fire with autoapi :)
    sphinx.connect("autodoc-process-docstring", ds_pp.process_docstring)
    # sphinx.connect("autodoc-process-signature", process_signature) # not used
    sphinx.connect("autoapi-skip-member", autoapi_skip_hook)

    sphinx.connect("missing-reference", on_missing_reference)
