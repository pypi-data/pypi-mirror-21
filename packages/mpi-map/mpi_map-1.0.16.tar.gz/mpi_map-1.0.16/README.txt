==============
MPI map
==============

`Documentation <http://mpi-map.readthedocs.io>`_

This package uses `mpi4py <https://pypi.python.org/pypi/mpi4py/>`_ and `dill <http://trac.mystic.cacr.caltech.edu/project/pathos/wiki/dill.html>`_ to spawn processes and execute them.

Installation
============

You need to have an MPI back-end installed on your machine and add the right path on the ``$LD_LIBRARY_PATH``, so that `mpi4py <https://pypi.python.org/pypi/mpi4py/>`_ can link to it. You should install `mpi4py <https://pypi.python.org/pypi/mpi4py/>`_ manually by

   $ pip install mpi4py

When everything is set, you can install the ``mpi_map`` using:

    $ pip install mpi_map

ChangeLog
=========

v1.0.1
------

* map methods of classes

v1.0.3
------

* added export of cwd in order to allow import of local modules