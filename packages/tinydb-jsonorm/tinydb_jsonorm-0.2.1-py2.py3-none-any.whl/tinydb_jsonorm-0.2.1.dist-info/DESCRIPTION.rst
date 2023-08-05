========
Overview
========



A library based on jsonmodels that adds some ORM features and another few conveniences to TinyDB with Json storage and
tinydb-smartcache enabled.

* Free software: BSD license

Installation
============

::

    pip install tinydb-jsonorm

Documentation
=============

https://tinydb-jsonorm.readthedocs.io/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox


Changelog
=========

0.1.0 (2016-05-06)
-----------------------------------------

* First release on PyPI.


