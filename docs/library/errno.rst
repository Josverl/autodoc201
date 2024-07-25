:mod:`errno` -- system error codes
==================================

.. module:: errno
   :synopsis: system error codes

|see_cpython_module| :mod:`python:errno`.

This module provides access to symbolic error codes for `OSError` exception.
A particular inventory of codes depends on :term:`MicroPython port`.

Constants
---------
.. TODO: Link to the the autoapi module for the error codes.

.. data:: EEXIST, EAGAIN, etc.
    :no-index:    

    Error codes, based on ANSI C/POSIX standard. All error codes start with
    "E". As mentioned above, inventory of the codes depends on
    :term:`MicroPython port`. Errors are usually accessible as ``exc.errno``
    where ``exc`` is an instance of `OSError`. Usage example::

        try:
            os.mkdir("my_dir")
        except OSError as exc:
            if exc.errno == errno.EEXIST:
                print("Directory already exists")

.. autoapidata:: errorcode
    :no-index:    
