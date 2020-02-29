import calendar
import datetime
import dateutil.parser

import doubledate.constants as constants

def semester(date, *, base=1):
    """
    Returns the semester index of the given date

    Examples
    ------------
    >>> semester(datetime.date(2020, 1, 10))
    1

    >>> semester(datetime.date(2020, 1, 10), base=0)
    0
    """
    return (date.month - 1)//6 + base

def trimester(date, *, base=1):
    """
    returns the trimester index of the given date

    Examples
    ------------
    >>> trimester(datetime.date(2020, 1, 10))
    1

    >>> trimester(datetime.date(2020, 1, 10), base=0)
    0
    """
    return (date.month - 1)//4 + base

def quarter(date, *, base=1):
    """
    Returns the quarter index of the given date

    Examples
    ------------
    >>> quarter(datetime.date(2020, 1, 10))
    1

    >>> quarter(datetime.date(2020, 1, 10), base=0)
    0
    """
    return (date.month - 1)//3 + base

def sow(date, offset=0, weekday="MON"):
    """
    Returns the start of the week, i.e. the first date on or before the given date 
    whose weekday is equal to the the weekday argument, and 
    offset by a given number of weeks. Weekday must be one of MON...SUN.

    Examples
    ------------
    >>> today = datetime.date(2020, 1, 15) #Wednesday
    >>> sow(today) 
    datetime.date(2020, 1, 13) #Monday

    >>> sow(today, 1)
    datetime.date(2020, 1, 20) #following Monday

    >>> sow(today, weekday="THU")
    datetime.date(2020, 1, 9) #last Thursday
    """
    if isinstance(weekday, str):
        weekday = constants.WEEKDAYS.index(weekday)
    return date + datetime.timedelta(offset * 7 - ((date.weekday() - weekday) % 7))

def eow(date, offset=0, weekday="SUN"):
    """
    Returns the end of the week, i.e. the first date on or after the given date
    whose weekday is equal to the the weekday argument, and 
    offset by a given number of weeks. 
    
    Weekday must be one of MON...SUN.

    Examples
    ------------
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
        weekday = constants.WEEKDAYS.index(weekday)
    return date + datetime.timedelta((weekday - date.weekday()) % 7 + offset * 7)

def som(date, offset=0):
    """
    Returns the start of the month some offset months from the date

    Example
    ------------
    >>> today = datetime.date(2020, 1, 15)
    >>> som(today)
    datetime.date(2020, 1, 1) #start of the current month

    >>> som(today, 1):
    datetime.date(2020, 2, 1) #first of February

    >>> som(today, -1):
    datetime.date(2019, 12, 1) #start of the previous month
    """
    return date.replace(
        year=(date.year + (date.month + offset - 1) // 12),
        month=((date.month - 1 + 12 * date.year + offset) % 12 + 1), 
        day=1)

def eom(date, offset=0):
    """
    Returns the end of month some given offset months away, emulating Excel's EOM function

    Examples
    ------------
    >>> today = datetime.date(2020, 1, 15)
    >>> eom(today) 
    datetime.date(2020, 1, 31)

    >>> eom(today, 1)
    datetime.date(2020, 2, 29) #2020 is a leap year

    >>> eom(today, -1)
    datetime.date(2019, 12, 31) #end of previous month
    """
    if offset == 0:
        return date.replace(day=calendar.monthrange(year=date.year, month=date.month)[1])
    return eom(som(date, offset))

def soq(date, offset=0):
    """
    Returns the first date of the quarter, i.e. one of 
    1 January, 1 April, 1 July or 1 October
    """
    return (eoq(date, offset) - datetime.timedelta(2 * 31 + 1)).replace(day=1)

def eoq(date, offset=0):
    """
    Returns the end of the calendar quarter, i.e. one of
    31 March, 30 June, 30 September or 31 December
    """
    return eom(date.replace(
        year=((date.month - 1) + date.year * 12 + 3 * offset) // 12, 
        month=3*(((date.month - 1)//3 + offset) % 4 + 1),
        day=1))
        
def eot(date, offset=0):
    """
    Returns the end of the calendar trimester, i.e. one of 
    30 April, 31 August or 31 December
    """
    return eom(date.replace(
        year=((date.month - 1) + date.year * 12 + 4 * offset) // 12, 
        month=4*(((date.month - 1)//4 + offset) % 3 + 1),
        day=1
    ))

def sot(date, offset=0):
    """
    Returns the first date of the calendar trimester, i.e. one of
    1 January, 1 May or 1 September
    """ 
    return (eot(date, offset) - datetime.timedelta(3 * 31 + 1)).replace(day=1)

def eos(date, offset=0):
    """
    Returns the end of the calendar semester, i.e. one of 
    30 June or 31 December
    """
    return eom(date.replace(
        year=((date.month - 1) + date.year * 12 + 6 * offset) // 12, 
        month=6*(((date.month - 1)//6 + offset) % 2 + 1),
        day=1
    ))

def sos(date, offset=0):
    """
    Returns the first date of the calendar semester, i.e. one of
    1 January or 1 July
    """ 
    return (eos(date, offset) - datetime.timedelta(5 * 31 + 1)).replace(day=1)

def soy(date, offset=0):
    """
    Returns the start of the year at a given offset
    """
    return type(date)(date.year + offset, 1, 1)

def eoy(date, offset=0):
    """
    Returns the end of the year at a given offset
    """
    return type(date)(date.year + offset, 12, 31)

def floor(date, frequency):
    """
    Returns the start of the frequency (e.g. quarter) for the date passed as first argument

    Arguments
    ------------
    date : datetime-like
        the date
    frequency : str
        one of Y, H, Q, M, W or W-MON...W-SUN for, respectively, year, semester, quarter, 
        month, week (or specific weekday)

    Examples
    ------------
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

def ceil(date, frequency):
    """
    Returns the end of the frequency (e.g. quarter) for the date passed as first argument

    Arguments
    ------------
    date : datetime-like
        the date to offset
    frequency : str
        one of Y, H, Q, M, W or W-MON...W-SUN for, respectively, year, semester, quarter, 
        month, week (or specific weekday)

    Examples
    ------------
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

def isleap(year):
    """
    Returns whether the given year is a leap-year

    Examples
    ------------
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
    return dateutil.parser.parse(date, dayfirst=dayfirst, 
            yearfirst=yearfirst, fuzzy=fuzzy).date()

def offset(date, days=None, weekdays=None, weeks=None, months=None, years=None, 
           to=None, handle=lambda eom, days: 0): 
    """
    Returns the date offset either by a number of frequencies 
    or else to the nearest frequency
    
    Arguments
    ------------
    date : datetime-like
        the date to offset
    days : int, optional
        the number of days to offset the date by
        shorthand notation for date + datetime.timedelta(days=days)
    weekdays : int, optional
        the number of weekays to offset the date by; 
        the given date to offset should be a weekday
    weeks : int, optional 
        shorthand notation for days = 7 * weeks
    months : int, optional 
        the number of months to offset the date by
        if the day does not exist in the target month, it will return 
        the end-of-month date of the target month plus the number of days 
        returned by the handle callback function, which by default is 0
    years : int, optional
        the number of years to offset the date by
        if the day does not exist in the target month, it will return 
        the end-of-month date of the target month plus the number of days 
        returned by the handle callback function, which by default is 0
    to : str, optional
        either the name of the nearest weekday to offset to
        if the date is already the target weekday, it simply returns the date; 
        otherwise it offsets forward to the nearest such weekday
        or one of EOM, EOQ, EOS or EOY for, respectively, 
        the end of the month, the end of the quarter, the end of the semester
        or the end of the year
        Note that EOW (end of week) can be reproduced by setting to="SUN" or
        whichever weekday the end of the week refers to.  
    handle : int, function, optional
        the number of days to add to the end-of-month of the target month in cases 
        where the target month is too short for the offset date's day
        can be either an integer or a callback (lambda) function which takes the 
        end of the month and the number of days difference, and must return an integer
    
    Raises 
    ------------
    ValueError 
        on invalid arguments
        
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
    
    >>> monthend = datetime.date(2020, 1, 31)
    >>> offset(monthend, months=1)
    datetime.date(2020, 2, 29) #defaults to end of month
    
    >>> offset(monthend, months=1, handle=1)
    datetime.date(2020, 3, 1)
    
    >>> offset(monthend, months=1, handle=lambda eom, days: 1)
    datetime.date(2020, 3, 1) #handle returns 1
    
    >>> offset(monthend, months=1, handle=lambda eom, days: days)
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
        return date + datetime.timedelta(7 * weeks + days + (2 if date.weekday() + days >= 5 else 0))
    if weeks is not None: 
        return date + datetime.timedelta(7 * weeks)
    if months is not None: 
        try: 
            return som(date, months).replace(day=date.day)
        except: 
            #if it fails, it must be that date is 29 February
            if isinstance(handle, int): 
                return eom(date, months) + datetime.timedelta(handle)
            monthend = eom(date, months)
            return monthend + datetime.timedelta(handle(monthend, (date.day-monthend.day)))
    if years is not None: 
        try: 
            return date.replace(year=date.year + years)
        except: 
            #29 February + 1 year...  adjust with the handle
            if isinstance(handle, int): 
                return date.replace(year=date.year + years, day=date.day-1) + datetime.timedelta(handle)
            monthend = date.replace(year=date.year + years, day=date.day-1)
            return  monthend + datetime.timedelta(handle(monthend, (date.day-monthend.day)))
    if to is not None: 
        if to in constants.WEEKDAYS:
            if date.weekday() == constants.WEEKDAYS.index(to): 
                return date
            if date.weekday() > constants.WEEKDAYS.index(to): 
                return date + datetime.timedelta(7 - (date.weekday() - constants.WEEKDAYS.index(to)))
            return date + datetime.timedelta(constants.WEEKDAYS.index(to) - date.weekday())
        if to == "EOM": 
            return eom(date, 0)
        if to == "EOQ":
            return eoq(date, 0)
        if to == "EOS":
            return eos(date, 0)
        if to == "EOY": 
            return eoy(date, 0)
        raise ValueError(f"to should be one of MON,...,SUN or one of EOM,EOQ,EOS,EOY; received {to}")

class dayof:
    FREQUENCIES = ["Y","H","T","Q","M","W",
                   "W-MON","W-TUE","W-WED","W-THU","W-FRI","W-SAT","W-SUN"]
    
    def __new__(cls, dates, frequency, base=1):
        if frequency not in dayof.FREQUENCIES:
            raise ValueError(f"expected frequency to be one of {','.join(dayof.FREQUENCIES)}, \
                             received {frequency}")
        if isinstance(dates, (datetime.date, datetime.datetime)): 
            return (dates - floor(dates, frequency)).days + base
        return super().__new__(cls)
        
    def __init__(self, dates, frequency, base=1):
        """
        Returns an efficient iterator that yields the position of each date 
        in a given frequency. 

        Arguments
        ------------
        dates : datetime, iterable
            either a date or an iterable of dates
        frequency : str
            one of Y, H, T, Q, M, W, W-MON,W-TUE,W-WED,W-THU,W-FRI,W-SAT,W-SUN
        base : int, defaults to 1
            whether the first date of the frequency should have value 0 or 1

        Examples
        ------------
        >>> dayof(datetime.date(2020,2,29), "M")
        29
        >>> dayof(datetime.date(2020,2,29), "Q")
        60
        >>> dayof(datetime.date(2020,2,29), "W-THU") #Saturday
        3

        >>> dates = [datetime.date(2020,1,1) + datetime.timedelta(i) for i in range(90) if i % 12 != 0]
        >>> for date, position in zip(dates, dayof(dates, "M")):
            print(position, date)
        2020-01-02, 1
        2020-01-03, 2
        ...
        2020-02-29,27
        2020-03-02,1
        ...
        2020-03-30,27

        >>> daysof(dates, "Q")[datetime.date(2020,3,30)]
        81

        Notes
        ------------
        If the first argument is a date, it simply returns the 1-based position
        of the date in the given frequency (e.q. month, quarter).

        The list of dates is assumed to be sorted chronologically (from oldest to 
        most recent). 
        """
        self.dates = dates
        self.frequency = frequency
        self.base = base
        
    @property
    def mapping(self):
        """
        Returns a dictionary mapping each date to its position
        """
        if not hasattr(self, "_mapping"):
            self._mapping, count = {}, 0
            for i, date in enumerate(self.dates):
                if i == 0: 
                    end = ceil(date, self.frequency)
                    counter = self.base
                elif date > end: 
                    end = ceil(date, self.frequency)
                    counter = self.base
                else: 
                    counter += 1
                self._mapping[date] = counter
        return self._mapping
            
    def __iter__(self):
        return iter(self.mapping.values())
    
    def __getitem__(self, date):
        return self.mapping[date]