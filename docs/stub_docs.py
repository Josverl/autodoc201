from pathlib import Path
from typing import List

SKIP_MODULES = [
    "__pycache__",
    "__builtins__",  # This module does not actually exists, is used by Pyright to resolve custom builtins
]


def copy_module_to_path(mod_path: Path, dest_path: Path, ext=".pyi") -> Path:
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


def copy_modules(lib_path: Path, temp_path: Path, ext=".py") -> List[Path]:
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
        result.extend(copy_module_to_path(p, temp_path, ext) for p in lib_py)
    return result


def packages_from(stub_path: Path, skip=SKIP_MODULES):
    """Create a list of packages from a folder to be used in autoapi_dirs"""
    return [p for p in stub_path.glob("*") if p.stem not in skip and p.is_dir()]
