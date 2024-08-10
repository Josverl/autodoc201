# Testground from Micropython Documentation

See: https://github.com/orgs/micropython/discussions/15463
## Work in Progress

To Implement this the following steps are needed 

 [ ] Create a documentation guide that helps contributors decide how to best document things. This can also be used as the basis to create Jinja templates that are used by AutoAPI.
 [ ] Select the relevant type-stubs and add them to the micropython repo 
  ( docs/stubs/library)
 [x] Add the Sphinx AutoAPI and relevant configuration 
 [x] Customize AutoAPI's jinja templates used to generate documentation 
 [ ] Update the existing .rST documents.
  Per document in docs/library:
  - Update the various python references to their autoapi equivalents:
    - `.. module::` --> `.. autoapimodule::`
    - `.. function::`-->`.. autoapifunction::`
    - `.. class::`-->`.. autoapiclass::`
    - etc...
  - Remove associated details for that topic 
  - regenerate the docs using `make -C ./docs`
  - check for errors and completeness
  [x] verify if overloads can be added to the stubs and rendered correctly
        ```python
            @overload
            def value(self, x: None) -> int: ...
            @overload
            def value(self, x: Any) -> None:
        ```
 [x] configure autoapi to document class __inits__ as part of the class parameters , not of the __init__ method
     This is the way the current docs are written , its best to keep it to the same method    


 [ ] Docstring pre-processing to 
    [ ] Update stubber to 
        [x] remove fewer of the .rst .. admonitions and other formatting ( --no-rst-clean option)
        [?] Merge the updated docstubs with the current stubs where some are manually updated
        [ ] add a module docstring for the machine.xxxx modules that mostly document classes. ( current logic drops those)
            these can also be manually added to the stubs
        [ ] add new functionality to add values from the mcu-stubs into the doc-stubs 


    [ ] add logic to mark the modules as originating from micropython-lib ( Need more than the module name, likely the complete path ) 
    [ ] add port designations (need source for that)

 [x] add logic to add the micropython-lib modules 
 [x] Check for missing sections / functions / classes in the generated documentation.
     There is a test `test_library_page` that tries to compare the generated docs with the source code, but it is not completely reliable 
     as it is hard for to distinguish between intentional changes, and omissions and errors.
     the test uses a diff of the source code and the generated docs, 
        - ignores moved lines (reordering of methods is common)
        - ignores functions/methods with additional type information pr return or parameters 
        - ignores Class.method / method notation differences
        - ignores a number of common headings that are not always present in generated docs new style

        The remainder of differences need to be manually checked and corrected.
        these are written to a file `checks/check-library-<module>.md` for each module that has differences


Manual stubs 
-----------
There are a few (stdlib)  Modules that likely need to be handcrafted or require additional care.
    - asyncio, the current stubs are based off the .py version , which is now outdated
    - stdlib modules 
        - collections
        - builtins    
        - collections
        - os / sys / gc 

    


## You build it, you break it

- clone 
- create & activate a virtual environment
- `pip install U -r docs/requirements.txt`
- `cd docs`
- `.\make html`  or `make html`
- `pytest` 

Vscode config is setup for Windows development with Ctrl-Shift-B to build the docs
this includes additional cleanup of folders that `make clean` leaves untouched.


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
    :no-index:
    :members:
    :undoc-members:
    :private-members: 
    :special-members:



    :exclude-members: __init__, __weakref__

.. restore_section::


   .. autoapiclass:: btree
        :noindex:
        :members:
        :undoc-members:
        :private-members: 
        :special-members:
        :show-inheritance:

### avoid adding () after `autoapiclass`,  `autoapifunction` and `autoapimethod` directives.

As that will override the signatures that are generated by autoAPI, and the documentation may not be generated correctly.

The check / correct you can use these regexes in you IDE of choise:

```regex
# Find
.. autoapi(\w+):: (.*)(\(.*\))
# replace with
.. autoapi$1:: $2
```

## Debugging rst in docstrings

it can be hard to `debug' the rst in docstrings, as the errors are not always clear, and there have been a lot of different writers that have added to the documentation over the years,
each with their own style , and sometimes incorrect syntax has apparently been copied over and over again

 I have been using the following approach to debug the rst in docstrings:
 1. find the error in the ( generated) .rst file
 2. find the corresponding docstring in the .py or .pyi file, as that is where the correction needs to be made
 3. copy the docstring 
 4. open a browser and go to https://snippets.documatt.com/
 5. paste the docstring in the `write` pane
 6. click the `preview` button

### wrong syntax for quotes

, such as back-tick .... single quote :  
"""
`sample'
rather than 
`sample`
"""
### check example codeblocks for \n or \n 

all special characters should have an extra `\` so `\n` should be `\\n`


### move class __init__ methods to the first method in the class
stubber places the `__init__` method at the end of the class, but it is more common to see it at the top of the class
Apparently autoAPI assumes __init__ is always the first method in the class, so it is better to move it there
if not the class will not be documented properly




# to we keep all the module pages generated by autoapi ?
Currently the library pages mix regular documentation and module/class documentation in the same page 
This is not ideal, as the module/class documentation is not easily accessible

There are multiple options to fix this:
1) keep the Why and How parts of the page and add links to the autoapi module or class pages in the autodocs
2) remove the autodoc pages and only use the autoapi pages


### index / no-index
As now its more likely that the autoapi pages will be the main source of information, it is important to be able to control which modules and classes are included in the index page and search.
With the `:noindex:` (or `:no-index:`? ) option, the module or class will not be included in the index page. This is useful for modules that are not part of the standard library, but are included in the documentation for reference purposes.

I hove ot (yet) found a way to control the no-index attribute of the pages generated by autoapi, 
therefore I have been marking the modules/classes and functions in teh `library/foobar.rts` files with the `.. no-index::` directive to prevent them from being included in the index page, and generating warnings 



## Micropython-lib 

Some of the modules have docstrings and some level of type annotation, but most are quite poorly documented, possibly to try to save space on the microcontroller.


Option 1) Direct processing 
    - copy module from micropython-lib to a temporary location
    - generate documentation using autoAPI 
    - add logic to mark the modules as originating fro micropython-lib 

Option 2) dynamically create type-stubs 
    - use stubber to generate type stubs for all micropython-lib modules (using mypy-stubgen and some post processing to clean up its mistakes) 
      this is already done for all modules that are frozen in the micropython firmware.
      The benefit is better type annotation
    - add the type stubs to a temporary location
    - generate documentation using autoAPI 
    - add logic to mark the modules as originating fro micropython-lib 

Option3) add type-stubs to micropython-lib
    - Generate once - then maintain manually
    - add logic to mark the modules as originating from micropython-lib 
    - generate documentation using autoAPI
    Pro: best option for rich documentation without overhead on the modules 
    con: manual maintenance of the type-stubs needed 


Note: 
  Both docstrings, type annotations and comments are stripped during compilation , so for cross compiled modules there is no real difference AFAIK.

### know limitations of the current PoC
In the  PoC the copying of the modules from micropython-lib is a bit simplistic, and does not correctly copy all the files needed for all modules to be used to generate documentation.
Current problematic modules are:
 - https://github.com/micropython/micropython-lib/tree/master/micropython/bluetooth/aioble/aioble      ( complex module with multiple files)
 - https://github.com/micropython/micropython-lib/tree/master/micropython/lora/lora/lora
 - https://github.com/micropython/micropython-lib/tree/master/micropython/mip-cmdline
 - https://github.com/micropython/micropython-lib/tree/master/micropython/mip/mip
 - https://github.com/micropython/micropython-lib/tree/master/micropython/senml/senml
 - https://github.com/micropython/micropython-lib/blob/master/micropython/umqtt.robust/umqtt/robust.py
 - https://github.com/micropython/micropython-lib/blob/master/micropython/umqtt.simple/umqtt/simple.py
 - https://github.com/micropython/micropython-lib/blob/master/micropython/urllib.urequest/urllib/urequest.py
 - https://github.com/micropython/micropython-lib/blob/master/micropython/usb .... (multiple files)

 - https://github.com/micropython/micropython-lib/tree/master/python-ecosys/aiohttp/aiohttp
 - https://github.com/micropython/micropython-lib/tree/master/python-ecosys/cbor2/cbor2
 - https://github.com/micropython/micropython-lib/tree/master/python-ecosys/pyjwt
 - https://github.com/micropython/micropython-lib/tree/master/python-ecosys/requests/requests

 - https://github.com/micropython/micropython-lib/blob/master/python-stdlib/collections-defaultdict/collections/defaultdict.py
 - https://github.com/micropython/micropython-lib/blob/master/python-stdlib/collections/collections/__init__.py
 - https://github.com/micropython/micropython-lib/blob/master/python-stdlib/curses.ascii/curses/ascii.py

The solution is probably using a piece of exiting code in `tools\manifestfile.py` to read the `manifest.py` and use that to copy the files / folders needed for the module to work.
for some modules such as collections that may not be sufficient and a manual stub may be needed to make the module work in the docs.


### rst formatting errors

There are a bunch of files that have rst formatting errors,  which causes the documentation to fail to generate a lot of warnings and cause incorrect formatting.
TODO: Create PR with the fixes for these files.








