"""
JSON encoding and decoding.

MicroPython module: https://docs.micropython.org/en/v1.23.0/library/json.html

CPython module: :mod:`python:json` https://docs.python.org/3/library/json.html .

This modules allows to convert between Python objects and the JSON
data format.
"""

# source version: v1.23.0
# origin module:: repos/micropython/docs/library/json.rst
from __future__ import annotations
from _typeshed import SupportsRead, SupportsWrite
from typing import Any, Iterable

def dump(obj: Any, stream: SupportsWrite[str], separators: Iterable = (", ", ": ")) -> None:
    """
    Serialise *obj* to a JSON string, writing it to the given *stream*.

    If specified, separators should be an ``(item_separator, key_separator)``
    tuple. The default is ``(', ', ': ')``. To get the most compact JSON
    representation, you should specify ``(',', ':')`` to eliminate whitespace.
    """
    ...

def dumps(obj, separators=None) -> str:
    """
    Return *obj* represented as a JSON string.

    The arguments have the same meaning as in `dump`.
    """
    ...

def load(stream: SupportsRead[str | bytes]) -> object:
    """
    Parse the given *stream*, interpreting it as a JSON string and
    deserialising the data to a Python object.  The resulting object is
    returned.

    Parsing continues until end-of-file is encountered.
    A :exc:`ValueError` is raised if the data in *stream* is not correctly formed.
    """
    ...

def loads(str) -> object:
    """
    Parse the JSON *str* and return an object.  Raises :exc:`ValueError` if the
    string is not correctly formed.
    """
    ...
