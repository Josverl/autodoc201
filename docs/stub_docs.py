import contextlib
from dataclasses import dataclass
from pathlib import Path
from typing import List
from sphinx.application import Sphinx
import sphinx.util.logging

# TODO: - make nice / explain
from autoapi._objects import TopLevelPythonPythonMapper

PythonObject = TopLevelPythonPythonMapper

log = sphinx.util.logging.getLogger(__name__)

SKIP_MODULES = [
    "__pycache__",
    "__builtins__",  # This module does not actually exists, is used by Pyright to resolve custom builtins
]


@dataclass
class ModuleOrigin:
    """Dataclass to hold the origin of a module"""

    origin_path: Path
    path: Path
    category: str = ""
    author: str = ""
    license: str = ""
    repo: str = ""
    url: str = ""

    @property
    def name(self) -> str:
        return self.origin_path.stem

    def github_url_from_path(
        self,
        mpy_lib_path: Path,
        repo: str = "https://github.com/micropython/micropython-lib",
        branch: str = "master",
    ) -> str:
        return f"{repo}/tree/{branch}/{self.origin_path.resolve().relative_to(mpy_lib_path.resolve()).as_posix()}"


class ModuleCollector:
    """
    Collect modules from a folder and copy them to a destination folder in a package form for autoapi
    """

    def __init__(self, temp_path: Path) -> None:
        self.temp_path = temp_path

    def copy_module_to_path(self, mod_path: Path, dest_path: Path, ext=".pyi") -> ModuleOrigin:
        """
        Copy a module to a folder
        TODO: Needs to be rewritten to use manifest.py to copy the correct files for more complex modules

        source form : module.py
        destination form : module/__init__.pyi

        """
        with open(mod_path, "r") as f:
            lines = f.readlines()
        mod_name = mod_path.stem
        dest_path = dest_path / mod_name / f"__init__{ext}"
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        if not lines[0].startswith('"""'):
            # Add a basic module docstring, to enable docstring pre-processing.
            lines[:0] = ['"""\n', f"{mod_name} for MicroPython.", '"""\n']

        with open(dest_path, "w") as f:
            for line in lines:
                f.write(line)
        return ModuleOrigin(mod_path, dest_path)

    def copy_modules(self, lib_path: Path, temp_path: Path, ext=".py") -> List[ModuleOrigin]:
        """
        Copy all modules from a micropython-lib folder to a destination folder
        restructure the module to a package for autoapi
        """
        if not lib_path.is_absolute():
            lib_path = Path(Path(__file__).parent) / lib_path

        result: List[ModuleOrigin] = []
        # copy only modules that have the same name as the parent folder
        # .../foo/foo.py -> .../foo/__init__.py
        # ../foo/test.py     not copied
        if lib_py := [p for p in lib_path.rglob(f"*{ext}") if p.stem == p.parent.stem]:
            # do not copy the errno module, it is a special case
            # TODO: Need to avoid copying in modules that are already documented as part of the micropython library
            # or at least avoid name conflicts
            result.extend(
                self.copy_module_to_path(p, temp_path, ext)
                for p in lib_py
                # if p.stem not in ["errno"]
            )
        return result

    def packages_from(self, stub_path: Path, skip=SKIP_MODULES):
        """Create a list of packages from a folder to be used in autoapi_dirs"""
        return [p for p in stub_path.glob("*") if p.stem not in skip and p.is_dir()]


################################################################################################################
# Docstring preprocessing
################################################################################################################


class DocstringProcessor:
    # revert some of the changes that stubber does to the docstrings to improve the readability
    reverts = [
        (r"CPython module: *([:\w`]+).*", r"|see_cpython_module| \1."),  # TODO :
        ("``Note:`` ", ".. note:: "),
        ("Note: ", ".. note:: "),
        ("Admonition: ", ".. admonition:: "),
        ("#### Need placeholder ####", ".. data:: "),
    ]

    def __init__(self, mpy_lib_modules: dict[str, ModuleOrigin] | None = None):

        # store the names of the micropython-lib modules and their origin
        self.mpy_lib_modules = mpy_lib_modules or {}

    def revert_stubber_mods(self, lines: List[str]):
        """
        Revert some of the changes that stubber does to the docstrings to improve the readability

        - Remove line starting with "MicroPython Module" from the micropython-stubs
          as that is pointing to this generated page
        - reinstate the ".. note::" directive
        """
        for i, l in enumerate(lines):
            if l.startswith("MicroPython module:"):
                # remove 1 or 2 lines in place
                lines.pop(i)
                if len(lines) > i and lines[i] == "":
                    lines.pop(i)
                break

        # Reverse Stubber docstring clean-ups Clean up note and other docstring anchors
        for i, l in enumerate(lines):
            for old, new in self.reverts:
                # with contextlib.suppress(re.error):
                lines[i] = re.sub(old, new, lines[i])

    def add_micropython_lib_note(self, lines: List[str], name: str):
        """
        Add a note to the docstring of a module from the micropython-lib repository.
        """
        if name in self.mpy_lib_modules:
            lines.extend(
                (
                    "",
                    ".. tip::",
                    f"    This is a `{self.mpy_lib_modules[name].category}` module from the ``micropython-lib`` repository.",
                    f"    It can be installed to a MicroPython board using::",
                    "",
                    f"        mpremote mip install {name}",
                    "",
                    f"    Source: {self.mpy_lib_modules[name].repo}",
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
        """
        Process the docstring of a module from the micropython-lib repository.

        Note:
            `lines` must  be modified in place, rather than a new value being assigned.
            To modify the contents of the lines list in-place, you can use list methods like:
            append(), extend(), or index assignment (lines[index] = value).

        """
        if what in {"package", "module"}:
            if name in self.mpy_lib_modules:
                self.add_micropython_lib_note(lines, name)

            self.revert_stubber_mods(lines)


################################################################################################################
# Generate the index.rst file for the modules in micropython-lib
################################################################################################################
from jinja2 import Environment, FileSystemLoader
import re

# Configure customizable templates for the AutoAPI extension.
autoapi_template_dir = (Path(__file__).parent / "autoapi_templates").absolute().as_posix()

# Load the Jinja2 template
env = Environment(loader=FileSystemLoader(autoapi_template_dir))
template = env.get_template("mpy-lib_index.rst")


def generate_library_index(mpylib_micropython: List[ModuleOrigin], title: str, output_file: str):
    """
    Generate the index.rst file for the modules in micropython-lib
    Args:
        mpylib_micropython (List[Path]): List of paths to the modules
        title (str): Title of the index.rst file
        output_file (str): Path to the output file

    TODO: Add more information to the index
        - mip icon / link to install
        - get author / tile / license
        - integrate this more with Sphinx/autoapi
    """
    rendered_content = template.render(modules=mpylib_micropython, title=title)
    # Write the rendered content to index.rst
    with open(output_file, "w") as f:
        f.write(rendered_content)
