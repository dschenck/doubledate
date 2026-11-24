import datetime
import re
from typing import Any, TypeVar, overload
from collections.abc import Callable

from . import constants

D = TypeVar("D", bound=datetime.date)

DAYCOUNTBYMONTH = {
    1: 31,
    2: 29,
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31,
}


class diem:
    """
    Abstract date without year (e.g. 17 June).

    Parameters
    ----------
    month : 1..12
        the month
    day : 1..31
        the day
    fold : 'back', 'forward'
        how to treat 29 Feb

    Note
    ----
    The fold argument determines how to resolve 29 February
    for years which are not leap years
    """

    def __init__(self, month: int, day: int, *, fold: str = "back") -> None:
        if not isinstance(month, int):
            raise TypeError("Expected month to be an integer")

        if month < 1 or month > 12:
            raise ValueError("month must be in 1..12")

        self.month = month

        if not isinstance(day, int):
            raise TypeError("Expected day to be an integer")

        if day < 1 or day > DAYCOUNTBYMONTH[month]:
            raise ValueError(f"day must be in 1..{DAYCOUNTBYMONTH[month]}")

        self.day = day

        if fold not in ("forward", "back"):
            raise ValueError(f"fold must be one of 'back' or 'forward', '{fold}' given")

        self.fold = fold

    @overload
    def resolve(self, year: int, *, fold: str | None = ...) -> datetime.date: ...

    @overload
    def resolve(
        self,
        year: int,
        *,
        fold: str | None = ...,
        dtype: Callable[[int, int, int], D],
    ) -> D: ...

    def resolve(
        self,
        year: int,
        *,
        fold: str | None = None,
        dtype: Callable[[int, int, int], Any] = datetime.date,
    ) -> Any:
        """
        Convert diem to actual datetime.date.

        Parameters
        ----------
        year : int
            the year of the date
        fold : 'back', 'forward', None (default)
            how to treat 29 Feb
        dtype : type
            the datetime type to instantiate (default is `datetime.date`)

        Returns
        -------
        date
            an instance of the dtype with the (year, month, day)

        Note
        ----
        If given, the `fold` argument overrides the fold attribute of the diem

        Examples
        --------
        >>> diem(2, 29).resolve(2020)
        datetime.date(2020, 2, 29)

        >>> diem(2, 29).resolve(2021) # default fold is 'back'
        datetime.date(2021, 2, 28)

        >>> diem(2, 29).resolve(2021, fold="forward")
        datetime.date(2021, 3, 1)

        >>> diem(2, 29, fold="forward").resolve(2021) # set default fold
        datetime.date(2021, 3, 1)

        >>> diem(2, 29, fold="forward").resolve(2021, fold="back") # override default fold
        datetime.date(2021, 2, 28)
        """
        try:
            return dtype(year, self.month, self.day)

        except ValueError:
            if not isinstance(year, int):
                raise TypeError(f"Expected year to be an integer, received {year}")

            if fold not in ("back", "forward", None):
                raise ValueError(
                    f"Expected fold to be one of 'back', 'forward' or None, received {fold}"
                )

            if fold is None:
                fold = self.fold

            if fold == "back":
                return dtype(year, 2, 28)

            return dtype(year, 3, 1)  # fold == "forward"

    def __str__(self) -> str:
        """
        Represent a diem in ISO 8601 format (--MM-DD).
        """
        return f"--{self.month:02d}-{self.day:02d}"

    def __repr__(self) -> str:
        """
        Return repr(self)
        """
        return f'doubledate.diem({self.month}, {self.day}, fold="{self.fold}")'

    def __eq__(self, other: object) -> bool:
        """
        Return self == other.
        """
        if not isinstance(other, diem):
            return False
        return (self.month, self.day, self.fold) == (other.month, other.day, other.fold)

    def __ne__(self, other: object) -> bool:
        """
        Return self != other.
        """
        if not isinstance(other, diem):
            return True
        return (self.month, self.day, self.fold) != (other.month, other.day, other.fold)

    def __hash__(self) -> int:
        """
        Return hash(self).
        """
        return hash((self.month, self.day, self.fold))

    def __lt__(self, other: object) -> bool:
        """
        Return self < other.
        """
        if not isinstance(other, diem):
            raise TypeError(
                f"'<' not supported between instances of 'doubledate.diem' and '{type(other).__name__}'"
            )
        return (self.month, self.day) < (other.month, other.day)

    def __le__(self, other: object) -> bool:
        """
        Return self <= other.
        """
        if not isinstance(other, diem):
            raise TypeError(
                f"'<=' not supported between instances of 'doubledate.diem' and '{type(other).__name__}'"
            )
        return (self.month, self.day) <= (other.month, other.day)

    def __gt__(self, other: object) -> bool:
        """
        Return self > other.
        """
        if not isinstance(other, diem):
            raise TypeError(
                f"'>' not supported between instances of 'doubledate.diem' and '{type(other).__name__}'"
            )
        return (self.month, self.day) > (other.month, other.day)

    def __ge__(self, other: object) -> bool:
        """
        Return self >= other.
        """
        if not isinstance(other, diem):
            raise TypeError(
                f"'>=' not supported between instances of 'doubledate.diem' and '{type(other).__name__}'"
            )
        return (self.month, self.day) >= (other.month, other.day)

    @staticmethod
    def parse(value: str | datetime.date) -> "diem":
        """
        Parse an input (str, datetime) as a diem.

        Parameters
        ----------
        value : str, datetime
            input to parse as diem

        Returns
        -------
        diem
            parsed input

        Examples
        --------
        >>> diem.parse("Jan")
        doubledate.diem(1, 31, fold="back")

        >>> diem.parse("Feb")
        doubledate.diem(2, 29, fold="back")

        >>> diem.parse("Jun-17")
        doubledate.diem(6, 17, fold="back")

        >>> diem.parse(datetime.datetime(2020,4,28))
        doubledate.diem(4, 28, fold="back")
        """
        if isinstance(value, datetime.date):
            return diem(value.month, value.day)

        if isinstance(value, str):
            if value.upper() in constants.MONTHS:
                index = constants.MONTHS[value.upper()]
                return diem(index, DAYCOUNTBYMONTH[index])

            match = re.search(r"--(\d{1,2})-(\d{1,2})", value)
            if match:
                month, day = match.groups()
                return diem(int(month), int(day))

            match = re.search(
                r"(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)-?(\d{1,2})",
                value,
                re.IGNORECASE,
            )
            if match:
                name, day = match.groups()
                return diem(constants.MONTHS[name.upper()], int(day))

        raise ValueError(f"Could not parse '{value}' ({type(value).__name__})")

    def lb(self, date: D) -> D:
        """
        Resolve the diem to the most recent date strictly before the given date.

        Parameters
        ----------
        date : datetime.date

        Returns
        -------
        datetime.date

        Examples
        --------
        >>> diem(3, 31).lb(datetime.date(2020,2,14))
        datetime.date(2019, 3, 31)

        >>> diem(3, 31).lb(datetime.date(2020, 6, 1))
        datetime.date(2020, 3, 31)
        """
        if (self.month, self.day) < (date.month, date.day):
            return self.resolve(date.year, dtype=type(date))
        return self.resolve(date.year - 1, dtype=type(date))

    def fa(self, date: D) -> D:
        """
        Resolve the diem to the first date strictly after the given date.

        Parameters
        ----------
        date : datetime.date

        Returns
        -------
        datetime.date

        Examples
        --------
        >>> diem(3, 31).fa(datetime.date(2020,2,14))
        datetime.date(2020, 3, 31)

        >>> diem(3, 31).fa(datetime.date(2020, 6, 1))
        datetime.date(2021, 3, 31)

        Note
        ----
        If the diem is `29 Feb`, the `diem.fa` will resolve based
        on the fold attribute (e.g. back to 28 Feb or forward to 1 Mar)
        """
        if (self.month, self.day) > (date.month, date.day):
            return self.resolve(date.year, dtype=type(date))
        return self.resolve(date.year + 1, dtype=type(date))

    def asof(self, date: D, side: str = "left") -> D:
        """
        Resolve the diem to the most recent date on or before (after) the given date.

        Parameters
        ----------
        date : datetime.date
            the date from which to compute the target date
        side : 'left', 'right'
            whether to resolve to the most recent (left) or the first date after (right)
            the given date

        Examples
        --------
        >>> diem(3, 31).asof(datetime.date(2020, 2, 28))
        datetime.date(2019, 3, 31)
        """
        if (date.month, date.day) == (self.month, self.day):
            return date
        if side == "left":
            return self.lb(date)
        if side == "right":
            return self.fa(date)
        raise ValueError(f"side should be one of 'left' or 'right', {side} given")

    def replace(
        self,
        *,
        month: int | None = None,
        day: int | None = None,
        fold: str | None = None,
    ) -> "diem":
        """
        Return a copy of the diem, partially replacing some of the attributes.

        Parameters
        ----------
        month : 1..12
            the month
        day : 1..31
            the day
        fold : 'back', 'forward'
            how to treat 29 Feb
        """
        return diem(month or self.month, day or self.day, fold=fold or self.fold)
