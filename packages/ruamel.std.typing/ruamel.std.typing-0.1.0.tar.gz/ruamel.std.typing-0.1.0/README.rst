
ruamel.std.typing
=================


`package ruamel.std.pathlib <https://bitbucket.org/ruamel/std.typing>`_ is a drop-in
replacement to extend the Python standard `typing`` module.

- adds pip install dependency for 2.7/3.3/3.4
- adds Text for 3.5.0 and 3.5.1

This package alleviates the need to do::

   import sys
   if sys.version_info >= (3, 5, 2):
       from typing import Dict, List, Any, Union, Text   # NOQA

instead you can just do::

   from ruamel.std.typing import Dict, List, Any, Union, Text
