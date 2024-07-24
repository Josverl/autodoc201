.. _micropythonmodules:

MicroPython Modules
===================

This page contains auto-generated module documentation.

.. toctree::
   :titlesonly:
   :maxdepth: 1

   {% for page in pages|selectattr("is_top_level_object")|sort %}
   {{ page.include_path }}
   {% endfor %}

.. [#f1] Created with `sphinx-autoapi <https://github.com/readthedocs/sphinx-autoapi>`_
