:mod:`os` -- basic "operating system" services
==============================================

.. autoapimodule:: os
    :no-index:

General functions
-----------------

.. autoapifunction:: uname()
    :no-index:

.. autoapifunction:: urandom(n)
    :no-index:

Filesystem access
-----------------

.. autoapifunction:: chdir(path)
    :no-index:


.. autoapifunction:: getcwd()
    :no-index:


.. autoapifunction:: ilistdir([dir])
    :no-index:


.. autoapifunction:: listdir([dir])
    :no-index:


.. autoapifunction:: mkdir(path)
    :no-index:


.. autoapifunction:: remove(path)
    :no-index:


.. autoapifunction:: rmdir(path)
    :no-index:


.. autoapifunction:: rename(old_path, new_path)
    :no-index:


.. autoapifunction:: stat(path)
    :no-index:


.. autoapifunction:: statvfs(path)
    :no-index:


.. autoapifunction:: sync()
    :no-index:


Terminal redirection and duplication
------------------------------------

.. autoapifunction:: dupterm()
    :no-index:


Filesystem mounting
-------------------

The following functions and classes have been moved to the :mod:`vfs` module.
They are provided in this module only for backwards compatibility and will be
removed in version 2 of MicroPython.

.. autoapifunction:: mount()
    :no-index:

.. autoapifunction:: umount(mount_point)
    :no-index:

.. autoapiclass:: VfsFat(block_dev)
    :no-index:

.. autoapiclass:: VfsLfs1(block_dev, readsize=32, progsize=32, lookahead=32)
    :no-index:

.. autoapiclass:: VfsLfs2(block_dev, readsize=32, progsize=32, lookahead=32, mtime=True)
    :no-index:

.. autoapiclass:: VfsPosix(root=None)
    :no-index:
