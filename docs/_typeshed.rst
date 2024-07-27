:mod:`_typeshed` -- Utility types for typeshed.
===============================================

The ``_typeshed`` package and its types do not exist at runtime, but can be used freely in stubs (.pyi) files

See: https://github.com/python/typeshed/tree/main/stdlib/_typeshed#utility-types-for-typeshed

.. .. data:: Incomplete

.. class:: Incomplete()
    :module: _typeshed

    For partially known annotations. Usually, fields where type annotations
    haven't been added are left unannotated, but in some situations this
    isn't possible or a type is already partially known. In cases like these,
    use Incomplete instead of Any as a marker. For example, use::

        "Incomplete | None" instead of "Any | None".

    In the context of MicroPython and the micropython-stubs, `Incomplete` is used 
    to mark functions and classes that are not yet fully documented. 

    This allows anyone to distinguish methods that are not yet documented from those
    that return a value of class `Any <python:typing.Any>`.

    If you encounter a method that is marked as ``Incomplete``, you can help by 
    updating that function , method or or class in the stub file (foo_bar.pyi) 
    and submitting a pull request with your changes.

