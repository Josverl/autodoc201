"""
System error codes.

MicroPython module: https://docs.micropython.org/en/v1.23.0/library/errno.html

CPython module: :mod:`python:errno` https://docs.python.org/3/library/errno.html .

This module provides access to symbolic error codes for `OSError` exception.
A particular inventory of codes depends on :term:`MicroPython port`.
"""

# source version: v1.23.0
# origin module:: repos/micropython/docs/library/errno.rst
from __future__ import annotations
from typing import Dict
from _typeshed import Incomplete

errorcode: Dict
"""\
Dictionary mapping numeric error codes to strings with symbolic error
code (see above)::

    >>> print(errno.errorcode[errno.EEXIST])
    EEXIST
"""

EPERM = 1
"Operation not permitted"

ENOENT = 2
"No such file or directory"

ESRCH = 3
"No such process"

EINTR = 4
"Interrupted system call"

EIO = 5
"I/O error"

ENXIO = 6
"No such device or address"

E2BIG = 7
"Argument list too long"

ENOEXEC = 8
"Exec format error"

EBADF = 9
"Bad file number"

ECHILD = 10
"No child processes"

EAGAIN = 11
"Try again"

ENOMEM = 12
"Out of memory"

EACCES = 13
"Permission denied"

EFAULT = 14
"Bad address"

ENOTBLK = 15
"Block device required"

EBUSY = 16
"Device or resource busy"

EEXIST = 17
"File exists"

EXDEV = 18
"Cross-device link"

ENODEV = 19
"No such device"

ENOTDIR = 20
"Not a directory"

EISDIR = 21
"Is a directory"

EINVAL = 22
"Invalid argument"

ENFILE = 23
"File table overflow"

EMFILE = 24
"Too many open files"

ENOTTY = 25
"Not a typewriter"

ETXTBSY = 26
"Text file busy"

EFBIG = 27
"File too large"

ENOSPC = 28
"No space left on device"

ESPIPE = 29
"Illegal seek"

EROFS = 30
"Read-only file system"

EMLINK = 31
"Too many links"

EPIPE = 32
"Broken pipe"

EDOM = 33
"Math argument out of domain of func"

ERANGE = 34
"Math result not representable"

EAFNOSUPPORT = 97
"Address family not supported by protocol"

ECONNRESET = 104
"Connection timed out"

ETIMEDOUT = 110
"Connection timed out"
