.. _micropythonmodules:

MicroPython Module Reference
============================

This is an index to documentation for MicroPython modules and MicroPython-lib modules.
The documentation is autogenerated from the MicroPython type-stub files, 
or from the python sources for modules in MicroPython-lib.

.. toctree::
   :titlesonly:
   :maxdepth: 1

   {% for page in pages|selectattr("is_top_level_object")|sort %}
   {{ page.include_path }}
   {% endfor %}

.. [#f1] Created with `sphinx-autoapi <https://github.com/readthedocs/sphinx-autoapi>`_
