import sortedcontainers
import collections
import datetime

import doubledate.utils as utils
import doubledate.constants as constants


class BD:
    """
    Business day

    Parameters
    ----------
    index : int
        day of the frequency
    frequency : str
        one of 'D','W','M','Q','H' or 'Y'
    base : 0 (default), 1
        whether to consider the index 1-based or 0-based 
    """

    def __init__(self, index: int, frequency: str = "M", *, base: int = 0):
        if not isinstance(index, int):
            raise TypeError(
                f"Expected index to be an integer, received {type(index).__name__}"
            )
        self.index = index

        if frequency not in ["D", "W", "M", "Q", "H", "Y"]:
            raise ValueError(
                f"Expected frequency to be one of 'D','W','M','Q','H' or 'Y', received '{frequency}'"
            )
        self.frequency = frequency

        if base not in (0, 1):
            raise ValueError(f"Expected base to be one of 0 or 1, received {base}")
        self.base = base

    def resolve(self, calendar, onerror: str = "skip"):
        """
        Returns a new Calendar containing only the n'th business day 
        each frequency.

        Allowed values for the onerror parameter: 
            - 'skip' to skip periods where the n'th business day is not defined
            - 'first' to fallback to the first date in the period when the n'th 
              business day is not defined
            - 'last' to fallback to the last date in the period when the n'th 
              business day is not defined
            - 'raise' to raise an error if the n'th business day is not defined

        Parameters
        ----------
        calendar : Calendar
            the calendar from which to compute the n'th business day
        onerror : str
            handling policy for periods the n'th business day is not defined

        Returns
        -------
        Calendar
            Calendar containing the n'th business day each frequency
        """
        if self.frequency == "D":
            return calendar

        dates = []
        for subcal in calendar.resample(self.frequency):
            try:
                dates.append(subcal[self.index - self.base])
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
                    raise ValueError(
                        f"expected onerror to be one of 'raise', 'skip', 'last', 'first' or a callable, received {onerror}"
                    )
        return Calendar(dates)


class Calendar:
    """
    Immutable, sorted set of dates

    Parameters
    ----------
    dates : iterable
        list of datetime objects

    Example
    -------

    .. code-block::

        >>> import datetime
        >>> import doubledate as dtwo

        >>> holidays = [
        ...     datetime.date(2022, 1, 17), 
        ...     datetime.date(2022, 5, 30), 
        ...     datetime.date(2022, 6, 4), 
        ...     datetime.date(2022, 9, 5), 
        ...     datetime.date(2022, 11, 11), 
        ...     datetime.date(2022, 12, 24),
        ...     datetime.date(2022, 12, 26)
        ... ]

        >>> dtwo.Calendar(holidays)
        <doubledate.Calendar at 0x7fd0fa4cfa60>

    Raises
    ------
    TypeError
        if dates is not an iterable of datetime objects
    """

    def __init__(self, dates):
        if not all([isinstance(item, datetime.date) for item in dates]):
            raise TypeError("Calendar expected an iterable of date objects")
        self.__dates__ = sortedcontainers.SortedSet([date for date in dates])
        self.__datemaps__ = {}

    def __hash__(self):
        """
        Returns the hash of the Calendar
        """
        return hash((date for date in self))

    @classmethod
    def generate(cls, starting: datetime.date, ending: datetime.date):
        """
        Creates a new calendar with all the calendar days between the starting
        and ending dates, with both bounds included

        Parameters
        ----------
        starting : datetime.date
            the starting date
        ending : datetime.date
            the ending date
        
        Returns
        -------
        Calendar
            the calendar

        Example
        -------

        .. code-block:: 

            >>> import datetime
            >>> import doubledate as dtwo

            >>> calendar = dtwo.Calendar.generate(
            ...     datetime.date(2021,1,1), 
            ...     datetime.date(2021,12,31)
            ... )
            >>> len(calendar)
            365

            >>> calendar[0]
            datetime.date(2021,1,1)

            >>> calendar[-1]
            datetime.date(2021,12,31)

        """
        if not all(isinstance(d, datetime.date) for d in (starting, ending)):
            raise TypeError("Expected starting and ending dates to be datetime objects")

        return cls(
            [
                starting + datetime.timedelta(days=i)
                for i in range((ending - starting).days + 1)
            ]
        )

    @property
    def last(self) -> datetime.date:
        """
        Returns the last date in the calendar

        Returns
        -------
        datetime.date
            The last date in the calendar

        Raises
        ------
        KeyError
            if the calendar is empty

        See also
        --------
        Calendar.first
            Returns the first date in the calendar
        Calendar.end
            Alias
        """
        return self.__dates__[-1]

    @property
    def end(self) -> datetime.date:
        """
        Returns the last date in the calendar

        Returns
        -------
        datetime.date
            The last date in the calendar

        Raises
        ------
        KeyError
            if the calendar is empty

        See also
        --------
        Calendar.start
            Returns the first date in the calendar
        Calendar.last
            Alias
        """
        return self.last

    @property
    def first(self) -> datetime.date:
        """
        Returns the first date in the calendar

        Returns
        -------
        datetime.date
            The first date in the calendar

        Raises
        ------
        KeyError
            if the calendar is empty

        See also
        --------
        Calendar.start
            alias
        Calendar.last
            Returns the last date in the calendar
        """
        return self.__dates__[0]

    @property
    def start(self) -> datetime.date:
        """
        Returns the first date in the calendar

        Returns
        -------
        datetime.date
            The first date in the calendar

        Raises
        ------
        KeyError
            if the calendar is empty

        See also
        --------
        Calendar.first
            alias
        Calendar.end
            Returns the last date in the calendar
        """
        return self.first

    @property
    def dates(self) -> list:
        """
        Returns the dates as a list

        Returns
        -------
        list
            List of dates
        """
        return list(self.__dates__)

    def __len__(self) -> int:
        """
        Returns the length of the calendar

        Returns
        -------
        int
            Number of days in teh calendar
        """
        return len(self.__dates__)

    def __contains__(self, date) -> bool:
        """
        Returns True if the date is in the calendar

        Returns
        -------
        bool
            True if date is in the calendar
        """
        return date in self.__dates__

    def index(self, date) -> int:
        """
        Returns the index (0-based position) of the date

        Parameters
        ----------
        date : datetime-like
            the date whose index is searched
        
        Raises
        ------
        ValueError
            If date is not in calendar

        Returns
        -------
        int
            Position (0-based) of the date
        """
        return self.__dates__.index(date)

    def __iter__(self):
        """
        Returns the iterator of the dates
        """
        return iter(self.__dates__)

    def __getitem__(self, value):
        """
        Retrieves a date by index or slices a calendar

        If `value` is a slice, the start and stop values can be 
        either integers or datetime.date objects. 

        Returns
        -------
        datetime.date 
            if passed an index
        Calendar
            if passed a slice

        Raises
        ------
        TypeError
            if value is neither an integer nor a slice
        KeyError
            if the index is out of range 
        """
        if isinstance(value, int):
            return self.__dates__.__getitem__(value)
        elif isinstance(value, slice):
            if isinstance(value.start, datetime.date):
                value = slice(self.__dates__.bisect_left(value.start), value.stop)
            if isinstance(value.stop, datetime.date):
                value = slice(value.start, self.__dates__.bisect_right(value.stop))
            return Calendar(self.__dates__.__getitem__(value))
        raise TypeError("Invalid index or slice object")

    def __add__(self, other):
        """
        Alias for union

        Parameter
        ---------
        other : iterable
            An iterable of datetime.date objects

        Returns
        -------
        Calendar
        """
        if isinstance(other, datetime.date):
            return Calendar(self).union(Calendar([other]))
        return Calendar(self).union(Calendar(other))

    def __eq__(self, other):
        """
        Returns True if all dates are in other, and all dates
        of other are in self

        Parameters
        ----------
        other : iterable
            the compared calendar
        
        Returns
        -------
        Calendar
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
        Combines two calendars by combining dates in self and other

        Parameters
        ----------
        others : iterables

        Returns
        -------
        Calendar
            The union of self with others
        """
        return Calendar(self.__dates__.union(*others))

    def difference(self, *others):
        """
        Returns a calendar containing dates in self and 
        not in others
        
        Parameters
        ----------
        others : iterables
            Iterables of datetime.date objects

        Returns
        -------
        Calendar
            The difference of this calendar with others
        """
        return Calendar(self.__dates__.difference(*others))

    def intersection(self, *others):
        """
        Returns a calendar containing dates from self 
        which are also in all the others

        Parameters
        ----------
        others : iterables
            Iterables of datetime.date objects

        Returns
        -------
        Calendar
        """
        return Calendar(self.__dates__.intersection(*others))

    def filter(
        self,
        func=None,
        *,
        year: int = None,
        semester: int = None,
        quarter: int = None,
        month: int = None,
        week: int = None,
        weekday: str = None,
    ):
        """
        Filters and returns a new calendar from this calendar based 
        on a criteria. 

        Allowed criteria are: 
        - either a filtering function (lambda)
        - one or several filtering frequencies as named arguments

        Parameters
        ----------
        func : function, optional
            a filtering function (receives each date as argument)
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

        Returns
        -------
        Calendar

        Example 
        -------
        Filter dates from 3Q 2020
        >>> calendar = Calendar(dates) #assume dates is a list of dates
        >>> calendar.filter(year=2020, quarter=3)

        Filter Mondays
        >>> calendar = Calendar(dates)
        >>> calendar.filter(lambda date: date.weekday() == 0)
        """
        if func is not None:
            if not callable(func):
                raise ValueError(
                    "Filter accepts either a function, one or several named arguments"
                )
            return Calendar([date for date in self.__dates__ if func(date)])
        if all(
            [arg is None for arg in [year, semester, quarter, month, week, weekday]]
        ):
            raise ValueError(
                "You need to provide one of year, semester, quarter, month, week, weekday"
            )
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
        Filters out all the weekends (Saturdays and Sundays)

        Returns
        -------
        Calendar
            Calendar excluding any week-ends (Sat and Sun)

        See also
        --------
        Calendar.weekends
            Filter out all the weekdays
        Calendar.filter
            Filter out days based on a callback
        """
        return self.filter(lambda date: date.weekday() not in [5, 6])

    def weekends(self):
        """
        Filters out all the weekdays (Mon, ..., Fri)

        Returns
        -------
        Calendar
            Calendar excluding any weekdays (Mon, ..., Fri)

        See also
        --------
        Calendar.weekdays
            Filter out all the weekends
        Calendar.filter
            Filter out days based on a callback
        """
        return self.filter(lambda date: date.weekday() in [5, 6])

    def inverse(self, starting: datetime.date = None, ending: datetime.date = None):
        """
        Returns a calendar with all dates between :code:`starting` and :code:`ending`,
        excluding any days in this calendar.

        Parameters
        ----------
        starting : datetime.date
            the starting date of the new calendar (defaults to :code:`calendar[0]`)
        ending : datetime.date 
            the ending date of the new calendar (defaults to :code:`calendar[-1]`)

        Returns
        -------
        Calendar
            Inverse of this calendar

        Example
        -------
        Compute the open weekdays in 2022 from a list of holidays
        
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
        >>> calendar = dtwo.Calendar(holidays).inverse(
        ...    datetime.date(2022,1,1), datetime.date(2022, 12, 31)
        ... ).weekdays()

        """
        if starting is None:
            starting = self[0]

        if ending is None:
            ending = self[-1]

        dates = []
        for i in range((ending - starting).days + 1):
            if starting + datetime.timedelta(i) not in self:
                dates.append(starting + datetime.timedelta(i))
        return Calendar(dates)

    def dayof(self, frequency: str, *, base: int = 1):
        """
        Returns a :code:`datemap` mapping dates to their index 
        in the given frequency.

        The frequency can be one of: 
            - :code:`W` for day of week (assumes week starts on Monday)
            - :code:`W-MON` for day of week (assumes week starts on Monday)
            - :code:`W-TUE` for day of week (assumes week starts on Tuesday)
            - :code:`W-WED` for day of week (assumes week starts on Wednesday)
            - :code:`W-THU` for day of week (assumes week starts on Thursay)
            - :code:`W-FRI` for day of week (assumes week starts on Friday)
            - :code:`W-SAT` for day of week (assumes week starts on Saturday)
            - :code:`W-SUN` for day of week (assumes week starts on Sunday)
            - :code:`M` for day of month
            - :code:`Q` for day of quarter
            - :code:`T` for day of trimester
            - :code:`H` for day of semester (half year)
            - :code:`Y` for day of year

        Parameters
        ----------
        frequency : str
            the frequency

        base : int
            the index of the first day each frequency

        Returns
        -------
        datemap
            The datemap

        Note
        ----
        The default base is 1 

        Note
        ----
        As the Calendar is immutable, the `datemap`
        is cached for efficiency. Repeatedly calling :code:`calendar.dayof("M")`
        should be of complexity 1 after the first call.


        Example
        -------
        >>> calendar = Calendar(dates)
        >>> calendar.dayof("M")[datetime.date(2021,1,3)]
        1
        """
        if ("dayof", frequency, base) not in self.__datemaps__:
            self.__datemaps__[("dayof", frequency, base)] = utils.dayof(
                frequency, calendar=self, base=base
            )
        return self.__datemaps__[("dayof", frequency, base)]

    def daysfrom(self, frequency: str):
        """
        Returns a :code:`datemap` mapping dates to the number of dates since the start
        of the given frequency

        Parameters
        ----------
        frequency : str, 
            the frequency at which to reset the counter
        base : int
            the index of the first day each frequency

        Returns
        -------
        datemap
        """
        if ("daysfrom", frequency) not in self.__datemaps__:
            self.__datemaps__[("daysfrom", frequency)] = utils.daysfrom(
                frequency, calendar=self
            )
        return self.__datemaps__[("daysfrom", frequency)]

    def daysto(self, frequency: str):
        """
        Returns a :code:`datemap` mapping dates to the number of dates to the end
        of the given frequency

        Returns
        -------
        datemap
        """
        if ("daysto", frequency) not in self.__datemaps__:
            self.__datemaps__[("daysto", frequency)] = utils.daysto(
                frequency, calendar=self
            )
        return self.__datemaps__[("daysto", frequency)]

    def daysbetween(
        self, this: datetime.date, that: datetime.date, bounds: str = "left"
    ) -> int:
        """
        Returns the number of open days between two dates

        Parameters
        ----------
        this : datetime.date
            the left-bound of the calendar
        that : datetime.date
            the right-bound of the calenar
        bounds : str, optional
            whether to include this or that in the count
            one of 'both', 'left' (default) or 'right' or None

        Returns 
        --------
        int
            The number of dates between this and that
        """
        if bounds == "both":
            return len(
                self.filter(lambda date: min(this, that) <= date <= max(this, that))
            )
        if bounds == "left":
            return len(
                self.filter(lambda date: min(this, that) <= date < max(this, that))
            )
        if bounds == "right":
            return len(
                self.filter(lambda date: min(this, that) < date <= max(this, that))
            )
        if bounds is None:
            return len(
                self.filter(lambda date: min(this, that) < date < max(this, that))
            )
        raise ValueError(
            f"bounds should be one of 'both', 'left' or 'right', {bounds} given"
        )

    def offset(self, date: datetime.date, days: int) -> datetime.date:
        """
        Returns the date in the calendar offset by n days

        Parameters
        ----------
        date : datetime.date
            the reference date
        days : int
            the offset

        Returns
        -------
        offsetted : datetime.date
            the date in the calendar days-away from the given date
        """
        if not date in self:
            raise ValueError(f"{date} is not in the calendar")
        if self.index(date) + days < 0:
            raise IndexError(f"Out of bounds")
        if self.index(date) + days >= len(self):
            raise IndexError(f"Out of bounds")
        return self[self.index(date) + days]

    def groupby(self, grouper):
        """
        Group dates by the grouper parameter. 

        Allowed values for the grouper: 
            - callable - the callable will receive the date and must return a hashable value
            - frequency criterion - a string representing a frequency 

        Frequency criteria include: 
            - :code:`W`: group by week number each year
            - :code:`M`: group by month each year
            - :code:`Q`: group by quarter each year
            - :code:`H`: group by semester each year
            - :code:`Y`: group by year each year
        
        Parameters
        ----------
        grouper : str, callable
            the criterion to group dates by

        Returns
        -------
        :class:`doubledate.calendar.Collection`
            Collection of calendars    

        Example
        -------
        Group dates by month

        >>> calendar = Calendar(dates)
        >>> calendar.groupby("M")
        <doubledate.Collection at 0x7fd0fa52c2e0>

        Group dates in half months

        >>> calendar = Calendar(dates)
        >>> calendar.groupby(lambda date: (date.year, date.month, date.day < 15))
        <doubledate.Collection at 0x7fd0fa52c2e0>

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
            raise ValueError(
                f"Expected one of 'W', 'M', 'Q', 'H' or 'Y'; '{grouper}' given"
            )

        if callable(grouper):
            calendars = collections.defaultdict(lambda: [])
            for date in self:
                calendars[grouper(date)].append(date)
            return Collection([Calendar(dates) for dates in calendars.values()])

        raise ValueError(f"Expected string or function, received '{grouper}'")

    def resample(self, grouper):
        """
        Alias for :class:`doubledate.Calendar.groupby`
        """
        return self.groupby(grouper)

    def split(
        self,
        on=None,
        side: str = "left",
        starting: datetime.date = None,
        ending: datetime.date = None,
    ):
        """
        Splits the calendar at the given business day, 
        assuming that the passed index is the first (or last) 
        date of each period.

        Parameters
        ----------
        on : BD
            the business day on which to split
        side : {'left','right'}
            whether to start or end each period on the split
        starting : BD
            the business day on which to split (with side :code:`left`)
        ending : BD
            the business day on which to split (with side :code:`right`)

        Returns
        -------
        Collection
            The collection of calendars each starting or ending 
            on the given business day

        Example
        -------
        Split the calendar on the 10th business day each month

        >>> from doubledate import BD
        >>> calendar = Calendar(dates)
        >>> calendar.split(BD(10, "M"))
        <doubledate.Collection at 0x7fd0fa52c2e0>

        Split the calendar on the penultimate day each quarter

        >>> calendar.split(BD(-2, "Y"))
        <doubledate.Collection at 0x7fd0fa52c2e0>

        See also
        --------
        Calendar.groupby
            Split the calendar on a criteria
        
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

        return Collection([Calendar(calendar) for calendar in calendars.values()])

    def fa(self, date: datetime.date, default=constants.RAISE) -> datetime.date:
        """
        Returns the first date strictly after ("first-after", or "fa")

        Parameters
        ----------
        date : datetime.date
            the date from which to compute the first date strictly after in the calendar
        default : optional
            the default value if the given date is on or after the last date in the calendar
            if no default value is given, it will raise an KeyError

        Returns
        -------
        datetime.date
            The first date strictly after the given date

        See also
        --------
        Calendar.lb
            Return the last date before
        """
        if date > self.__dates__[-1]:
            if default == constants.RAISE:
                raise KeyError(
                    f"Out-of-range error: {date} is after last date in the calendar"
                )
            return default
        return self.__dates__[self.__dates__.bisect_right(date)]

    def lb(self, date: datetime.date, default=constants.RAISE) -> datetime.date:
        """
        Returns the most recent date strictly before ("last-before", or "lb")

        Parameters
        ----------
        date : datetime.date
            the lookup date

        default: optional
            default value if the given date is strictly before the first date in the calendar

        Returns
        -------
        datetime.date
            the most recent date strictly before date

        See also
        --------
        Calendar.fa
            Returns the first date after
        Calendar.asof
            Returns the most recent date on or before (after) another date
        """
        if date < self.__dates__[0]:
            if default == constants.RAISE:
                raise KeyError(
                    f"Out-of-range error: {date} is before the first date in the calendar"
                )
            return default
        return self.__dates__[self.__dates__.bisect_left(date) - 1]

    def asof(
        self, date: datetime.date, side: str = "left", default=constants.RAISE
    ) -> datetime.date:
        """
        Returns the date if the date is in the calendar, or 
        the last (first) date before (after) that

        Parameters
        ----------
        date : datetime.date
            the lookup date
        side : 'left', 'right'
            direction to search if date is not in calendar
        default: optional
            default value if the given date is strictly before (after) 
            the first (last) date in the calendar

        Returns
        -------
        datetime.date
            the last (first) date on or before (after) date

        Raises
        ------
        KeyError
            if date is before (after) the first (last) date
            in the calendar, and no default is provided

        Example
        -------
        
        .. code-block::

            >>> import datetime

            >>> calendar = Calendar([
            ...     datetime.date(2020, 1, 20),
            ...     datetime.date(2020, 4, 28)
            ... ])

            >>> calendar.asof(datetime.date(2020, 1, 20))
            datetime.date(2020, 1, 20)

            >>> calendar.asof(datetime.date(2020, 2, 15))
            datetime.date(2020, 1, 20)

            >>> calendar.asof(datetime.date(2020, 2, 15), side="right")
            datetime.date(2020, 4, 28)

            >>> calendar.asof(datetime.date(2020, 1, 1))
            KeyError("Out-of-range error: 2020-01-01 is before first date in the calendar")

            >>> calendar.asof(datetime.date(2020, 1, 1), default=None)
            None

        See also
        --------
        Calendar.lb
            last date strictly before 
        Calendar.fa
            first date strictly after
        
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
        Combines this calendar with other, such as: 
            - Dates in both calendars are kept
            - Dates in this calendar but not in other are either dropped or
              replaced with either the first previous or following date in other

        Parameters
        ------------
        other : iterable
            other calendar
        
        fallback : str
            one of 'drop', 'previous' (a.k.a. ffill), 'next' (a.k.a. bfill)

        Returns
        -------
        Calendar
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
        If all mapped values are datetime.date objects, function returns a new calendar
        Else it returns a new list

        Parameters
        ----------
        func : callable
            callback function

        Returns
        ------------
        mapped : Calendar | List
            the mapped values
        """
        if not callable(func):
            raise ValueError("Expected func to be a callable function")
        mapped = [func(date) for date in self]
        if all([isinstance(m, datetime.date) for m in mapped]):
            return Calendar(mapped)
        return mapped

    def som(self, date: datetime.date) -> datetime.date:
        """
        Return the first open day of the month given the date

        Parameters
        ----------
        date : datetime.date
            the date from which to compute the start of the month

        Returns
        -------
        datetime.date
        """
        for i in range(self.index(date), -1, -1):
            if (
                self.__dates__[i].month == date.month
                and self.__dates__[i].year == date.year
            ):
                continue
            return self.__dates__[i + 1]
        return self.__dates__[i]

    def eom(self, date: datetime.date) -> datetime.date:
        """
        Return the last open day of the month given the date

        Parameters
        ----------
        date : datetime.date
            the date from which to compute the end of the month

        Returns
        -------
        datetime.date
        """
        for i in range(self.index(date), len(self)):
            if (
                self.__dates__[i].month == date.month
                and self.__dates__[i].year == date.year
            ):
                continue
            return self.__dates__[i - 1]
        return self.__dates__[i]

    def soq(self, date: datetime.date) -> datetime.date:
        """
        Returns the first open day of the quarter given the date

        Parameters
        ----------
        date : datetime.date
            the date from which to compute the start of the quarter

        Returns
        -------
        datetime.date
        """
        for i in range(self.index(date), -1, -1):
            if (
                utils.quarter(self.__dates__[i]) == utils.quarter(date)
                and self.__dates__[i].year == date.year
            ):
                continue
            return self.__dates__[i + 1]
        return self.__dates__[i]

    def eoq(self, date: datetime.date) -> datetime.date:
        """
        Returns the last open date of the quarter

        Parameters
        ----------
        date : datetime.date
            the date from which to compute the end of quarter

        Returns
        -------
        datetime.date
        """
        for i in range(self.index(date), len(self)):
            if (
                utils.quarter(self.__dates__[i]) == utils.quarter(date)
                and self.__dates__[i].year == date.year
            ):
                continue
            return self.__dates__[i - 1]
        return self.__dates__[i]

    def sot(self, date: datetime.date) -> datetime.date:
        """
        Returns the first open day of the trimester given the date

        Parameters
        ----------
        date : datetime.date
            the date from which to compute the start of trimester

        Returns
        -------
        datetime.date
        """
        for i in range(self.index(date), -1, -1):
            if (
                utils.trimester(self.__dates__[i]) == utils.trimester(date)
                and self.__dates__[i].year == date.year
            ):
                continue
            return self.__dates__[i + 1]
        return self.__dates__[i]

    def eot(self, date: datetime.date) -> datetime.date:
        """
        Returns the last open date of the trimester

        Parameters
        ----------
        date : datetime.date
            the date from which to compute the end of trimester

        Returns
        -------
        datetime.date
        """
        for i in range(self.index(date), len(self)):
            if (
                utils.trimester(self.__dates__[i]) == utils.trimester(date)
                and self.__dates__[i].year == date.year
            ):
                continue
            return self.__dates__[i - 1]
        return self.__dates__[i]

    def sos(self, date: datetime.date) -> datetime.date:
        """
        Returns the first open day of the semester given the date

        Parameters
        ----------
        date : datetime.date
            the date from which to compute the start of semester

        Returns
        -------
        datetime.date
        """
        for i in range(self.index(date), -1, -1):
            if (
                utils.semester(self.__dates__[i]) == utils.semester(date)
                and self.__dates__[i].year == date.year
            ):
                continue
            return self.__dates__[i + 1]
        return self.__dates__[i]

    def eos(self, date: datetime.date) -> datetime.date:
        """
        Returns the last open date of the semester

        Parameters
        ----------
        date : datetime.date
            the date from which to compute the end of semester

        Returns
        -------
        datetime.date
        """
        for i in range(self.index(date), len(self)):
            if (
                utils.semester(self.__dates__[i]) == utils.semester(date)
                and self.__dates__[i].year == date.year
            ):
                continue
            return self.__dates__[i - 1]
        return self.__dates__[i]

    def soy(self, date: datetime.date) -> datetime.date:
        """
        Return the first open day of the year given the date

        Parameters
        ----------
        date : datetime.date
            the date from which to compute the start of year

        Returns
        -------
        datetime.date
        """
        for i in range(self.index(date), -1, -1):
            if self.__dates__[i].year == date.year:
                continue
            return self.__dates__[i + 1]
        return self.__dates__[i]

    def eoy(self, date: datetime.date) -> datetime.date:
        """
        Returns the last open date of the year

        Parameters
        ----------
        date : datetime.date
            the date from which to compute the end of year

        Returns
        -------
        datetime.date
        """
        for i in range(self.index(date), len(self)):
            if self.__dates__[i].year == date.year:
                continue
            return self.__dates__[i - 1]
        return self.__dates__[i]


class Collection:
    """
    Collection of calendars. 

    Collections are normally generated from splitting a Calendar in several periods 
    via resampling or grouping

    Example
    -------
    .. code-block::

        >>> import datetime
        >>> import doubledate as dtwo

        >>> holidays = [
        ...     datetime.date(2022, 1, 17), 
        ...     datetime.date(2022, 5, 30), 
        ...     datetime.date(2022, 6, 4), 
        ...     datetime.date(2022, 9, 5), 
        ...     datetime.date(2022, 11, 11), 
        ...     datetime.date(2022, 12, 24),
        ...     datetime.date(2022, 12, 26)
        ... ]

        >>> calendar = dtwo.Calendar(holidays).inverse().weekdays()
        >>> calendar
        <doubledate.Calendar>

        >>> calendar.resample("M") #split the calendar by month
        <doubledate.Collection>

        >>> calendar.resample("M").nth(10, base=1) #get the 10th business day each month
        <doubledate.Calendar>

    """

    def __init__(self, calendars):
        """
        Parameters
        ----------
        calendars : iterable
            list of Calendar instances
        """
        if not all([isinstance(calendar, Calendar) for calendar in calendars]):
            raise TypeError("Expected a list of calendar objects")
        self.calendars = list(calendars)

    def first(self, onerror="raise") -> Calendar:
        """
        Returns a calendar with the first date each period in the collection

        Allowed values for the onerror parameter: 
            - 'skip' to skip empty calendars
            - 'raise' to raise an error

        Parameters
        ----------
        onerror : str
            handling policy for empty calendars

        Returns
        -------
        Calendar
        """
        return self.apply(lambda period: period[0], onerror=onerror).combine()

    def last(self, onerror="raise") -> Calendar:
        """
        Returns a calendar with the last date each period in the collection

        Allowed values for the onerror parameter: 
            - 'skip' to skip empty calendars
            - 'raise' to raise an error

        Parameters
        ----------
        onerror : str
            handling policy for empty calendars

        Returns
        -------
        Calendar
        """
        return self.apply(lambda period: period[-1], onerror=onerror).combine()

    def nth(self, index, *, base=0, onerror="raise") -> Calendar:
        """
        Returns a calendar with the nth date each period from the collection
        
        Allowed values for the onerror parameter: 
            - 'skip' to skip periods where the n'th business day is not defined
            - 'first' to fallback to the first date in the period when the n'th 
              business day is not defined
            - 'last' to fallback to the last date in the period when the n'th 
              business day is not defined
            - 'raise' to raise an error if the n'th business day is not defined

        Parameters
        ----------
        index : int, slice
            the index or range of indices
        base : 0, 1
            whether indices are 0 or 1 based
        onerror : str
            handling policy for periods the n'th business day is not defined

        Returns
        -------
        Calendar
        """
        if isinstance(index, slice):
            if isinstance(index.start, int):
                index = slice(index.start - base, index.stop, index.step)
            if isinstance(index.stop, int):
                index = slice(index.start, index.stop - base, index.step)
            return self.apply(
                lambda calendar: calendar[index], onerror=onerror
            ).combine()

        return self.apply(
            lambda period: period[index - base], onerror=onerror
        ).combine()

    def __getitem__(self, value) -> Calendar:
        """
        Slices or indexes each calendar, combining the result

        Returns
        -------
        Calendar

        Note
        ----
        Indices and slices thereof are assumed 0-based
        """
        return self.apply(lambda calendar: calendar[value], onerror="raise").combine()

    def index(self, value) -> int:
        """
        Returns the 0-based index of the calendar, 
        or 0-based index of the calendar containing the date

        Returns
        -------
        int
        """
        if isinstance(value, datetime.date):
            for i, calendar in enumerate(self.calendars):
                if value in calendar:
                    return i
            raise IndexError(f"{value} is not in any of the calendars")

        if isinstance(value, Calendar):
            return self.calendars.index(value)

        raise ValueError(
            f"Expected value to be datetime.date or Calendar, received {type(value).__name__}"
        )

    def __contains__(self, value) -> bool:
        """
        Returns True if one of the calendars contains the given date

        Returns
        -------
        bool
        """
        if isinstance(value, Calendar):
            return value in self.calendars

        if isinstance(value, datetime.date):
            for calendar in self.calendars:
                if value in calendar:
                    return True
            return False

        raise ValueError(
            f"Expected value to be datetime.date or Calendar, received {type(value).__name__}"
        )

    def apply(self, func, onerror="raise"):
        """
        Applies a function to each calendar

        Returns
        -------
        Collection
        """
        if not callable(func):
            raise ValueError("Expected func to be a callable function")

        dates = []
        for calendar in self.calendars:
            try:
                dates.append(func(calendar))
            except Exception as e:
                if onerror == "raise":
                    raise e
                elif onerror == "skip" or onerror == "drop":
                    pass
                elif onerror == "first":
                    dates.append(calendar[0])
                elif onerror == "last":
                    dates.append(calendar[-1])
                elif callable(onerror):
                    dates.append(onerror(calendar))
                else:
                    raise ValueError(
                        "Expected onerror to be one of 'raise', 'first', 'last' or callable"
                    )

        for i, value in enumerate(dates):
            if isinstance(value, datetime.date):
                dates[i] = Calendar([value])
            elif isinstance(value, (list, tuple)):
                dates[i] = Calendar(value)
            elif isinstance(value, Calendar):
                pass
            else:
                raise ValueError(
                    "mapped values must be a datetime, a list thereof or a Calendar"
                )

        return Collection(dates)

    def combine(self):
        """
        Combines the calendars of the collection back into a 
        single Calendar object

        Returns
        -------
        Calendar
        """
        return Calendar([]).union(*self.calendars)

    def filter(self, func):
        """
        Filters out calendars from the collection

        Parameters
        ----------
        func : callable
            filtering function

        Returns
        -------
        Collection
        """
        if not callable(func):
            raise ValueError("Expected func to be a callable function")
        return Collection([cal for cal in self.calendars if func(cal)])

    def __len__(self):
        """
        Returns the number of calendars

        Returns
        -------
        int
        """
        return len(self.calendars)

    def __iter__(self):
        """
        Iterate over each calendar in the collection
        """
        return iter(self.calendars)
