doubledate: another datetime library
=====================================
**doubledate**, yet another datetime library, exposes a set of 20+ utility functions as well as an immutable :code:`Calendar` object representing a sorted-list of dates.

.. image:: https://badge.fury.io/py/doubledate.svg
   :target: https://badge.fury.io/py/doubledate

.. image:: https://readthedocs.org/projects/doubledate/badge/?version=latest
   :target: https://doubledate.readthedocs.io/en/latest/?badge=latest

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black

Installation
-------------------------------------
**doubledate** is written in pure Python. Installing doubledate is simple with pip: 
::

    $ pip install doubledate

Quickstart 
-------------------------------------

Using doubledate is also easy
::

    >>> import datetime
    >>> import doubledate as dtwo

    >>> trade = datetime.date(2020, 6, 17)

    >>> dtwo.quarter(trade), dtwo.quarter(trade, base=0)
    (2, 1)

    >>> dtwo.eom(trade) #end-of-month
    datetime.date(2020, 6, 30)

    >>> dtwo.offset(trade, weekdays=3)
    datetime.date(2020, 6, 22) #Wednesday + 3 weekdays is Monday

    >>> dtwo.offset(datetime.datetime(2020, 3, 31), months=-1)
    datetime.datetime(2020, 2, 29) #2020 is a leap year

    >>> dtwo.offset(datetime.datetime(2020, 3, 31), months=1, handle=lambda eom, gap: 1)
    datetime.datetime(2020, 5, 1) #handle function returned 1... i.e. eom + 1 day


.. toctree::
   :maxdepth: 2
   :caption: Contents

   source/installation
   source/API/index
   source/changelog


Documentation
-------------------------------------
Complete documentation for doubledate is available at https://doubledate.readthedocs.io
