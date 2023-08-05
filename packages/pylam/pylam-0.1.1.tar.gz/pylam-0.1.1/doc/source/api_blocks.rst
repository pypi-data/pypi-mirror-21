.. _api-blocks:

Block classes
-------------

.. _api-datablock:

DataBlock
^^^^^^^^^

.. autoclass:: pylam.DataBlock
    :members:
    :private-members:
    :special-members:
    :exclude-members: __dict__, __module__, __weakref__, __iter__, __init__


.. _api-thermoblock:

ThermoBlock
^^^^^^^^^^^

This class represents a `thermodynamic info`_ block which is section of the `log file`_ (log.lammps).

.. autoclass:: pylam.ThermoBlock
    :members:
    :private-members:
    :special-members:
    :exclude-members: __dict__, __module__, __weakref__, __iter__, __init__, _get_timing, _get_timing_new, _get_timing_old


FixBlock
^^^^^^^^
.. autoclass:: pylam.FixBlock
    :members:
    :private-members:
    :special-members:
    :exclude-members: __dict__, __module__, __weakref__, __iter__, __init__


.. _log file: http://lammps.sandia.gov/doc/log.html
.. _thermodynamic info: http://lammps.sandia.gov/doc/thermo.html