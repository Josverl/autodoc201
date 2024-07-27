.. _{{ title }}modules:

{{ title }}
===========================================================

This index contains modules from the MicroPython-lib library.

.. toctree::
   :titlesonly:
   :maxdepth: 1

{% for mo in modules %}
   /modules/{{ mo.name }}/index{% endfor %}

