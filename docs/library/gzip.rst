:mod:`gzip` -- gzip compression & decompression
===============================================

.. autoapimodule:: gzip
    :synopsis: gzip compression & decompression
    :no-index:
    :members:
    :undoc-members:
    :private-members: 
    :special-members:


Examples
--------

A typical use case for :class:`gzip.GzipFile` is to read or write a compressed
file from storage:

.. code:: python

   import gzip

   # Reading:
   with open("data.gz", "rb") as f:
       with gzip.GzipFile(fileobj=f, mode="rb") as g:
           # Use g.read(), g.readinto(), etc.

    # Same, but using gzip.open:
   with gzip.open("data.gz", "rb") as f:
        # Use f.read(), f.readinto(), etc.

   # Writing:
   with open("data.gz", "wb") as f:
       with gzip.GzipFile(fileobj=f, mode="wb") as g:
           # Use g.write(...) etc

   # Same, but using gzip.open:
   with gzip.open("data.gz", "wb") as f:
       # Use f.write(...) etc

   # Write a dictionary as JSON in gzip format, with a
   # small (64 byte) window size.
   config = { ... }
   with gzip.open("config.gz", "wb") as f:
       json.dump(config, f)

For guidance on working with gzip sources and choosing the window size see the
note at the :ref:`end of the deflate documentation <deflate_wbits>`.