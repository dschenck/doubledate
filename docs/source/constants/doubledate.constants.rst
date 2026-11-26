Constants
=====================================

doubledate exposes a few constants for frequencies and weekdays, which can be used
instead of the equivalent strings and integers.

Frequencies
-------------------------
Accepted by functions such as :code:`floor`, :code:`ceil` and :code:`dayof`, and by
:code:`Calendar.groupby` / :code:`Calendar.resample`.

=================  ============  ========================
Constant           Value         Frequency
=================  ============  ========================
:code:`dtwo.Y`     :code:`"Y"`   year
:code:`dtwo.H`     :code:`"H"`   semester (half year)
:code:`dtwo.T`     :code:`"T"`   trimester (four months)
:code:`dtwo.Q`     :code:`"Q"`   quarter
:code:`dtwo.M`     :code:`"M"`   month
:code:`dtwo.W`     :code:`"W"`   week
=================  ============  ========================

Weekdays
-------------------------
Weekdays follow Python's :code:`datetime.date.weekday` convention: Monday is 0 and
Sunday is 6.

=================  ==========
Constant           Value
=================  ==========
:code:`dtwo.MON`   :code:`0`
:code:`dtwo.TUE`   :code:`1`
:code:`dtwo.WED`   :code:`2`
:code:`dtwo.THU`   :code:`3`
:code:`dtwo.FRI`   :code:`4`
:code:`dtwo.SAT`   :code:`5`
:code:`dtwo.SUN`   :code:`6`
=================  ==========

:code:`dtwo.WEEKDAYS` maps the weekday names to these integers:

.. code-block::

    >>> import doubledate as dtwo

    >>> dtwo.WEEKDAYS
    {'MON': 0, 'TUE': 1, 'WED': 2, 'THU': 3, 'FRI': 4, 'SAT': 5, 'SUN': 6}

    >>> dtwo.last(dtwo.FRI, asof=dtwo.date(2020, 1, 15))
    datetime.date(2020, 1, 10)

Date limits
-------------------------
:code:`dtwo.MINYEAR` (1) and :code:`dtwo.MAXYEAR` (9999) are aliases for
:code:`datetime.MINYEAR` and :code:`datetime.MAXYEAR`.
