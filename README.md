[![Documentation Status](https://readthedocs.org/projects/doubledate/badge/?version=latest)](https://doubledate.readthedocs.io/en/latest/?badge=latest)

# doubledate
Managing irregular calendars isn't hard per-se, but it can be painful, especially in the context of trading calendars and backtesting. That is why doubledate exposes a nifty `Calendar` class to work with custom calendars.

## Installation
The best - and easiest - way to install `doubledate` is by calling:
```python
pip install doubledate 
```

## Usage
```python
import datetime
from doubledate import Calendar, utils

#every day in 2019
#you can load up your own dates from a backend, API, file...
calendar = Calendar([datetime.date(2019,1,1) + datetime.timedelta(i) for i in range(365)])

#weekends
weekends = calendar.weekends()

#week days
weekdays = calendar.weekdays()

#first and last date
weekdays.first(), weekdays.last()

#or index
weekdays[0], weekdays[-1]

#slice the calendar
#like normal lists, the Calendar is 0-based, such that slice(10:20) returns the 11th to 20th dates
weekdays[10:20]

#or with a date-like object
#this will be inclusive of the bounds, if they are in the calendar
s2 = weekdays[datetime.date(2019,7,1):datetime.date(2019,12,31)]

#10th weekday each month
b10 = weekdays.groupby("month").apply(lambda cal: cal[10])

#5th to 10th weekday each month
b5to10 = weekdays.groupby("month").apply(lambda cal: cal[5:10])

#lets retrieve holidays from somewhere (API, file...)
holidays = [
    datetime.date(2019, 1, 1), datetime.date(2019, 1, 21), 
    datetime.date(2019, 2, 18), datetime.date(2019, 5, 27),
    datetime.date(2019, 7, 4), datetime.date(2019, 9, 2), 
    datetime.date(2019, 10, 14), datetime.date(2019, 11, 11), 
    datetime.date(2019, 11, 28), datetime.date(2019, 12, 25)
]

#because the calendar class is a sorted set, you have set methods like union, intersection and difference
#business days
workdays = weekdays.difference(holidays)

#... alternatively
workdays = holidays.inverse(datetime.date(2019, 1, 1), datetime.date(2019, 12, 31)).weekdays()

#non-weekend holidays
offdays = weekdays.union(holidays)

#is my birthday a weekday?
datetime.date(2019, 6, 17) in weekdays
>> True

#slicing is inclusive of the two bounds... summer workdays
summer = workdays[datetime.date(2019,6,21):datetime.date(2019,9,20)]

#index of given date in given frequency
workdays.dayof(datetime.date(2019,8,14), "month")
>> 8

#a few utilities
utils.isleap(2016), utils.isleap(datetime.date(2019,6,17))
>> True, False

#end of month
utils.eom(datetime.date(2016,2,14), 0), utils.eom(datetime.date(2016,2,14), -1)
>> datetime.date(2019, 2, 29), datetime.date(2019, 1, 31)

#... number of work days to new Year's eve
#week end, month end, quarter end, semester end or year end... simply ask for it!
workdays.daysto(to="year end", asof=datetime.date(2019, 11, 15))
>> 45
```

## About doubledate
This package is named after the doubledate calendar, which was itself named after Pope Gregory XIII who introduced it as a correction to the Julian calendar in 1582.
