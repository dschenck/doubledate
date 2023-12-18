doubledate
=====================================
**doubledate** exposes an immutable :code:`Calendar` object representing a sorted-set of dates as well as a suite of 20+ utility functions.

.. include:: fragments/badges.rst

Installation
-------------------------------------
**doubledate** is written in pure Python. Installing doubledate is simple with pip: 
::

    $ pip install doubledate

Quickstart 
-------------------------------------

Using doubledate is also easy: simply wrap a list of dates in a :code:`doubledate.Calendar`
::

    >>> import doubledate as dtwo
    
    >>> dates = [...] # list of dates
    >>> calendar = dtwo.Calendar(dates)
    <doubledate.calendar.Calendar at 0x17...>

More realistically:

::

    >>> import datetime
    >>> import doubledate as dtwo

    # load from database, file...
    >>> holidays = [
    ...     datetime.date(2024,  1,  2),  # New Years Day
    ...     datetime.date(2024,  1, 15),  # Martin Luther King, Jr. Day
    ...     datetime.date(2024,  2, 19),  # Washington's Birthday
    ...     datetime.date(2024,  3, 29),  # Good Friday
    ...     datetime.date(2024,  5, 27),  # Memorial Day
    ...     datetime.date(2024,  6, 19),  # Juneteenth National Independence Day
    ...     datetime.date(2024,  7,  4),  # Independence Day
    ...     datetime.date(2024,  9,  2),  # Labor day
    ...     datetime.date(2024, 11, 28),  # Thanksgiving Day
    ...     datetime.date(2024, 12, 25)   # Christmas day
    ... ]

    # create a Calendar
    # here, every weekday (Mon-Fri), excluding holidys
    >>> calendar = dtwo.Calendar.create(
    ...     "B", 
    ...     starting=dtwo.date(2024, 1, 1), 
    ...     ending=dtwo.date(2024, 12, 31)
    ... ).difference(holidays)

    # first business day each month
    >>> calendar.resample("M").first()
    <doubledate.calendar.Calendar at 0x17...>

    # last business day each week ending on Wednesday 
    >>> calendar.resample("W-WED").nth(-1)
    <doubledate.calendar.Calendar at 0x17...>

    # first or last business day dependending on month
    >>> calendar.resample("M").apply(
    ...    lambda month: month[0] if month.start.month < 7 else month[-1]
    ... ).combine()
    <doubledate.calendar.Calendar at 0x17...>

    # most recent date as of given date
    >>> calendar.asof(datetime.date(2024, 9, 4), side="left")
    datetime.date(2024, 8, 30)

The library also comes with an additional suite of utility functions
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
   source/utils/doubledate.utils
   source/Calendar/doubledate.Calendar
   source/diem/doubledate.diem
   source/BD/doubledate.BD
   source/Collection/doubledate.Collection
   source/changelog


Documentation
-------------------------------------
Complete documentation for doubledate is available at https://doubledate.readthedocs.io
