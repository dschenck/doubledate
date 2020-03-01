Calendar
=====================================

Usage
----------------------------------
The calendar class allows to easily operate on a list of dates. It is built on top of a sortedset for efficiency. 
::

    >>> import datetime
    >>> import doubledate as dtwo

    #you can load up your own dates from a backend, API, file...
    >>> calendar = dtwo.Calendar([datetime.date(2019,1,1) + datetime.timedelta(i) for i in range(365)])

    #isolate all the week-end days
    >>> weekends = calendar.weekends()

    #or just the week days
    >>> weekdays = calendar.weekdays()

    #first and last date
    >>> weekdays.first(), weekdays.last()

    #or index
    >>> weekdays[0], weekdays[-1]

    #slice the calendar
    #like normal lists, the Calendar is 0-based, such that slice(10:20) returns the 11th to 20th dates
    >>> weekdays[10:20]

    #or with a date-like object
    #this will be inclusive of the bounds, if they are in the calendar
    >>> semester = weekdays[datetime.date(2019,7,1):datetime.date(2019,12,31)]

    #10th weekday each month
    >>> b10 = weekdays.groupby("month").apply(lambda cal: cal[10]).combine()

    #5th to 10th weekday each month
    >>> b5to10 = weekdays.groupby("month").apply(lambda cal: cal[5:10])

    #lets retrieve holidays from somewhere (API, file...)
    >>> holidays = [
            datetime.date(2019, 1, 1), datetime.date(2019, 1, 21), 
            datetime.date(2019, 2, 18), datetime.date(2019, 5, 27),
            datetime.date(2019, 7, 4), datetime.date(2019, 9, 2), 
            datetime.date(2019, 10, 14), datetime.date(2019, 11, 11), 
            datetime.date(2019, 11, 28), datetime.date(2019, 12, 25)
        ]

    #because the calendar class is a sorted set, you have set methods like union, intersection and difference
    #business days
    >>> workdays = weekdays.difference(holidays)

    #... alternatively
    >>> workdays = holidays.inverse(datetime.date(2019, 1, 1), datetime.date(2019, 12, 31)).weekdays()

    #non-weekend holidays
    >>> offdays = weekdays.intersection(holidays)

    #iterate over the days
    >>> for date in offdays: 
            pass

API
----------------------------------
.. autoclass:: doubledate.Calendar
    :members: