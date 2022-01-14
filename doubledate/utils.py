import calendar
import datetime
import dateutil.parser

import doubledate.constants as constants


def today():
    """
    Returns today's date as a :code:`datetime.date` object

    Returns
    -------
    datetime.date
        today's date

    See also
    --------
    tomorrow : compute tomorrow's date
    yesterday : compute yesterday's date
    now : compute current datetime
    """
    return datetime.date.today()


def tomorrow():
    """
    Returns tomorrow's date as a :code:`datetime.date` object

    Returns
    -------
    datetime.date
        tomorrow's date

    See also
    --------
    today, yesterday, now
    """
    return datetime.date.today() + datetime.timedelta(days=1)


def yesterday():
    """
    Returns yesterday's date as a :code:`datetime.date` object

    Returns
    -------
    datetime.date
        yesterday's date

    See also
    --------
    today, tomorrow, now
    """
    return datetime.date.today() - datetime.timedelta(days=-1)


def now():
    """
    Returns :code:`datetime.datetime.now()`

    Returns
    -------
    datetime.datetime
        current datetime

    See also
    --------
    today, tomorrow, yesterday
    """
    return datetime.datetime.now()


def semester(date, *, base=1):
    """
    Returns the semester of the given date.

    The first semester runs from 1 January to 30 June; the second
    from 1 July to 31 December.

    Parameters
    ----------
    date : datetime.date
        the date from which to determine the semester
    base : int, optional
        the index of the first semester (default is 1)

    Returns
    -------
    int
        semester's index

    Examples
    ------------
    >>> semester(datetime.date(2020, 1, 10))
    1

    >>> semester(datetime.date(2020, 1, 10), base=0)
    0

    See also
    --------
    trimester, quarter
    """
    return (date.month - 1) // 6 + base


def trimester(date, *, base=1):
    """
    Returns the trimester of the given date

    Trimesters run from 1 January to 30 April, 1 May to 31 August 
    and 1 September to 31 December.

    Parameters
    ----------
    date : datetime.date
        the date from which to determine the trimester
    base : int, optional
        the index of the first trimester (default is 1)

    Returns
    -------
    int
        trimester's index

    Examples
    --------
    >>> trimester(datetime.date(2020, 5, 10))
    2

    >>> trimester(datetime.date(2020, 5, 10), base=0)
    1

    >>> trimester(datetime.date(2020, 9, 10))
    3

    See also
    --------
    semester, quarter
    """
    return (date.month - 1) // 4 + base


def quarter(date, *, base=1):
    """
    Returns the quarter of the given date

    Quarters run from 1 January to 31 March, 1 April to 30 June, 
    1 July to 30 September and 1 October to 31 December.

    Parameters
    ----------
    date : datetime.date
        the date from which to determine the quarter
    base : int, optional
        the index of the first trimester (default is 1)

    Returns
    -------
    int
        quarter's index

    Examples
    ------------
    >>> quarter(datetime.date(2020, 1, 10))
    1

    >>> quarter(datetime.date(2020, 1, 10), base=0)
    0

    See also
    --------
    semester, trimester
    """
    return (date.month - 1) // 3 + base


def sow(date: datetime.date, offset: int = 0, weekday: str = "MON") -> datetime.date:
    """
    Returns the start of the week, i.e. the first date on or before the given date 
    whose weekday is equal to the the weekday argument, and 
    offset by a given number of weeks. 
    
    Weekday must be one of :code:`'MON'`, :code:`'TUE'`, :code:`'WED'`, :code:`'THU'`, 
    :code:`'FRI'`, :code:`'SAT'` or :code:`'SUN'`.

    Parameters
    ----------
    date : datetime.date
        the date from which to determine the start of the week
    offset : int, optional
        the number of weeks from which to offset the most recent start 
        of the week (default is 0)
    weekday : str, optional
        the weekday which defines the start of the week (default is :code:`"MON"`)

    Returns
    -------
    :code:`datetime.date`
        The start of the week

    Examples
    --------
    >>> today = datetime.date(2020, 1, 15) #Wednesday
    >>> sow(today) 
    datetime.date(2020, 1, 13) #last Monday

    >>> sow(today, 1)
    datetime.date(2020, 1, 20) #following Monday

    >>> sow(today, weekday="WED") 
    datetime.date(2020, 1, 15) #today

    >>> sow(today, weekday="THU")
    datetime.date(2020, 1, 9) #last Thursday

    See also
    --------
    eow : compute end of week
    som : compute start of month
    soq : compute start of quarter
    sot : compute start of trimester
    soy : compute start of year
    """
    if isinstance(weekday, str):
        weekday = constants.WEEKDAYS[weekday]
    return date + datetime.timedelta(offset * 7 - ((date.weekday() - weekday) % 7))


def next(weekday: str, *, asof=None) -> datetime.date:
    """
    Returns the first weekday strictly after the :code:`asof` date (or today) 
    for which the weekday is equal to the passed :code:`weekday` argument.

    Weekday must be one of :code:`'MON'`, :code:`'TUE'`, :code:`'WED'`, :code:`'THU'`, 
    :code:`'FRI'`, :code:`'SAT'` or :code:`'SUN'`.

    Parameters
    ----------
    weekday : str
        the target weekday
    asof : datetime.date, optional
        the date from which to determine the next date (default is :code:`today`)

    Returns
    -------
    :code:`datetime.date`
        The first weekday strictly after the asof date

    Examples
    --------
    >>> next("MON") #assume today is Wed 15 Jan 2020
    datetime.date(2020, 1, 20)

    >>> next("WED")
    datetime.date(2020,1,22)

    >>> next("MON", asof=datetime.date(2020,1,15))
    datetime.date(2020, 1, 20)

    See also
    --------
    sow : compute start of week
    last : compute last weekday (e.g. Monday)
    """
    return sow(asof or today(), offset=1, weekday=weekday)


def eow(date: datetime.date, offset: int = 0, weekday: str = "SUN") -> datetime.date:
    """
    Returns the end of the week, i.e. the first date on or after the given date
    whose weekday is equal to the the :code:`weekday` argument, and 
    offset by a given number of weeks. 
    
    Weekday must be one of :code:`'MON'`, :code:`'TUE'`, :code:`'WED'`, :code:`'THU'`, 
    :code:`'FRI'`, :code:`'SAT'` or :code:`'SUN'`.

    Parameters
    ----------
    date : datetime.date
        the date from which to determine the end of the week
    offset : int, optional
        the number of weeks from which to offset the most recent end 
        of the week (default is 0)
    weekday : str, optional
        the weekday which defines the end of the week (default is :code:`"SUN"`)

    Returns
    -------
    :code:`datetime.date`
        The end of the week


    Examples
    --------
    >>> today = datetime.date(2020, 1, 15) #Wednesday
    >>> eow(today) 
    datetime.date(2020, 1, 20) #Sunday (by default)

    >>> eow(today, 1)
    datetime.date(2020, 1, 27) #following Sunday

    >>> eow(today, weekday="THU")
    datetime.date(2020, 1, 16) #first Thursday on or after today

    >>> eow(today, weekday="THU", offset=-1)
    datetime.date(2020, 1, 8) #most recent Thursday strictly before today
    """
    if isinstance(weekday, str):
        weekday = constants.WEEKDAYS[weekday]
    return date + datetime.timedelta((weekday - date.weekday()) % 7 + offset * 7)


def last(weekday: str, *, asof=None) -> datetime.date:
    """
    Returns the most recent date strictly before today (or the :code:`asof` date) 
    for which the weekday is equal to the passed :code:`weekday` argument

    Parameters
    ----------
    weekday : str
        the target weekday
    asof : datetime.date, optional
        the date from which to determine the last date (default is :code:`today`)

    Returns
    -------
    :code:`datetime.date`
        The first weekday strictly before the asof date

    Example
    -------
    >>> last("MON") #assume today is Wed 15 Jan 2020
    datetime.date(2020, 1, 13)

    >>> last("SUN")
    datetime.date(2020, 1, 12)

    >>> last("WED", asof=datetime.date(2020, 1, 15))
    datetime.date(2020, 1, 8)

    """
    if asof is None:
        asof = today()

    if constants.WEEKDAYS[weekday] == asof.weekday():
        return asof - datetime.timedelta(days=7)

    return sow(asof, weekday=weekday)


def som(date: datetime.date, offset: int = 0) -> datetime.date:
    """
    Returns the start of the month for the given :code:`date`, then optionally 
    offsets it by :code:`offset` months.

    Parameters
    ----------
    date : datetime.date
        The date for which to compute the start of the month
    offset : int, optional  
        The number of months from which to offset the start of 
        the month

    Returns
    -------
    :code:`datetime.date`
        The start of the month

    Example
    ------------
    >>> today = datetime.date(2020, 1, 15)
    >>> som(today)
    datetime.date(2020, 1, 1) #start of the current month

    >>> som(today, 1):
    datetime.date(2020, 2, 1) #first of February

    >>> som(today, -1):
    datetime.date(2019, 12, 1) #start of the previous month

    See also
    --------
    eom : compute the end of the month
    """
    return date.replace(
        year=(date.year + (date.month + offset - 1) // 12),
        month=((date.month - 1 + 12 * date.year + offset) % 12 + 1),
        day=1,
    )


def eom(date: datetime.date, offset: int = 0):
    """
    Returns the last date of month for the given date, then optionally 
    offsets it by :code:`offset` months.

    Parameters
    ----------
    date : datetime.date
        The date for which to compute the end of the month
    offset : int, optional  
        The number of months from which to offset the end of 
        the month

    Returns
    -------
    :code:`datetime.date`
        The end of the month

    Note
    ----
    This function emulates Excel's EOM function

    Examples
    ------------
    >>> today = datetime.date(2020, 1, 15)
    >>> eom(today) 
    datetime.date(2020, 1, 31)

    >>> eom(today, 1)
    datetime.date(2020, 2, 29) #2020 is a leap year

    >>> eom(today, -1)
    datetime.date(2019, 12, 31) #end of previous month

    See also
    --------
    som : compute the start of the month
    """
    if offset == 0:
        return date.replace(
            day=calendar.monthrange(year=date.year, month=date.month)[1]
        )
    return eom(som(date, offset))


def soq(date: datetime.date, offset: int = 0) -> datetime.date:
    """
    Returns the first date of the quarter, i.e. one of 
    1 January, 1 April, 1 July or 1 October, then optionally 
    offsets it by :code:`offset` quarters

    Parameters
    ----------
    date : datetime.date
        the date from which to compute the start of the quarter
    offset : int, optional
        an offset from the start of the quarter of the date

    Returns
    -------
    datetime.date
        The start of the quarter

    Examples
    --------
    >>> today = datetime.date(2020, 1, 15)
    >>> soq(today):
    datetime.date(2020,1,1)

    >>> soq(today, 1)
    datetime.date(2020,4,1)
    """
    return (eoq(date, offset) - datetime.timedelta(2 * 31 + 1)).replace(day=1)


def eoq(date: datetime.date, offset: int = 0) -> datetime.date:
    """
    Returns the end of the quarter, i.e. one of
    31 March, 30 June, 30 September or 31 December, then 
    optionally offsets it by :code:`offset` quarters

    Parameters
    ----------
    date : datetime.date
        the date from which to compute the end of the quarter
    offset : int, optional
        an offset from the end of the quarter of the date

    Returns
    -------
    datetime.date
        The end of the quarter

    Examples
    --------
    >>> today = datetime.date(2020, 1, 15)
    >>> eoq(today):
    datetime.date(2020,3,31)

    >>> soq(today, 1)
    datetime.date(2020,6,30)
    """
    return eom(
        date.replace(
            year=((date.month - 1) + date.year * 12 + 3 * offset) // 12,
            month=3 * (((date.month - 1) // 3 + offset) % 4 + 1),
            day=1,
        )
    )


def eot(date: datetime.date, offset: int = 0) -> datetime.date:
    """
    Returns the end of the calendar trimester, i.e. one of 
    30 April, 31 August or 31 December, then optionally offsets it 
    by :code:`offset` trimesters

    Parameters
    ----------
    date : datetime.date
        the date from which to compute the end of the trimester
    offset : int, optional
        an offset from the end of the trimester of the date

    Returns
    -------
    datetime.date
        The end of the trimester

    Examples
    --------
    >>> today = datetime.date(2020, 1, 15)
    >>> eot(today):
    datetime.date(2020,4,30)

    >>> eot(today, 1)
    datetime.date(2020,8,31)
    """
    return eom(
        date.replace(
            year=((date.month - 1) + date.year * 12 + 4 * offset) // 12,
            month=4 * (((date.month - 1) // 4 + offset) % 3 + 1),
            day=1,
        )
    )


def sot(date: datetime.date, offset: int = 0) -> datetime.date:
    """
    Returns the first date of the calendar trimester, i.e. one of
    1 January, 1 May or 1 September, then optionally offsets it 
    by :code:`offset` trimesters

    Parameters
    ----------
    date : datetime.date
        the date from which to compute the start of the trimester
    offset : int, optional
        an offset from the start of the trimester of the date

    Returns
    -------
    datetime.date
        The start of the trimester
    """
    return (eot(date, offset) - datetime.timedelta(3 * 31 + 1)).replace(day=1)


def eos(date: datetime.date, offset: int = 0) -> datetime.date:
    """
    Returns the end of the calendar semester, i.e. one of 
    30 June or 31 December, then optionally offsets it 
    by :code:`offset` semesters

    Parameters
    ----------
    date : datetime.date
        the date from which to compute the end of the semester
    offset : int, optional
        an offset from the end of the semester of the date

    Returns
    -------
    datetime.date
        The end of the semester
    """
    return eom(
        date.replace(
            year=((date.month - 1) + date.year * 12 + 6 * offset) // 12,
            month=6 * (((date.month - 1) // 6 + offset) % 2 + 1),
            day=1,
        )
    )


def sos(date: datetime.date, offset: int = 0) -> datetime.date:
    """
    Returns the first date of the calendar semester, i.e. one of
    1 January or 1 July, then optionally offsets it 
    by :code:`offset` semesters

    Parameters
    ----------
    date : datetime.date
        the date from which to compute the start of the semester
    offset : int, optional
        an offset from the start of the semester of the date

    Returns
    -------
    datetime.date
        The start of the semester
    """
    return (eos(date, offset) - datetime.timedelta(5 * 31 + 1)).replace(day=1)


def soy(date: datetime.date, offset: int = 0) -> datetime.date:
    """
    Returns the start of the year, i.e. the 1st January of the current date, 
    then optionally offset by :code:`offset` years.

    Parameters
    ----------
    date : datetime.date
        the date from which to compute the start of the year
    offset : int, optional
        an offset from the start of the year of the date

    Returns
    -------
    datetime.date
        The start of the year
    """
    return type(date)(date.year + offset, 1, 1)


def eoy(date: datetime.date, offset: int = 0) -> datetime.date:
    """
    Returns the end of the year, i.e. the 31 December of the date's year, 
    then optionally offset by :code:`offset` years.

    Parameters
    ----------
    date : datetime.date
        the date from which to compute the end of the year
    offset : int, optional
        an offset from the end of the year of the date

    Returns
    -------
    datetime.date
        The end of the year
    """
    return type(date)(date.year + offset, 12, 31)


def floor(date: datetime.date, frequency: str) -> datetime.date:
    """
    Returns the first date of the frequency (e.g. quarter) 
    for the date passed as first argument. 

    Parameters
    ----------
    date : datetime-like
        the date
    frequency : str
        one of Y, H, Q, M, W or W-MON...W-SUN for, respectively, year, semester, quarter, 
        month, week (or specific weekday)

    Examples
    --------
    >>> floor(datetime.date(2020, 4, 10), "Y")
    datetime.date(2020, 1, 1) #start of year

    >>> floor(datetime.date(2020, 7, 4), "Q")
    datetime.date(2020, 7, 1) #start of quarter
    """
    if frequency == "Y":
        return soy(date)
    if frequency == "H":
        return sos(date)
    if frequency == "T":
        return sot(date)
    if frequency == "Q":
        return soq(date)
    if frequency == "M":
        return som(date)
    if frequency[0] == "W":
        if len(frequency) > 1:
            return sow(date, weekday=frequency[-3:])
        return sow(date)
    raise ValueError(f"Unrecognized frequency {frequency}")


def ceil(date: datetime.date, frequency: str) -> datetime.date:
    """
    Returns the end of the frequency (e.g. quarter) for the date passed as first argument

    Parameters
    ----------
    date : datetime-like
        the date to offset
    frequency : str
        one of Y, H, Q, M, W or W-MON...W-SUN for, respectively, year, semester, quarter, 
        month, week (or specific weekday)

    Examples
    --------
    >>> ceil(datetime.date(2020, 4, 10), "Y")
    datetime.date(2020, 12, 31) #end of year

    >>> ceil(datetime.date(2020, 7, 4), "Q")
    datetime.date(2020, 9, 30) #end of quarter
    """
    if frequency == "Y":
        return eoy(date)
    if frequency == "H":
        return eos(date)
    if frequency == "T":
        return eot(date)
    if frequency == "Q":
        return eoq(date)
    if frequency == "M":
        return eom(date)
    if frequency[0] == "W":
        if len(frequency) > 1:
            return eow(date, weekday=frequency[-3:])
        return eow(date)
    raise ValueError(f"Unrecognized frequency {frequency}")


def isleap(year) -> bool:
    """
    Returns whether the given year (or date's year) is a leap-year.

    Parameters
    ----------
    year : int, datetime.date
        the year, or the date for whose year to determine
        whether it is a leap year or not

    Examples
    --------
    >>> isleap(2020)
    True #2020 is a leap year

    >>> isleap(datetime.date(2020, 4, 10))
    True #also accepts a datetime
    """
    if isinstance(year, datetime.date):
        return isleap(year.year)
    return calendar.isleap(year)


def parse(date, dayfirst=True, yearfirst=True, fuzzy=True):
    """
    parses a string into a datetime.date format
    """
    if isinstance(date, (datetime.date, datetime.datetime)):
        return date
    return dateutil.parser.parse(
        date, dayfirst=dayfirst, yearfirst=yearfirst, fuzzy=fuzzy
    ).date()


def offset(
    date: datetime.date,
    days: int = None,
    weekdays: int = None,
    weeks: int = None,
    months: int = None,
    years: int = None,
    to: str = None,
    handle=0,
):
    """
    Returns the date offset either by a number of frequencies 
    or else to the nearest frequency. Only one of the :code:`days`, :code:`weekdays`,
    :code:`weeks`, :code:`months`, :code:`years` or :code:`to` must be provided.
    
    Arguments
    ------------
    date : datetime-like
        the reference date to offset
    days : int, optional
        to offset the reference date by *n* calendar days
    weekdays : int, optional
        to offset the reference date by *n* weekdays
    weeks : int, optional 
        to offset the reference date by *n* weeks
    months : int, optional 
        to offset the reference date by *n* months. See notes below
        on handling out-of-range dates (e.g. 31 Jan + 1m)
    years : int, optional
        to offset the reference date by *n* months. See notes below 
        if the reference date is 29 February
    to : str, optional
        to offset the reference date to a given period start or period end
    handle : int, function, optional
        optional callback function (or integer) to customize the way out-of-range
        dates are handled (e.g. 31 Jan + 1m). See note below
    
    Raises 
    ------------
    ValueError 
        on invalid arguments
        
    Notes
    ------------
    When adding months or years, there may ambiguity as to what the function should
    return when the "intended" target date is out-of-range. For example, 31 January + 1m 
    should - in a perfect world - yield 31 February... which is out-of-range. 

    By default, the function will handle these out-of-range cases by returning the last
    calendar date in the target month (e.g. 28 February, or 29 February if the year is a
    leap year). 
    ::

        >>> offset(datetime.date(2020, 1, 31), months=1)
        datetime.date(2020, 2, 29)

    You can can customize this behavior using the :code:`handle` argument, which can take 
    either an integer or a callback function: 

    - if given an integer (e.g. 1), the function adds that number of days to the end 
      of target month (e.g. 28 February + 1 day is 1 March)

    ::

        >>> offset(datetime.date(2020, 1, 31), months=1, handle=0)
        datetime.date(2020, 2, 29)

        >>> offset(datetime.date(2020, 1, 31), months=1, handle=1)
        datetime.date(2020, 3, 1)

        >>> offset(datetime.date(2020, 1, 31), months=1, handle=2)
        datetime.date(2020, 3, 2)

        >>> offset(datetime.date(2020, 1, 31), months=1, handle=-1)
        datetime.date(2020, 2, 28)

        >>> offset(datetime.date(2020, 2, 29), years=1, handle=1)
        datetime.date(2021, 3, 1)


    - if given a callback function (e.g. lambda function), the function must accept the 
      end of the month (e.g. 28 February) and the number of gap days between the "intended" 
      target date (e.g. 31 February) and the most recent feasible date (29 February)
      and return an integer (e.g. 1). The result of the callback function is then added to
      end of the month. 

    :: 

        >>> offset(datetime.date(2020, 1, 31), months=1, handle=lambda eom, gap: 0)
        datetime.date(2020, 2, 29)

        >>> offset(datetime.date(2020, 1, 31), months=1, handle=lambda eom, gap: 1)
        datetime.date(2020, 3, 1)

        >>> offset(datetime.date(2020, 1, 31), months=1, handle=lambda eom, gap: 2)
        datetime.date(2020, 3, 2)

        >>> offset(datetime.date(2020, 1, 31), months=1, handle=lambda eom, gap: gap)
        datetime.date(2020, 3, 2) #gap is 2 as 2020 is a leap year

        >>> offset(datetime.date(2021, 1, 31), months=1, handle=lambda eom, gap: gap)
        datetime.date(2020, 3, 3) #gap is 3 as 2021 is not a leap year

        >>> offset(datetime.date(2020, 8, 31), months=1, handle=lambda eom, gap: gap)
        datetime.date(2020, 10, 1) #gap is 1

    Examples
    ------------
    >>> today = datetime.date(2020, 1, 10)
    >>> today
    datetime.date(2020, 1, 10) #Friday
    
    >>> offset(today, days=1)
    datetime.date(2020, 1, 11) #Saturday
    
    >>> offset(today, weekdays=1)
    datetime.date(2020, 1, 13) #Monday
    
    >>> offset(today, weekdays=-1)
    datetime.date(2020, 1, 9) #Thursday
    
    >>> offset(today, weeks=1)
    datetime.date(2020, 1, 17) #Friday next week
    
    >>> offset(today, weekdays=5)
    datetime.date(2020, 1, 17) #also Friday next week
    
    >>> offset(today, months=1)
    datetime.date(2020, 2, 10)
    
    >>> jan31 = datetime.date(2020, 1, 31)
    >>> offset(jan31, months=1)
    datetime.date(2020, 2, 29) #defaults to end of month
    
    >>> offset(jan31, months=1, handle=1)
    datetime.date(2020, 3, 1)
    
    >>> offset(jan31, months=1, handle=lambda eom, days: 1)
    datetime.date(2020, 3, 1) #handle returns 1
    
    >>> offset(jan31, months=1, handle=lambda eom, days: days)
    datetime.dte(2020, 3, 2) #handle returns the size of the gap
    """
    if sum(arg is not None for arg in [days, weekdays, weeks, months, years, to]) != 1:
        raise ValueError("you must pass one argument of days, weekdays or weeks only")
    if days is not None:
        return date + datetime.timedelta(days=days)
    if weekdays is not None:
        if date.weekday() > 4:
            raise ValueError("cannot offset non weekday date by weekdays")
        weeks, days = weekdays // 5, weekdays % 5
        if days < 0:
            weeks, days = weeks - 1, days + 7
        return date + datetime.timedelta(
            7 * weeks + days + (2 if date.weekday() + days >= 5 else 0)
        )
    if weeks is not None:
        return date + datetime.timedelta(7 * weeks)
    if months is not None:
        try:
            return som(date, months).replace(day=date.day)
        except:
            # if it fails, it must be that date is 29 February
            if isinstance(handle, int):
                return eom(date, months) + datetime.timedelta(handle)
            monthend = eom(date, months)
            return monthend + datetime.timedelta(
                handle(monthend, (date.day - monthend.day))
            )
    if years is not None:
        try:
            return date.replace(year=date.year + years)
        except:
            # 29 February + 1 year...  adjust with the handle
            if isinstance(handle, int):
                return date.replace(
                    year=date.year + years, day=date.day - 1
                ) + datetime.timedelta(handle)
            monthend = date.replace(year=date.year + years, day=date.day - 1)
            return monthend + datetime.timedelta(
                handle(monthend, (date.day - monthend.day))
            )
    if to is not None:
        if to in constants.WEEKDAYS:
            if date.weekday() == constants.WEEKDAYS[to]:
                return date
            if date.weekday() > constants.WEEKDAYS[to]:
                return date + datetime.timedelta(
                    7 - (date.weekday() - constants.WEEKDAYS[to])
                )
            return date + datetime.timedelta(constants.WEEKDAYS[to] - date.weekday())
        if to == "EOM":
            return eom(date, 0)
        if to == "EOQ":
            return eoq(date, 0)
        if to == "EOS":
            return eos(date, 0)
        if to == "EOY":
            return eoy(date, 0)
        raise ValueError(
            f"to should be one of MON,...,SUN or one of EOM,EOQ,EOS,EOY; received {to}"
        )


class datemap:
    """
    Read-only sorted dictionary mapping dates to values

    Example
    -------
    .. code-block::

        >>> import doubledate as dtwo
        >>> import datetime

        >>> holidays = [
        ...     datetime.date(2022, 1, 17), 
        ...     datetime.date(2022, 5, 30), 
        ...     datetime.date(2022, 6, 4), 
        ...     datetime.date(2022, 9, 5), 
        ...     datetime.date(2022, 11, 11), 
        ...     datetime.date(2022, 12, 24),
        ...     datetime.date(2022, 12, 26)
        ... ]

        >>> mapping = dtwo.datemap({d:i for d, i in enumerate(holidays)})
        <doubledate.utils.datemap at 0x7fd0fa4cfa60>
    """

    def __init__(self, mapping):
        self._mapping = {date: mapping[date] for date in sorted(mapping)}

    def __len__(self):
        return len(self._mapping)

    def __contains__(self, value):
        return value in self._mapping

    def __iter__(self):
        return iter(self._mapping.values())

    def __getitem__(self, value):
        if isinstance(value, (datetime.date, datetime.datetime)):
            try:
                return self._mapping[value]
            except KeyError:
                raise KeyError(f"{value} not in datemap")
        return [self[v] for v in value]


def dayof(frequency: str, dates=None, *, calendar=None, base=1):
    """
    Returns an efficient iterator that yields the position of each date 
    in a given frequency.

    Arguments
    ------------
    dates : datetime, iterable
        either a date or an iterable of dates
    frequency : str
        one of Y, H, T, Q, M, W, W-MON,W-TUE,W-WED,W-THU,W-FRI,W-SAT,W-SUN
    calendar: iterable
        custom calendar to use
    base : int, defaults to 1
        whether the first date of the frequency should have value 0 or 1

    Returns
    ------------
    mapping : datemap 
        dictionary-like container mapping dates to position in frequency

    Examples
    ------------
    :: 
    
        >>> dayof(datetime.date(2020,2,29), "M")
        29
        >>> dayof(datetime.date(2020,2,29), "Q")
        60
        >>> dayof(datetime.date(2020,2,29), "W-THU") #Saturday
        3

        >>> dates = [datetime.date(2020,1,1) + datetime.timedelta(i) for i in range(90) if i % 12 != 0]
        >>> for date, position in zip(dates, dayof("M", calendar=dates)):
        ...     print(date, position)
        2020-01-02, 1
        2020-01-03, 2
        ...
        2020-02-29,27
        2020-03-02,1
        ...
        2020-03-30,27

        >>> dayof("Q", calendar=dates)[datetime.date(2020,3,30)]
        81

    Notes
    ------------
    .. warning:: 
        If given a calendar and no dates, the function returns a date-map, mapping each date
        of the custom calendar to its position within the frequency. 
        
        If given a set of dates and no calendar, the function returns the number of days
        from the generic start of the frequency. 
        
        If given a set of dates and a custom calendar, the function returns the number of days
        since the start of the frequency using the custom calendar as the reference.  
    """

    FREQUENCIES = [
        "Y",
        "H",
        "T",
        "Q",
        "M",
        "W",
        "W-MON",
        "W-TUE",
        "W-WED",
        "W-THU",
        "W-FRI",
        "W-SAT",
        "W-SUN",
    ]

    if frequency not in FREQUENCIES:
        raise ValueError(
            f"expected frequency to be one of {','.join(FREQUENCIES)}, \
                            received {frequency}"
        )

    mapping = {}

    if calendar is None:
        if isinstance(dates, (datetime.date, datetime.datetime)):
            return (dates - floor(dates, frequency)).days + base
        for i, date in enumerate(sorted(dates)):
            if i == 0 or date > end:
                start, end = floor(date, frequency), ceil(date, frequency)
            mapping[date] = (date - start).days + base
        return datemap(mapping)[dates]

    for i, date in enumerate(sorted(calendar)):
        if i == 0 or date > end:
            end, counter = ceil(date, frequency), base
        else:
            counter += 1
        mapping[date] = counter

    if dates is not None:
        return datemap(mapping)[dates]

    return datemap(mapping)


def daysfrom(frequency: str, dates=None, *, calendar=None):
    """
    Returns an efficient iterator that yields the number of days since the  
    start of a given frequency. 

    Arguments
    ------------
    dates : datetime, iterable, optional
        either a date or an iterable of dates
    calendar : iterable
        iterable of dates to use as custom calendar
    frequency : str
        one of YS, HS, TS, QS, MS, WS

    Notes
    ------------
    .. warning:: 
        If given a calendar and no dates, the function returns a date-map, mapping each date
        of the custom calendar to its position within the frequency. 
        
        If given a set of dates and no calendar, the function returns the number of days
        from the generic start of the frequency. 
        
        If given a set of dates and a custom calendar, the function returns the number of days
        since the start of the frequency using the custom calendar as the reference. 

    Examples
    ------------
    ::
    
        >>> daysfrom(datetime.date(2020,2,29), "MS")
        28
        >>> daysfrom(datetime.date(2020,2,29), "QS")
        59

        >>> dates = [datetime.date(2020,1,1) + datetime.timedelta(i) for i in range(90) if i % 12 != 0]
        >>> for date, position in zip(dates, daysfrom(dates, "MS")):
        ...     print(date, position)
        2020-01-02, 0
        2020-01-03, 1
        ...
        2020-02-29,26
        2020-03-02,0
        ...
        2020-03-30,26
    """
    FREQUENCIES = {"YS": "Y", "HS": "H", "TS": "T", "QS": "Q", "MS": "M", "WS": "W"}

    if frequency not in FREQUENCIES:
        raise ValueError(
            f"expected frequency to be one of {','.join(FREQUENCIES)}, \
                            received {frequency}"
        )
    return dayof(FREQUENCIES[frequency], dates, calendar=calendar, base=0)


def daysto(frequency: str, dates=None, *, calendar=None):
    """
    Returns an efficient iterator that yields the number of days to the  
    end of a given frequency. 

    Arguments
    ------------
    dates : datetime, iterable
        either a date or an iterable of dates
    calendar : iterable
        custom calendar to use
    frequency : str
        one of YE, HE, TE, QE, ME, WE

    Examples
    ------------
    ::
    
        >>> daysto("ME",datetime.date(2020,2,29))
        0
        >>> daysto("QE",datetime.date(2020,2,29))
        31

        >>> dates = [datetime.date(2020,1,1) + datetime.timedelta(i) for i in range(90) if i % 12 != 0]
        >>> for date, position in zip(dates, daysto("ME", calendar=dates)):
        ...     print(date, position)
        2020-01-02, 27
        2020-01-03, 26
        ...
        2020-02-29,0
        2020-03-02,26
        ...
        2020-03-30,0

    Notes
    ------------
    .. warning:: 
        If given a date (rather than a list of dates), the function returns the number of days to the 
        end of the calendar frequency. 

    .. note:: 
        The list of dates is assumed to be sorted chronologically (from oldest to 
        most recent), i.e. period changes are detected by comparing two adjacent dates
    """

    FREQUENCIES = {"YE": "Y", "HE": "H", "TE": "T", "QE": "Q", "ME": "M", "WE": "W"}

    if frequency not in FREQUENCIES:
        raise ValueError(
            f"expected frequency to be one of {','.join(FREQUENCIES)}, \
                            received {frequency}"
        )

    mapping = {}

    if calendar is None:
        if isinstance(dates, (datetime.date, datetime.datetime)):
            return (ceil(dates, FREQUENCIES[frequency]) - dates).days
        for i, date in enumerate(sorted(dates, reverse=True)):
            if i == 0 or date < start:
                start, end = (
                    floor(date, FREQUENCIES[frequency]),
                    ceil(date, FREQUENCIES[frequency]),
                )
            mapping[date] = (end - date).days
        return datemap(mapping)[dates]

    for i, date in enumerate(sorted(calendar, reverse=True)):
        if i == 0 or date < start:
            start, counter = floor(date, FREQUENCIES[frequency]), 0
        else:
            counter += 1
        mapping[date] = counter

    if dates is not None:
        return datemap(mapping)[dates]

    return datemap(mapping)


def weekdayof(frequency: str, date=None, *, base=1):
    """
    Returns the number of weeks since the start of the frequency
    assuming the week starts on the same weekday as the date given.

    Arguments
    -----------
    frequency : str
        one of Y, H, T, Q, M
    date : datetime-like
        the date 
    base : int
        whether to consider the first date as 0 or 1
    
    Examples
    -------------
    >>> weekdayof("Y", datetime.date(2020,1,27))
    4 #4th Monday of the year

    >>> weekdayof("Y", datetime.date(2020,6,17))
    25 #25th Tuesday of the year

    >>> weekdayof("M", datetime.date(2020,3,31))
    5 #5th Tuesday of March
    """
    if frequency not in ["Y", "H", "T", "Q", "M"]:
        raise ValueError(
            f"expected frequency to be one of 'YHTQM', receive {frequency}"
        )

    freqstart = floor(date, frequency)
    return (
        int(
            (
                sow(date, weekday=freqstart.weekday())
                - eow(freqstart, weekday=freqstart.weekday())
            ).days
            / 7
        )
        + base
    )
