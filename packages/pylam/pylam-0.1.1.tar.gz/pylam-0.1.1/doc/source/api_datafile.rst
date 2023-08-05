.. _api-datafile:

Data File classes
-----------------

SimpleDataFile
^^^^^^^^^^^^^^

Class to handle simple data files, aka `cvs`_ files.

.. autoclass:: pylam.SimpleDataFile
    :members:
    :private-members:
    :special-members:
    :exclude-members: __dict__, __module__, __weakref__, __iter__, __init__, _scan_file


FixBlockFile
^^^^^^^^^^^^

.. autoclass:: pylam.FixBlockFile
    :members:
    :private-members:
    :special-members:
    :exclude-members: __dict__, __module__, __weakref__, __iter__, __init__, _scan_file


LogFile
^^^^^^^
This class provides a access to the `log file`_ (log.lammps).
The `thermodynamic info`_ block(s) are made accessable as :ref:`ThermoBlock <api-thermoblock>` objects.

.. autoclass:: pylam.LogFile
    :members:
    :private-members:
    :special-members:
    :exclude-members: __dict__, __module__, __weakref__, __iter__, __init__, _scan_file




.. _cvs: https://en.wikipedia.org/wiki/Comma-separated_values
.. _log file: http://lammps.sandia.gov/doc/log.html
.. _thermodynamic info: http://lammps.sandia.gov/doc/thermo.html
