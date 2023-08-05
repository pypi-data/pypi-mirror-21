.. _api-indexedfile:

:class:`IndexedFile` --- File Base class
----------------------------------------

**This is the base class used for (large) file handling in the** *pylam* **framework.**

It provides a random access to a file based on the line index.
This is realized by scanning the file at initialization and building a table of byte offsets.
Therefore, if one needs access to line(s) at the middle or at the end of a large file,
one did not need to go through all previous lines until one reaches the line(s) of interest.

.. note:: An object must be initiated with an input file, which will be scanned to generate an index initially.
          Hereafter the file will be closed and re-opened for each access!

The core methods are :meth:`.IndexedFile.getLines` and :meth:`.IndexedFile.getLine` to retrieve certain line(s) from a
file as a string, including the newline character.
The python function :func:`len` will return the length of the file as number of lines.

Example input file ``test.txt``::

      _     _       Line index 0
     (_) __| |_  __ Line index 1
     | |/ _` \ \/ / Line index 2
     | | (_| |>  <  Line index 3
     |_|\__,_/_/\_\ Line index 4
       __ _ _       Line index 5
      / _(_) | ___  Line index 6
     | |_| | |/ _ \ Line index 7
     |  _| | |  __/ Line index 8
     |_| |_|_|\___| Line index 9
    *eof*           Line index 10

.. code-block:: py

    >>> import pylam.base
    >>> ifile = pylam.base.IndexedFile('test.txt')
    >>> print len(ifile)  # returns the total number of lines
    11
    >>> lines = ifile.getLines(5, 9)  # get lines as string (incl. new lines!)
    >>> print lines
       __ _ _       Line index 5
      / _(_) | ___  Line index 6
     | |_| | |/ _ \ Line index 7
     |  _| | |  __/ Line index 8
     |_| |_|_|\___| Line index 9
    >>> print type(lines)
    <type 'str'>


One can although iterate over an :class:`IndexedFile` object:

.. code-block:: py

    >>> for line in ifile:
    >>>     print line[0:16]
      _     _
     (_) __| |_  __
     | |/ _` \ \/ /
     | | (_| |>  <
     |_|\__,_/_/\_\
       __ _ _
      / _(_) | ___
     | |_| | |/ _ \
     |  _| | |  __/
     |_| |_|_|\___|
    *eof*

But remember, the file will be re-opened for each access!

The method :meth:`.IndexedFile._indexFile` (which is called in :meth:`__init__`) calls for *each* line :meth:`.IndexedFile._parseLine`.
This method is here a dummy. By replacing this method in a derived class one can easily implement further parsing.



----------------------------------



.. autoclass:: pylam.base.IndexedFile
    :members:
    :private-members:
    :special-members:
    :show-inheritance:
    :exclude-members: __dict__, __module__, __weakref__, __iter__, __init__



