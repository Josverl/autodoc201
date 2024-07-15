## Autodoc-Style Directives

You can opt to write API documentation yourself using autodoc style directives. These directives work similarly to autodoc, but docstrings are retrieved through static analysis instead of through imports.
For Python, all directives have an autodoc equivalent and accept the same options. The following directives are available:

.. autoapimodule::
.. autoapiclass::
.. autoapiexception::

Equivalent to automodule, autoclass, and autoexception respectively. autodoc_inherit_docstrings does not currently work.

.. autoapifunction::
.. autoapidata::
.. autoapimethod::
.. autoapiattribute::

Equivalent to autofunction, autodata, automethod, and autoattribute respectively.

see: https://sphinx-autoapi.readthedocs.io/en/latest/reference/directives.html


.. autoapimodule:: array
   :members:
   :undoc-members:
   :private-members: 
   :special-members:
   :show-inheritance:
   :exclude-members: __init__, __weakref__


   .. autoapiclass:: btree
   :members:
   :undoc-members:
   :private-members: 
   :special-members:
