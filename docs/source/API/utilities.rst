Utilities
=====================================
doubledate comes with a dozen utility functions allowing to easily compute the start and end of various frequencies given a date.
::

    >>> import datetime
    >>> import doubledate as dtwo

    >>> dtwo.utils.eom(datetime.date(2020, 2, 23))
    datetime.date(2020, 2, 29) #end of month

    >>> dtwo.utils.eoq(datetime.date(2020, 2, 23), 1)
    datetime.date(2020, 6, 30) #end of next quarter

    >>> dtwo.utils.offset(datetime.date(2020, 3, 5), weekdays=3))
    datetime.date(2020, 3, 9) #3 weekdays after Thursday 5 March is Monday 9 March

The full list of utility functions can be found below. 

.. automodule:: doubledate.utils
    :members: quarter, trimester, semester, eow, sow, eom, som, eoq, soq, eos, sos, soy, eoy, ceil, floor, offset, isleap
