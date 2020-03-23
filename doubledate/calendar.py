"""
Calendar object
"""
import sortedcontainers
import collections
import datetime

import doubledate.utils as utils
import doubledate.constants as constants

class BD: 
    def __init__(self, index, frequency="M"):
        self.index     = index
        self.frequency = frequency

    def resolve(self, calendar, onerror="last"): 
        dates = []
        for subcal in calendar.resample(self.frequency):
            try:
                dates.append(subcal[self.index])
            except Exception as e:
                if onerror == "raise":
                    raise e 
                elif onerror == "drop" or onerror == "skip":
                    pass
                elif onerror == "last":
                    dates.append(subcal[-1])
                elif onerror == "first":
                    dates.append(subcal[0])
                elif callable(onerror):
                    dates.append(onerror(subcal))
                else:
                    raise ValueError("expected onerror to be one of raise, last, first or callable")
        return Calendar(dates)

class Calendar:
    def __init__(self, dates=None):
        """
        Creates a calendar using the optional dates iterable

        Throws
        ------------
        TypeError
            if dates is not an iterable of date-like objects
        """
        if dates is None: 
            dates = []
        if not all([isinstance(item, (datetime.date, datetime.datetime)) for item in dates]):
            raise TypeError("Calendar expected an iterable of date objects")
        self.__dates__    = sortedcontainers.SortedSet([date for date in dates])
        self.__datemaps__ = {}
    
    @property
    def last(self):
        """
        Returns the last date in the calendar

        Throws
        ------------
        KeyError
            if the calendar is empty
        """
        return self.__dates__[-1]

    @property
    def end(self):
        """
        Returns the last date in the calendar

        Throws
        ------------
        KeyError
            if the calendar is empty
        """
        return self.last

    @property
    def first(self):
        """
        Returns the first date in the calendar

        Throws
        ------------
        KeyError
            if the calendar is empty
        """
        return self.__dates__[0]

    @property
    def start(self):
        """
        Returns the first date in the calendar

        Throws
        ------------
        KeyError
            if the calendar is empty
        """
        return self.first
        
    @property
    def dates(self):
        """
        Returns the dates as a list
        """
        return list(self.__dates__)

    def __len__(self):
        """
        Returns the length of the calendar
        """
        return len(self.__dates__)

    def __contains__(self, date):
        """
        Returns True if the date is in the calendar
        """
        return date in self.__dates__

    def index(self, date):
        """
        Returns the index (0-based position) of the date

        Parameters
        ------------
        date : datetime-like
            the date whose index is searched
        """
        return self.__dates__.index(date)

    def __iter__(self):
        """
        Returns the iterator of the dates
        """
        return iter(self.__dates__)

    def __getitem__(self, value):
        """
        Retrieves a value at a given index
        Retrieves a calendar by a slice
        """
        if isinstance(value, int):
            return self.__dates__.__getitem__(value)
        elif isinstance(value, slice):
            if isinstance(value.start, (datetime.date, datetime.datetime)):
                value = slice(self.__dates__.bisect_left(value.start), value.stop)
            if isinstance(value.stop, (datetime.date, datetime.datetime)):
                value = slice(value.start, self.__dates__.bisect_right(value.stop))
            return Calendar(self.__dates__.__getitem__(value))
        raise KeyError("Invalid index or slice object")

    def __add__(self, other): 
        """
        Alias for union
        """
        if isinstance(other, (datetime.date, datetime.datetime)): 
            return Calendar(self).union(Calendar([other]))
        return Calendar(self).union(Calendar(other))

    def __eq__(self, other):
        """
        Returns True if all dates are in other, and all dates
        of other are in self

        Parameters
        ------------
        other : Calendar, iterable
            the compared calendar
        """
        for date in self: 
            if date not in other: 
                return False
        for date in other:
            if date not in self: 
                return False
        return True

    def union(self, *others):
        """
        Combines two calendar by including dates in self and other
        """
        return Calendar(self.__dates__.union(*others))

    def difference(self, *others):
        """
        Returns a calendar in this and not in other
        """
        return Calendar(self.__dates__.difference(*others))

    def intersection(self, *others):
        """
        Returns a calendar including dates contained both in self and other
        """
        return Calendar(self.__dates__.intersection(*others))

    def filter(self, func=None, *, year=None, semester=None, quarter=None, month=None, week=None, weekday=None):
        """
        Returns a new filtered calendar
        Either pass a filtering function, one or several filtering criterai

        Arguments
        ------------
        func : function, optional
            the filtering function
        year : int, optional
            pass a value to filter dates of the given year only
        semester : int, optional (1 or 2)
            pass a value to filter dates of the given semester only
        quarter : int, optional (1, 2, 3, or 4)
            pass a value to filter dates of the given quarter only
        month : int, optional (1 through 12)
            pass a value to filter dates of the given month only
        week : int, optional (1 through 53)
            pass a value to filter dates of the given week number only
        weekday : int, optional (0 through 6)
            pass a value to filter dates of the given weekday only
            Monday = 0, Tuesday = 1... Sunday = 6

        Return
        ------------
        filtered : Calendar

        Example 
        ------------
        >>> cdr = Calendar([dates]) #assume dates is a list of dates
        >>> cdr.filter(year=2020, quarter=3)
        """
        if func is not None:
            if not callable(func):
                raise ValueError("Filter accepts either a function, one or several named arguments")
            return Calendar([date for date in self.__dates__ if func(date)])
        if all([arg is None for arg in [year, semester, quarter, month, week, weekday]]):
            raise ValueError("You need to provide one of year, semester, quarter, month, week, weekday")
        dates = list(self.__dates__)
        if year is not None: 
            dates = list(filter(lambda date: date.year == year, dates))
        if semester is not None: 
            dates = list(filter(lambda date: utils.semester(date) == semester, dates))
        if quarter is not None: 
            dates = list(filter(lambda date: utils.quarter(date) == quarter, dates))
        if month is not None: 
            dates = list(filter(lambda date: date.month == month, dates))
        if week is not None: 
            dates = list(filter(lambda date: date.isocalendar()[1] == week, dates))
        if weekday is not None:
            dates = list(filter(lambda date: date.weekday() == weekday, dates))
        return Calendar(dates)

    def weekdays(self):
        """
        Filters out all the weekends
        Assumed to mean Saturdays and Sundays

        Return
        ------------
        filtered : Calendar
        """
        return self.filter(lambda date: date.weekday() not in [5, 6])

    def weekends(self):
        """
        Filters out all the weekdays

        Return
        ------------
        filtered : Calendar
        """
        return self.filter(lambda date: date.weekday() in [5, 6])

    def inverse(self, starting=None, ending=None):
        """
        Returns the negative of the calendar, using this calendar as the holiday mask

        Return
        ------------
        inversed : Calendar
        """
        if starting is None: 
            starting = self.__dates__[0]
        if ending is None: 
            ending = self.__dates__[-1]
        dates = []
        for i in range(1, (ending-starting).days):
            if starting + datetime.timedelta(i) not in self:
                dates.append(starting + datetime.timedelta(i))
        return Calendar(dates)

    def dayof(self, date, frequency=None, *, base=1):
        """
        Returns the position of the date in the calendar at a given 
        frequency. By default, base is 1. 

        Return
        ------------
        position : int 
            the index + 1 of the given date in the filtered frequency
        """
        if ("dayof", frequency, base) not in self.__datemaps__: 
            mapping = utils.dayof(frequency, calendar=self, base=base)
            self.__datemaps__[("dayof", frequency, base)] = mapping
        return self.__datemaps__[("dayof", frequency, base)][date]

    def daysfrom(self, start=None, *, asof=None):
        """
        Returns the number of days since the start of the given frequency
        This is exclusive of the given date (i.e. base 0)

        Return
        ------------
        days : int 
            the number of days prior to the date but in the same frequency
        """
        if isinstance(start, (datetime.date, datetime.datetime)):
            return len(self[start:asof]) - 1

        if ("daysfrom", start) not in self.__datemaps__: 
            mapping = utils.daysfrom(start, calendar=self)
            self.__datemaps__[("daysfrom", start)] = mapping
        if asof is not None: 
            return self.__datemaps__[("daysfrom", start)][asof]
        return self.__datemaps__[("daysfrom", start)]

    def daysto(self, to=None, *, asof=None):
        """
        returns the number of days left until the end of the given frequency

        Returns 
        ------------
        days : int 
            number of days in the calendar until the end of the frequency;
            exlusive of the given date
        """
        if isinstance(to, (datetime.date, datetime.datetime)):
            return len(self[asof:to]) - 1
             
        if ("daysto", to) not in self.__datemaps__: 
            mapping = utils.daysto(to, calendar=self)
            self.__datemaps__[("daysto", to)] = mapping
        if asof is not None: 
            return self.__datemaps__[("daysto", to)][asof]
        self.__datemaps__[("daysto", to)]
    
    def daysbetween(self, this, that, bounds="both"): 
        """
        returns the number of open days between two dates

        Arguments
        ------------
        this : date-like
            the left-bound of the calendar
        that : date-like
            the right-bound of the calenar
        bounds : str, optional
            whether to include this or that in the count
            one of 'both' (default), 'left' or 'right' or None

        Returns 
        ------------
        sliced : Calendar
            the calendar starting no earlier than this, and ending no later than that
        """
        if bounds == "both":
            return len(self.filter(lambda date: min(this, that) <= date <= max(this, that)))
        if bounds == "left":
            return len(self.filter(lambda date: min(this, that) <= date < max(this, that)))
        if bounds == "right":
            return len(self.filter(lambda date: min(this, that) < date <= max(this, that)))
        if bounds is None:
            return len(self.filter(lambda date: min(this, that) < date < max(this, that)))
        raise ValueError(f"bounds should be one of 'both', 'left' or 'right', {bounds} given")

    def offset(self, date, days):
        """
        returns the date in the calendar offset by n days

        Arguments
        ------------
        date : date-like
            the reference date
        days : int
            the offset

        Returns
        ------------
        offsetted : date-like
            the date in the calendar days-away from the given date
        """
        if not date in self: 
            raise ValueError(f"{date} is not in the calendar")
        return self[self.index(date) + days]

    def groupby(self, grouper):
        """
        Returns a calendar-grouper object containing the sub-calendars
        Dates are grouped by the grouper argument
        Grouper argument can be a function or a string frequency
        If the grouper is a string, groups are created by year
        IF the grouper is a callable, the callable will receive the date and must return a hashable value

        Arguments
        ------------
        grouper : str | callable
            the criterion to group dates by
            string groupers include
                - W: groupby by week number
                - M: groupby by month
                - Q: groupby by quarter
                - H: groupby semester
                - Y: groupby year
        """
        if isinstance(grouper, str):
            if grouper == "W":
                return self.groupby(lambda date: (date.year, date.isocalendar()[1]))
            elif grouper == "M":
                return self.groupby(lambda date: (date.year, date.month))
            elif grouper == "Q":
                return self.groupby(lambda date: (date.year, utils.quarter(date)))
            elif grouper == "H":
                return self.groupby(lambda date: (date.year, date.month > 6))
            elif grouper == "Y":
                return self.groupby(lambda date: date.year)
            raise ValueError(f"grouper should be a callable or one of W,M,Q,H or Y; {grouper} given")
        if callable(grouper):
            calendars = collections.defaultdict(lambda: [])
            for date in self: 
                calendars[grouper(date)].append(date)
            return Grouper([Calendar(dates) for dates in calendars.values()])
        raise ValueError("Expected string or function")

    def resample(self, grouper): 
        """
        alias for groupby
        """
        return self.groupby(grouper)

    def split(self, on=None, side="left", starting=None, ending=None):
        """
        Splits the calendar in subcalendars at the given frequency and on the given index, 
        assuming that the passed index is the first date of each period. 

        Arguments
        ---------------
        frequency : str
            one of 'month', 'quarter', 'trimester', 'semester' or 'year
        on : int
            one of 0...27 or -1...-27

        Returns
        ---------------
        subcalendars : Grouper
            the subcalendars
        """
        if sum(0 if arg is None else 1 for arg in [on, starting, ending]) != 1: 
            raise ValueError("Expected one of on, starting or ending")
        if starting is not None: 
            on, side = starting, "left"
        if ending is not None: 
            on, side = ending, "right"
        if not isinstance(on, BD):
            raise TypeError("expected cutoff to be an instance of BD")
        splitdays = on.resolve(self, onerror="drop")
        calendars = collections.defaultdict(lambda: [])
        for date in self: 
            try:
                calendars[splitdays.asof(date, side)].append(date)
            except:
                pass
        return Grouper([Calendar(calendar) for calendar in calendars.values()])

    def fa(self, date, default=constants.RAISE):
        """
        Returns the first date after ("first-after", or "fa")

        Arguments
        ------------
        date : date-like
            the date from which to compute the first date strictly after in the calendar
        default : optional
            the default value if the given date is on or after the last date in the calendar
            if no default value is given, it will raise an KeyError

        Return
        ------------
        date : datetime.date
            the first date following the given date argument
        """
        if date > self.__dates__[-1]:
            if default == constants.RAISE:
                raise KeyError(f"Out-of-range error: {date} is after last date in the calendar")
            return default
        return self.__dates__[self.__dates__.bisect_right(date)]

    def lb(self, date, default=constants.RAISE):
        """
        Returns the last date immediately before ("last-before", or "lb")

        Arguments
        ------------
        date : date-like
            the lookup date

        default: *, optional
            default value if the given date is strictly before the first date in the calendar

        Return
        ------------
        date : datetime.date
            the last date immediately before the given date argument
        """
        if date < self.__dates__[0]: 
            if default == constants.RAISE:
                raise KeyError(f"Out-of-range error: {date} is before the first date in the calendar")
            return default
        return self.__dates__[self.__dates__.bisect_left(date) - 1]

    def asof(self, date, side="left", default=constants.RAISE):
        """
        Returns the date if the date is in the calendar, or the last date before that

        Arguments
        ------------
        date : date-like
            the lookup date

        default: *, optional
            default value if the given date is strictly before the first date in the calendar

        Return
        ------------
        date : datetime.date
            the date or its immediate precedent in the calendar
        """
        if date in self: 
            return date
        if side == "left":
            return self.lb(date, default=default)
        if side == "right":
            return self.fa(date, default=default)
        raise ValueError(f"side should be one of 'left' or 'right', {side} given")

    def snap(self, other, fallback="drop"):
        """
        Snaps this calendar to another
        Date in both calendars are kept
        Dates in this calendar but not in other are either dropped or
        replaced with either the first previous or following date in other

        Arguments
        ------------
        other : iterable
            other calendar
        
        fallback : str, optional
            one of drop, previous (a.k.a. ffill), next (a.k.a. bfill)

        Return
        ------------
        snapped : Calendar
            the snapped calendar
        """
        if fallback not in ["drop", "previous", "ffill", "next", "bfill"]: 
            raise ValueError("fallback should be one of 'drop', 'previous' or 'next'")
        filtered, other = [], Calendar(other)
        for date in self: 
            if date in other: 
                filtered.append(date)
            else: 
                if fallback == "drop":
                    pass
                elif fallback in ["last", "previous", "ffill"]:
                    filtered.append(other.lb(date))
                elif fallback in ["next", "bfill", "following"]:
                    filtered.append(other.fa(date))
        return Calendar(filtered)

    def apply(self, func):
        """
        Passes all the dates in the calendar to the function
        If all mapped values are date-like objects, function returns a new calendar
        Else it returns a new list

        Returns
        ------------
        mapped : Calendar | List
            the mapped values
        """ 
        if not callable(func): 
            raise ValueError("Expected func to be a callable function")
        mapped = [func(date) for date in self]
        if all([isinstance(m, (datetime.date, datetime.datetime)) for m in mapped]): 
            return Calendar(mapped)
        return mapped

    def som(self, date):
        """
        return the first open day of the month given the date
        """
        for i in range(self.index(date), -1, -1):
            if self.__dates__[i].month == date.month and self.__dates__[i].year == date.year: 
                continue
            return self.__dates__[i+1]
        return self.__dates__[i]

    def eom(self, date):
        """
        return the last open day of the month given the date
        """
        for i in range(self.index(date), len(self)):
            if self.__dates__[i].month == date.month and self.__dates__[i].year == date.year: 
                continue
            return self.__dates__[i-1]
        return self.__dates__[i]

    def soq(self, date):
        """
        return the first open day of the quarter given the date
        """
        for i in range(self.index(date), -1, -1):
            if utils.quarter(self.__dates__[i]) == utils.quarter(date) and self.__dates__[i].year == date.year:
                continue
            return self.__dates__[i+1]
        return self.__dates__[i]

    def eoq(self, date):
        """
        Returns the last open date of the quarter
        """
        for i in range(self.index(date), len(self)):
            if utils.quarter(self.__dates__[i]) == utils.quarter(date) and self.__dates__[i].year == date.year: 
                continue
            return self.__dates__[i-1]
        return self.__dates__[i]

    def sot(self, date):
        """
        return the first open day of the trimester given the date
        """
        for i in range(self.index(date), -1, -1):
            if utils.trimester(self.__dates__[i]) == utils.trimester(date) and self.__dates__[i].year == date.year:
                continue
            return self.__dates__[i+1]
        return self.__dates__[i]

    def eot(self, date):
        """
        Returns the last open date of the trimester
        """
        for i in range(self.index(date), len(self)):
            if utils.trimester(self.__dates__[i]) == utils.trimester(date) and self.__dates__[i].year == date.year: 
                continue
            return self.__dates__[i-1]
        return self.__dates__[i]

    def sos(self, date):
        """
        return the first open day of the semester given the date
        """
        for i in range(self.index(date), -1, -1):
            if utils.semester(self.__dates__[i]) == utils.semester(date) and self.__dates__[i].year == date.year:
                continue
            return self.__dates__[i+1]
        return self.__dates__[i]

    def eos(self, date):
        """
        Returns the last open date of the semester
        """
        for i in range(self.index(date), len(self)):
            if utils.semester(self.__dates__[i]) == utils.semester(date) and self.__dates__[i].year == date.year: 
                continue
            return self.__dates__[i-1]
        return self.__dates__[i]

    def soy(self, date):
        """
        return the first open day of the year given the date
        """
        for i in range(self.index(date), -1, -1):
            if self.__dates__[i].year == date.year:
                continue
            return self.__dates__[i+1]
        return self.__dates__[i]

    def eoy(self, date):
        """
        Returns the last open date of the quarter
        """
        for i in range(self.index(date), len(self)):
            if self.__dates__[i].year == date.year: 
                continue
            return self.__dates__[i-1]
        return self.__dates__[i]

class Grouper: 
    def __init__(self, calendars=None):
        if calendars is None: 
            self.calendars = []
        else:
            if not all([isinstance(calendar, Calendar) for calendar in calendars]): 
                raise TypeError("Expected a list of calendar objects")
            self.calendars = list(calendars)

    def first(self):
        """
        Returns the first date of each subcalendar
        """
        return Calendar([calendar[0] for calendar in self.calendars])

    def last(self):
        """
        Returns the last date of each subcalendar
        """
        return Calendar([calendar[-1] for calendar in self.calendars])

    def __getitem__(self, value):
        """
        Returns one or several subcalendars
        """
        if isinstance(value, int):
            return self.calendars[value]
        if isinstance(value, (datetime.date, datetime.datetime)):
            return self[self.index(value)]
        if isinstance(value, slice):
            return Calendar().union(*self.calendars[value])

    def index(self, date):
        """
        Returns the 0-based index of the calendar containing the date
        """
        if isinstance(date, (datetime.date, datetime.datetime)):
            for i, calendar in enumerate(self.calendars):
                if date in calendar: 
                    return i
            raise IndexError(f"{date} is not in any subcalendar")
        if isinstance(value, Calendar):
            return self.calendars.index(value)
        raise ValueError("Invalid use of .index")

    def __contains__(self, date):
        """
        Returns True if one of the subcalendars contains the given date
        """
        for calendar in self.calendars: 
            if date in calendar: 
                return True
        return False

    def apply(self, func, onerror="raise"):
        """
        Apply a function to each sub-calendars
        """
        if not callable(func): 
            raise ValueError("Expected func to be a callable function")
        dates = []
        for c in self.calendars:
            try:
                dates.append(func(c))
            except Exception as e: 
                if onerror == "raise":
                    raise e
                elif onerror == "skip" or onerror == "drop":
                    pass
                elif onerror == "first":
                    dates.append(c[0])
                elif onerror == "last":
                    dates.append(c[-1])
                elif callable(onerror):
                    dates.append(onerror(c))
                else: 
                    raise ValueError("Expected onerror to be one of raise, first, last or callable")
        for i, value in enumerate(dates):
            if isinstance(value, (datetime.date, datetime.datetime)): 
                dates[i] = Calendar([value])
            elif isinstance(value, (list, tuple)):
                dates[i] = Calendar(value)
            elif isinstance(value, Calendar):
                pass
            else: 
                raise ValueError("mapped values must be a datetime, a list thereof or a Calendar")
        return Grouper(dates)

    def filter(self, func):
        """
        Filters out subcalendars
        """
        if not callable(func): 
            raise ValueError("Expected func to be a callable function")
        return Grouper([cal for cal in self.calendars if func(cal)])

    def combine(self):
        """
        Combines the subcalendars in one
        """
        return Calendar().union(*self.calendars)

    def __len__(self):
        """
        Returns the 
        """
        return len(self.calendars)

    def __iter__(self):
        return iter(self.calendars)