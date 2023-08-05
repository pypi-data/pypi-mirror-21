.. image::  https://badge.fury.io/py/pydon.svg
   :target: https://badge.fury.io/py/pydon
   :alt:    Latest Version

.. image::  https://travis-ci.org/dusktreader/pydon.svg?branch=master
   :target: https://travis-ci.org/dusktreader/pydon
   :alt:    Build Status

*******
 pydon
*******

-----------------------------------------------------
Python data object notation. Like json, but pythonic
-----------------------------------------------------

This package provides some basic tools for reading and writing python data
objects to and from strings or files. A .pydon file or string is simply a
string representation of python data. The pydon package is meant to provide
similar functionality to json. Any pydon strings should be valid python
expressions and must be parsable by the python AST's literal_eval method. This
means that pydon strings can safely contain data expressed as pytyhon literals.

Requirements
============

 - Python 3

Installing
==========
Install using pip::

$ pip install pydon

Using
=====
This package should be usable in a very similar manner to the json package:

.. code-block:: python

   import pydon
   my_data = pydon.load_string("{'a': 1, 'b': '2', 'c': [4, 5, 6]}")

The `load_file` method may be used to load data from a file directly:

.. code-block:: python

   import pydon
   my_data = pydon.load_file('some_file.pydon')

The `dump_string` method may be used to dump a pydon serializable data object
to a string. The method can accept `pprint format arguments
<https://docs.python.org/3/library/pprint.html>`_:

.. code-block:: python

   import pydon
   pydon.dump_string({'a': 1, 'b': '2', 'c': [4, 5, 6]}, width=1, indent=2)

This should result in the following output::

  {
    'a': 1,
    'b': '2',
    'c': [4, 5, 6],
  }

The `dump_file` method may be used to dump a pydon serializable data object
directly to a named file. The method can accept `pprint format arguments
<https://docs.python.org/3/library/pprint.html>`_ as well:

.. code-block:: python

   import pydon
   pydon.dump_file(
       {'a': 1, 'b': '2', 'c': [4, 5, 6]},
       'some_file.pydon',
       width=1, indent=2,
   )

Note that the `.pydon` extension is only used as a matter of convention. You
may find it more useful to simply use the `.py` extension.
