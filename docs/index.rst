doubledate: another datetime library
=====================================
**doubledate** is yet another datetime library, because one is never enough. It comes with a few utility functions as well as a `Calendar` object designed to interface custom calendars.

>>> import doubledate as dtwo

Quickstart
-------------------------------------
Installing doubledate is simple with pip: 
::

    $ pip install doubledate

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
    

Documentation
-------------------------------------
Complete documentation for doubledate is available at https://doubledate.readthedocs.io


.. toctree::
   :maxdepth: 2
   :caption: Contents

   source/installation
   source/API/index
   source/changelog