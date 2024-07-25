.. _{{ title }}modules:

{{ title }}
===========================================================

This index contains modules from the MicroPython-lib library.

.. toctree::
   :titlesonly:
   :maxdepth: 1

{% for path in modules %}
   /modules/{{ path.parent.stem }}/index{% endfor %}

