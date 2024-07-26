:mod:`os` -- basic "operating system" services
==============================================

.. autoapimodule:: os
    :no-index:

General functions
-----------------

.. autoapifunction:: uname
    :no-index:

.. autoapifunction:: urandom
    :no-index:

Filesystem access
-----------------

.. autoapifunction:: chdir
    :no-index:


.. autoapifunction:: getcwd
    :no-index:


.. autoapifunction:: ilistdir
    :no-index:


.. autoapifunction:: listdir
    :no-index:


.. autoapifunction:: mkdir
    :no-index:


.. autoapifunction:: remove
    :no-index:


.. autoapifunction:: rmdir
    :no-index:


.. autoapifunction:: rename
    :no-index:


.. autoapifunction:: stat
    :no-index:


.. autoapifunction:: statvfs
    :no-index:


.. autoapifunction:: sync
    :no-index:


Terminal redirection and duplication
------------------------------------

.. autoapifunction:: dupterm
    :no-index:


Filesystem mounting
-------------------

The following functions and classes have been moved to the :mod:`vfs` module.
They are provided in this module only for backwards compatibility and will be
removed in version 2 of MicroPython.

.. autoapifunction:: mount
    :no-index:

.. autoapifunction:: umount
    :no-index:

.. autoapiclass:: VfsFat
    :no-index:

.. autoapiclass:: VfsLfs1
    :no-index:

.. autoapiclass:: VfsLfs2
    :no-index:

.. autoapiclass:: VfsPosix
    :no-index:
