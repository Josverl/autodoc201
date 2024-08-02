from typing import List
import pytest
from stub_docs import DocstringProcessor


@pytest.mark.parametrize(
    "lines, expected",
    [
        (["foo"], ["foo"]),
        (["MicroPython module: foo"], []),
        (["MicroPython module: foo", ""], []),
        (["CPython module: bar"], ["|see_cpython_module| bar."]),
        (["CPython module: bar https:some.where://foo.bar"], ["|see_cpython_module| bar."]),
    ],
)
def test_revert_stubber_mods(lines: List[str], expected: List[str]):
    processor = DocstringProcessor()
    processor.revert_stubber_mods(lines)
    assert lines == expected


@pytest.mark.parametrize(
    "what",
    [
        "module",
        "package",
    ],
)
@pytest.mark.parametrize(
    "lines, expected",
    [
        (["foo"], ["foo"]),
        (["MicroPython module: foo"], []),
        (["MicroPython module: foo", ""], []),
        (["CPython module: bar"], ["|see_cpython_module| bar."]),
        (["CPython module: bar https:some.where://foo.bar"], ["|see_cpython_module| bar."]),
    ],
)
def test_process_docstring(what, lines, expected):
    processor = DocstringProcessor()
    app = None
    name = "module_name"
    obj = None
    options = None

    processor.process_docstring(app, what, name, obj, options, lines)
    assert lines == expected
