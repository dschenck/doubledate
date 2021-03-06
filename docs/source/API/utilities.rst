Utilities
=====================================

Usage
----------------------------------
doubledate comes with a 20+ utility functions allowing to easily compute the start and end of various frequencies given a date.
::

    >>> import datetime
    >>> import doubledate as dtwo

    >>> dtwo.eom(datetime.date(2020, 2, 23))
    datetime.date(2020, 2, 29) #end of month

    >>> dtwo.eoq(datetime.date(2020, 2, 23), 1)
    datetime.date(2020, 6, 30) #end of next quarter

    >>> dtwo.offset(datetime.date(2020, 3, 5), weekdays=3))
    datetime.date(2020, 3, 9) #3 weekdays after Thursday 5 March is Monday 9 March

    >>> dtwo.dayof(datetime.date(2020,2,29), "Q")
    60

    >>> dtwo.daysto(datetime.date(2020,2,29), "QE")
    31

    >>> dtwo.isleap(datetime.date(2020,4,12))
    True #accepts an integer or a date
    

The full list of utility functions can be found below. 

API
----------------------------------
.. automodule:: doubledate
    :members: quarter, trimester, semester, eow, sow, eom, som, eoq, soq, eot, sot, eos, sos, soy, eoy, ceil, floor, offset, isleap, dayof, daysfrom, daysto, weekdayof
