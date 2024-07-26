from pathlib import Path
from typing import List
from sphinx.application import Sphinx
import sphinx.util.logging

# TODO: - make nice / explain
from autoapi._objects import TopLevelPythonPythonMapper

PythonObject = TopLevelPythonPythonMapper

LOGGER = sphinx.util.logging.getLogger(__name__)

SKIP_MODULES = [
    "__pycache__",
    "__builtins__",  # This module does not actually exists, is used by Pyright to resolve custom builtins
]


class ModuleCollector:
    def __init__(self, temp_path: Path) -> None:
        self.temp_path = temp_path

    def copy_module_to_path(self, mod_path: Path, dest_path: Path, ext=".pyi") -> Path:
        """
        Copy a module to a folder

        source form : module.py
        destination form : module/__init__.pyi

        """
        with open(mod_path, "r") as f:
            lines = f.readlines()
        dest_path = dest_path / mod_path.stem / f"__init__{ext}"
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        with open(dest_path, "w") as f:
            for line in lines:
                f.write(line)
        return dest_path

    def copy_modules(self, lib_path: Path, temp_path: Path, ext=".py") -> List[Path]:
        """ "
        Copy all modules from a micropython-lib folder to a destination folder
        restructure the module to a package for autoapi
        """
        if not lib_path.is_absolute():
            lib_path = Path(Path(__file__).parent) / lib_path

        result: List[Path] = []
        # copy only modules that have the same name as the parent folder
        # .../foo/foo.py -> .../foo/__init__.py
        # ../foo/test.py     not copied
        if lib_py := [p for p in lib_path.rglob(f"*{ext}") if p.stem == p.parent.stem]:
            result.extend(self.copy_module_to_path(p, temp_path, ext) for p in lib_py)
        return result

    def packages_from(self, stub_path: Path, skip=SKIP_MODULES):
        """Create a list of packages from a folder to be used in autoapi_dirs"""
        return [p for p in stub_path.glob("*") if p.stem not in skip and p.is_dir()]


################################################################################################################
# Docstring preprocessing
################################################################################################################
class DocstringProcessor:
    def __init__(self, mpy_lib_modules: dict[str, str]):
        # store the names of the micropython-lib modules and their origin
        self.mpy_lib_modules = mpy_lib_modules

    def revert_stubber_mods(self, lines: List[str]):
        """
        Revert some of the changes that stubber does to the docstrings to improve the readability

        - Remove line starting with "MicroPython Module" from the micropython-stubs
          as that is pointing to this generated page
        - reinstate the ".. note::" directive
        """
        for i, l in enumerate(lines):
            if l.startswith("MicroPython module: https://"):
                snip = 2 if lines[i + 1] == "" else 1
                lines = lines[:i] + lines[i + snip :]
                break
        for l in lines:
            # Reverse Stubber docstring clean-ups Clean up note and other docstring anchors
            if l:
                l = l.replace("``Note:`` ", ".. note:: ")
                l = l.replace("Note: ", ".. note:: ")
                l = l.replace("``Admonition:``", ".. admonition:: ")
                l = l.replace("Admonition:", ".. admonition:: ")
                l = l.replace("CPython module:", "|see_cpython_module|")
                l = l.replace("#### Need placeholder ####", ".. data:: ")

    def add_micropython_lib_note(self, lines: List[str], name: str):
        """
        Add a note to the docstring of a module from the micropython-lib repository.
        """
        if name in self.mpy_lib_modules:
            lines.extend(
                (
                    "",
                    f".. seealso:: This is a {self.mpy_lib_modules[name]} module from the ``micropython-lib`` repository.",
                )
            )

    def process_docstring(
        self,
        app: Sphinx,
        what: str,  # "module", "class", "exception", "function", "method", "attribute" ( "package", 'data' with autoapi)
        name: str,
        obj: PythonObject,  # Always None with autoapi
        options: dict,  # Always None with autoapi
        lines: List[str],
    ):

        if what in {"package", "module"}:
            if name in self.mpy_lib_modules:
                self.add_micropython_lib_note(lines, name)
            else:
                self.revert_stubber_mods(lines)
                # TODO: restore formatting of cpython reference in the docstring


################################################################################################################
# Generate the index.rst file for the modules in micropython-lib
################################################################################################################
from jinja2 import Environment, FileSystemLoader

# Configure customizable templates for the AutoAPI extension.
autoapi_template_dir = (Path(__file__).parent / "autoapi_templates").absolute().as_posix()

# Load the Jinja2 template
env = Environment(loader=FileSystemLoader(autoapi_template_dir))
template = env.get_template("mpylib_index.rst")


def generate_library_index(mpylib_micropython: List[Path], title: str, output_file: str):
    """
    Generate the index.rst file for the modules in micropython-lib
    Args:
        mpylib_micropython (List[Path]): List of paths to the modules
        title (str): Title of the index.rst file
        output_file (str): Path to the output file
    """
    rendered_content = template.render(modules=mpylib_micropython, title=title)
    # Write the rendered content to index.rst
    with open(output_file, "w") as f:
        f.write(rendered_content)


################################################################################################################
# HTML post processing
################################################################################################################

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
