.. _{{ title }}modules:

{{ title }}
===========================================================

This index contains modules from the MicroPython-lib library.

.. toctree::
   :titlesonly:
   :maxdepth: 1

{% for mod in modules %}
    /modules/{{ mod.path.parent.parent.stem }}/{{ mod.name }}/index{% endfor %}

