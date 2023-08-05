.. _api-blockfile:

:class:`BlockFile` --- Block File Bases class
---------------------------------------------

**This is the base class used for (large) files consisting of blocks within the** *pylam* **framework.**

As a *Block file* we consider a file which can be contains of one ore more repeating logical sections, like ``bfile.txt``::

    Example for a block file.

    [data]
    00 01 02 03 04
    10 11 12 13 14
    20 21 22 23 24
    [end data]

    Lorem ipsum dolor sit amet, consetetur sadipscing elitr,
    sed diam nonumy eirmod tempor invidunt ut labore et dolore.

    [data]
    20 21 22 23 24
    30 31 32 33 34
    40 41 42 43 44
    50 51 52 53 54
    [end data]

    Et vero eos et accusam et justo duo dolores et ea rebum.

    [data]
    40 41 42 43 44
    50 51 52 53 54
    60 61 62 63 64
    70 71 72 73 74
    80 81 82 83 84
    [end data]

    *eof*

The :class:`.base.BlockFile` class is derived from :class:`.base.IndexedFile`.
Therefore we can easily make use of the :meth:`.base.IndexedFile._parseLine` method to implement a parsing.
That way a *Block file* object can be populated with :class:`.base.Block` objects by using :meth:`.base.BlockFile.addBlock`.

For the above shown example ``bfile.txt``, a simple implementation could look like:

.. code-block:: py

    >>> import pylam.base
    >>>
    >>> class MyBlockFile(pylam.base.BlockFile):
    >>>
    >>>     def __init__(self, filename):
    >>>         self.tmp = None
    >>>         super(MyBlockFile, self).__init__(filename)
    >>>
    >>>     def _parseLine(self, line, no):
    >>>         if "[data]" in line:
    >>>            self.tmp = no + 1
    >>>         if "[end data]" in line:
    >>>           self.addBlock(fline=self.tmp,
    >>>                         lline=no-1,
    >>>                         header_line=str('Block {0:d}'.format(len(self))))
    >>>
    >>>
    >>> blockfile = MyBlockFile('bfile.txt')
    >>> print len(blockfile)   # returns the number of blocks
    3

.. note:: :func:`len` returns the **number of blocks**, not number of lines!

One can iterate over the blocks within a *block file* object, and has itemized access:

.. code-block:: py

    >>> for block in blockfile:
    >>>     print block.header_line
    Block 0
    Block 1
    Block 2
    >>> print blockfile[0].data
    00 01 02 03 04
    10 11 12 13 14
    20 21 22 23 24


----------------------------------


.. autoclass:: pylam.base.BlockFile
    :members:
    :private-members:
    :special-members:
    :exclude-members: __dict__, __module__, __weakref__, __iter__, __init__



:class:`Block` --- Block Bases class
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**This is the base class for a block (a logical subunit) within a file.**





.. autoclass:: pylam.base.Block
    :members:
    :private-members:
    :special-members:
    :exclude-members: __dict__, __module__, __weakref__, __iter__, __init__