import unittest
import datetime
import os
import pandas as pd

import doubledate.utils as utils
import doubledate.internals as internals

from doubledate import Calendar

def load():
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "calendar.CSV"), "r") as f: 
        return Calendar([datetime.datetime.strptime(date, "%Y-%m-%d").date()
            for date in f.read().strip().split("\n")])

class TestUtils(unittest.TestCase):

    def test_semester(self):
        dates = [
            datetime.date(2019, 1, 1), datetime.date(2019, 6, 30), 
            datetime.date(2019, 7, 1), datetime.date(2019, 12, 31)
        ]
        self.assertEqual([utils.semester(date) for date in dates], [1,1,2,2])

    def test_trimester(self):
        dates = [
            datetime.date(2019, 1, 1), datetime.date(2019, 6, 30), 
            datetime.date(2019, 7, 1), datetime.date(2019, 12, 31)
        ]
        self.assertEqual([utils.trimester(date) for date in dates], [1,2,2,3])

    def test_quarter(self):
        dates = [
            datetime.date(2019, 1, 1), datetime.date(2019, 6, 30), 
            datetime.date(2019, 7, 1), datetime.date(2019, 12, 31)
        ]
        self.assertEqual([utils.quarter(date) for date in dates], [1,2,3,4])

    def test_eow(self):
        self.assertEqual(
            utils.eow(datetime.date(2020, 1, 4)),
            datetime.date(2020, 1, 5)
        )
        self.assertEqual(
            utils.eow(datetime.date(2020, 1, 4), 0),
            datetime.date(2020, 1, 5)
        )
        self.assertEqual(
            utils.eow(datetime.date(2020, 1, 4), 0, "SUN"),
            datetime.date(2020, 1, 5)
        )
        self.assertEqual(
            utils.eow(datetime.date(2020, 1, 4), 1, "SUN"),
            datetime.date(2020, 1, 12)
        )
        self.assertEqual(
            utils.eow(datetime.date(2020, 1, 4), -1, "SUN"),
            datetime.date(2019, 12, 29)
        )
        self.assertEqual(
            utils.eow(datetime.date(2020, 1, 4), 0, "SAT"),
            datetime.date(2020, 1, 4)
        )
        self.assertEqual(
            utils.eow(datetime.date(2020, 1, 4), 0, "FRI"),
            datetime.date(2020, 1, 10)
        )
        self.assertEqual(
            utils.eow(datetime.date(2020, 1, 4), 0, "THU"),
            datetime.date(2020, 1, 9)
        )
        self.assertEqual(
            utils.eow(datetime.date(2020, 1, 4), 0, "WED"),
            datetime.date(2020, 1, 8)
        )
        self.assertEqual(
            utils.eow(datetime.date(2020, 1, 4), 0, "TUE"),
            datetime.date(2020, 1, 7)
        )
        self.assertEqual(
            utils.eow(datetime.date(2020, 1, 4), 0, "MON"),
            datetime.date(2020, 1, 6)
        )

    def test_sow(self): 
        self.assertEqual(
            utils.sow(datetime.date(2020, 1, 4)),
            datetime.date(2019, 12, 30)
        )
        self.assertEqual(
            utils.sow(datetime.date(2020, 1, 4), 0),
            datetime.date(2019, 12, 30)
        )
        self.assertEqual(
            utils.sow(datetime.date(2020, 1, 4), 0, "SUN"),
            datetime.date(2019, 12, 29)
        )
        self.assertEqual(
            utils.sow(datetime.date(2020, 1, 4), 0, "SAT"),
            datetime.date(2020, 1, 4)
        )
        self.assertEqual(
            utils.sow(datetime.date(2020, 1, 4), 0, "FRI"),
            datetime.date(2020, 1, 3)
        )
        self.assertEqual(
            utils.sow(datetime.date(2020, 1, 4), 0, "THU"),
            datetime.date(2020, 1, 2)
        )
        self.assertEqual(
            utils.sow(datetime.date(2020, 1, 4), 0, "WED"),
            datetime.date(2020, 1, 1)
        )
        self.assertEqual(
            utils.sow(datetime.date(2020, 1, 4), 0, "TUE"),
            datetime.date(2019, 12, 31)
        )
        self.assertEqual(
            utils.sow(datetime.date(2020, 1, 4), 0, "MON"),
            datetime.date(2019, 12, 30)
        )

    def test_eom(self):
        self.assertEqual(
            utils.eom(datetime.date(2019,6,17)), 
            datetime.date(2019,6,30))

        self.assertEqual(
            utils.eom(datetime.date(2019,6,17), 0), 
            datetime.date(2019,6,30))

        self.assertEqual(
            utils.eom(datetime.date(2019,6,17), 1), 
            datetime.date(2019,7,31))

        self.assertEqual(
            utils.eom(datetime.date(2019,6,17), -1), 
            datetime.date(2019,5,31))

        self.assertEqual(
            utils.eom(datetime.date(2016, 2, 29), 0), 
            datetime.date(2016, 2, 29)
        )

        self.assertEqual(
            utils.eom(datetime.date(2016, 2, 29), 12), 
            datetime.date(2017, 2, 28)
        )

    def test_som(self):
        self.assertEqual(
            utils.som(datetime.date(2019,6,17)), 
            datetime.date(2019,6,1)
        )

        self.assertEqual(
            utils.som(datetime.date(2016,3,15), -1),
            datetime.date(2016,2,1)
        )

        self.assertEqual(
            utils.som(datetime.date(2015,4,20),1),
            datetime.date(2015, 5,1)
        )

    def test_soq(self):
        self.assertEqual(
            utils.soq(datetime.date(2020,1,4)), 
            datetime.date(2020, 1, 1)
        )
        self.assertEqual(
            utils.soq(datetime.date(2020, 3, 31)), 
            datetime.date(2020, 1, 1)
        )
        self.assertEqual(
            utils.soq(datetime.date(2020,2,4), 0), 
            datetime.date(2020, 1, 1)
        )
        self.assertEqual(
            utils.soq(datetime.date(2020,2,4), 1), 
            datetime.date(2020, 4, 1)
        )
        self.assertEqual(
            utils.soq(datetime.date(2020,2,4), -1), 
            datetime.date(2019, 10, 1)
        )

    def test_eoq(self):
        self.assertEqual(
            utils.eoq(datetime.date(2020,1,4)), 
            datetime.date(2020, 3, 31)
        )
        self.assertEqual(
            utils.eoq(datetime.date(2020, 3, 31)), 
            datetime.date(2020, 3, 31)
        )
        self.assertEqual(
            utils.eoq(datetime.date(2020,1,4), 0), 
            datetime.date(2020, 3, 31)
        )
        self.assertEqual(
            utils.eoq(datetime.date(2020,1,4), 1), 
            datetime.date(2020, 6, 30)
        )
        self.assertEqual(
            utils.eoq(datetime.date(2020,1,4), -1), 
            datetime.date(2019, 12, 31)
        )

    def test_sos(self):
        self.assertEqual(
            utils.sos(datetime.date(2019,11,4)), 
            datetime.date(2019,7,1)
        )
        self.assertEqual(
            utils.sos(datetime.date(2019,11,4), 0), 
            datetime.date(2019,7,1)
        )
        self.assertEqual(
            utils.sos(datetime.date(2019,11,4), 1),
            datetime.date(2020,1,1)
        )
        self.assertEqual(
            utils.sos(datetime.date(2019,11,4), -1),
            datetime.date(2019,1,1)
        )

    def test_eos(self):
        self.assertEqual(
            utils.eos(datetime.date(2019,11,4)), 
            datetime.date(2019,12,31)
        )
        self.assertEqual(
            utils.eos(datetime.date(2019,11,4), 0), 
            datetime.date(2019,12,31)
        )
        self.assertEqual(
            utils.eos(datetime.date(2019,11,4), 1),
            datetime.date(2020,6,30)
        )
        self.assertEqual(
            utils.eos(datetime.date(2019,11,4), -1),
            datetime.date(2019,6,30)
        )

    def test_eoy(self):
        self.assertEqual(
            utils.eoy(datetime.date(2019,11,4)), 
            datetime.date(2019,12,31)
        )
        self.assertEqual(
            utils.eoy(datetime.date(2019,11,4), 0), 
            datetime.date(2019,12,31)
        )
        self.assertEqual(
            utils.eoy(datetime.date(2019,11,4), 1),
            datetime.date(2020,12,31)
        )
        self.assertEqual(
            utils.eoy(datetime.date(2019,11,4), -1),
            datetime.date(2018,12,31)
        )

    def test_isdatelike(self):
        self.assertTrue(internals.isdatelike(datetime.date.today()))
        self.assertTrue(internals.isdatelike(datetime.datetime.now()))
        self.assertTrue(internals.isdatelike(pd.Timestamp("2016-05-19")))

    def test_parse(self):
        self.assertTrue(
            utils.parse("05/03/2019"),
            datetime.date(2019, 5, 3)
        )

    def test_offset(self):
        today = datetime.date(2020, 1, 10) #Friday
        
        #by days
        self.assertEqual(utils.offset(today, days=+1), datetime.date(2020, 1, 11))
        self.assertEqual(utils.offset(today, days=-1), datetime.date(2020, 1, 9))

        #by weekdays
        self.assertEqual(utils.offset(today, weekdays=+1), datetime.date(2020, 1, 13)) #Monday
        self.assertEqual(utils.offset(today, weekdays=-1), datetime.date(2020, 1, 9))  #Thursday

        #by weeks
        self.assertEqual(utils.offset(today, weeks=+1), datetime.date(2020, 1, 17))
        self.assertEqual(utils.offset(today, weeks=-1), datetime.date(2020, 1, 3))

        #by months
        self.assertEqual(utils.offset(today, months=+1), datetime.date(2020, 2, 10))
        self.assertEqual(utils.offset(today, months=-1), datetime.date(2019, 12, 10))

        self.assertEqual(
            utils.offset(datetime.date(2020,1,31), months=+1), 
            datetime.date(2020, 2, 29)) #2020 is a leap year

        self.assertEqual(
            utils.offset(datetime.date(2020,1,31), months=+1, handle=0), 
            datetime.date(2020, 2, 29)) #2020 is a leap year

        self.assertEqual(
            utils.offset(datetime.date(2020,1,31), months=+1, handle=1), 
            datetime.date(2020, 3, 1)) #2020 is a leap year

        self.assertEqual(
            utils.offset(datetime.date(2019,1,31), months=+1, handle=1), 
            datetime.date(2019, 3, 1)) #2019 is not a leap year

        self.assertEqual(
            utils.offset(datetime.date(2020,1,31), months=+1, handle=lambda eom, days: 0), 
            datetime.date(2020, 2, 29)) #2020 is a leap year

        self.assertEqual(
            utils.offset(datetime.date(2020,1,31), months=+1, handle=lambda eom, days: 1), 
            datetime.date(2020, 3, 1)) #2020 is a leap year

        self.assertEqual(
            utils.offset(datetime.date(2020,1,31), months=+1, handle=lambda eom, days: days), 
            datetime.date(2020, 3, 2)) #2020 is a leap year

        self.assertEqual(
            utils.offset(datetime.date(2019,1,31), months=+1, handle=lambda eom, days: days), 
            datetime.date(2019, 3, 3)) #note this example carefully!

        #by years
        self.assertEqual(utils.offset(today, years=1), datetime.date(2021, 1, 10))

        #exception handling
        self.assertEqual(
            utils.offset(datetime.date(2020, 2, 29), years=-1), 
            datetime.date(2019, 2, 28))

        self.assertEqual(
            utils.offset(datetime.date(2020, 2, 29), years=-1, handle=0), 
            datetime.date(2019, 2, 28))

        self.assertEqual(
            utils.offset(datetime.date(2020, 2, 29), years=-1, handle=1), 
            datetime.date(2019, 3, 1))

        self.assertEqual(
            utils.offset(datetime.date(2020, 2, 29), years=-1, handle=lambda eom, days: days), 
            datetime.date(2019, 3, 1))

class CalendarTests(unittest.TestCase):
    def test_init(self):
        self.assertIsInstance(
            Calendar(),
            Calendar
        )
        self.assertIsInstance(
            Calendar([]), 
            Calendar
        )
        self.assertIsInstance(
            Calendar([datetime.date.today()]), Calendar
        )
        self.assertIsInstance(
            Calendar(pd.date_range(datetime.date.today(), freq="D", periods=10)), 
            Calendar
        )
        with self.assertRaises(Exception):
            cdr = Calendar(True)

    def test_indexing(self):
        cal = Calendar([datetime.date(2019,1,1) + datetime.timedelta(i) for i in range(45)])

        self.assertEqual(
            cal[0], datetime.date(2019,1,1)
        )
        self.assertEqual(
            cal[-1], datetime.date(2019,2,14)
        )
        self.assertEqual(
            cal[0:31][-1], datetime.date(2019,1,31)
        )
        self.assertEqual(
            cal[:31][0], datetime.date(2019,1,1)
        )

    def test_slicing(self):
        dates = [
            datetime.date(2019,8,15), datetime.date(2019,8,16),
            datetime.date(2019,8,19), datetime.date(2019,8,20)
        ]
        cdr = Calendar(dates)

        self.assertEqual(
            cdr[0:2], 
            Calendar(dates[0:2])
        )
        self.assertEqual(
            cdr[-2:], 
            Calendar(dates[-2:])
        )
        self.assertEqual(
            cdr[datetime.date(2019,8,1):], 
            cdr
        )
        self.assertEqual(
            cdr[datetime.date(2019,8,15):][0], 
            datetime.date(2019,8,15)
        )
        self.assertEqual(
            cdr[datetime.date(2019,8,17):][0], 
            datetime.date(2019,8,19)
        )
        self.assertEqual(
            len(cdr[datetime.date(2019,8,21):]), 
            0
        )
        self.assertEqual(
            cdr[:datetime.date(2019,8,18)][-1],
            datetime.date(2019,8,16)
        )
        self.assertEqual(
            cdr[:datetime.date(2019,8,19)][-1],
            datetime.date(2019,8,19)
        )
        self.assertEqual(
            cdr[:datetime.date(2019,8,22)][-1],
            datetime.date(2019,8,20)
        )
        self.assertEqual(
            len(cdr[:datetime.date(2019,8,1)]),
            0
        )

    def test_first_last(self):
        dates = [
            datetime.date(2019,8,15), datetime.date(2019,8,16),
            datetime.date(2019,8,19), datetime.date(2019,8,20)
        ]
        cdr = Calendar(dates)

        self.assertEqual(cdr.first, datetime.date(2019,8,15))
        self.assertEqual(cdr.last, datetime.date(2019,8,20))

    def test_filter(self):
        dates = [
            datetime.date(2019,8,15), datetime.date(2019,8,16),
            datetime.date(2019,8,19), datetime.date(2019,8,20)
        ]
        cdr = Calendar(dates)

        self.assertEqual(
            cdr.filter(weekday=4), 
            Calendar([datetime.date(2019,8,16)])
        )

    def test_groupby(self):
        dates = [
            datetime.date(2019,8,15), datetime.date(2019,8,16),
            datetime.date(2019,8,19), datetime.date(2019,8,20)
        ]
        cdr = Calendar(dates)

        self.assertEqual(
            cdr.groupby("week").first(), 
            Calendar([dates[0], dates[2]])
        )
        self.assertEqual(
            cdr.groupby("month").first(), 
            Calendar([dates[0]])
        )
        self.assertEqual(
            cdr.groupby("year").last(), 
            Calendar([dates[-1]])
        )
        self.assertEqual(
            cdr.groupby("week").apply(lambda c: c[0:1]).combine(),
            Calendar(dates[0:1] + dates[2:3])
        )
        self.assertEqual(
            cdr.groupby("week").apply(lambda c: c[0]).combine(),
            Calendar(dates[0:1] + dates[2:3])
        )

    def test_lb(self):
        dates = [
            datetime.date(2019,8,15), datetime.date(2019,8,16),
            datetime.date(2019,8,19), datetime.date(2019,8,20)
        ]
        cdr = Calendar(dates)

        self.assertEqual(
            dates[0] in cdr, 
            True
        )

        self.assertEqual(
            dates[-1] in cdr, 
            True
        )
        
        self.assertEqual(
            datetime.date(2019,8,17) in cdr, 
            False
        )

    def test_fa(self):
        dates = [
            datetime.date(2019,8,15), datetime.date(2019,8,16),
            datetime.date(2019,8,19), datetime.date(2019,8,20)
        ]
        cdr = Calendar(dates)

        self.assertEqual(
            cdr.fa(datetime.date(2019,8,16)), 
            datetime.date(2019,8,19)
        )
        self.assertEqual(
            cdr.fa(datetime.date(2019,8,17)), 
            datetime.date(2019,8,19)
        )
        self.assertEqual(
            cdr.fa(datetime.date(2019,8,1)), 
            datetime.date(2019,8,15)
        )
        self.assertEqual(
            cdr.fa(datetime.date(2019,9,1), None), 
            None
        )

    def test_lb(self):
        dates = [
            datetime.date(2019,8,15), datetime.date(2019,8,16),
            datetime.date(2019,8,19), datetime.date(2019,8,20)
        ]
        cdr = Calendar(dates)

        self.assertEqual(
            cdr.lb(datetime.date(2019,8,16)), 
            datetime.date(2019,8,15)
        )
        self.assertEqual(
            cdr.lb(datetime.date(2019,8,17)), 
            datetime.date(2019,8,16)
        )
        self.assertEqual(
            cdr.lb(datetime.date(2019,8,30)), 
            datetime.date(2019,8,20)
        )
        self.assertEqual(
            cdr.lb(datetime.date(2019,8,1), None), 
            None
        )

    def test_dayof(self):
        dates = [
            datetime.date(2019,7,14), datetime.date(2019,7,29),
            datetime.date(2019,8,15), datetime.date(2019,8,16),
            datetime.date(2019,8,19), datetime.date(2019,8,20)
        ]
        cdr = Calendar(dates)

        self.assertEqual(
            cdr.dayof(dates[0], "month"), 
            1
        )
        self.assertEqual(
            cdr.dayof(dates[1], "month"), 
            2
        )
        self.assertEqual(
            cdr.dayof(dates[3], "month"), 
            2
        )
        self.assertEqual(
            cdr.dayof(dates[3], "year"), 
            4
        )
        self.assertEqual(
            cdr.dayof(dates[4], "week"), 
            1
        )
        self.assertEqual(
            cdr.dayof(dates[-1], "week"), 
            2
        )

    def test_setmethods(self):
        c1 = Calendar([
            datetime.date(2019,7,14), datetime.date(2019,7,29),
            datetime.date(2019,8,15), datetime.date(2019,8,16),
            datetime.date(2019,8,19)
        ])

        c2 = Calendar([
            datetime.date(2019,7,14), datetime.date(2019,7,20),
            datetime.date(2019,8,15), datetime.date(2019,8,17),
            datetime.date(2019,8,19)
        ])

        self.assertEqual(
            c1.union(c2), 
            Calendar(set(c1.dates).union(c2.dates))
        )

        self.assertEqual(
            c1.intersection(c2), 
            Calendar(set(c1.dates).intersection(set(c2.dates)))
        )

    def test_snap(self):
        dates = [
            datetime.date(2019,7,14), datetime.date(2019,7,29),
            datetime.date(2019,8,15), datetime.date(2019,8,16),
            datetime.date(2019,8,19), datetime.date(2019,8,20)
        ]
        cdr = Calendar(dates)

        refdates = [
            datetime.date(2019,7,14), datetime.date(2019,7,20),
            datetime.date(2019,8,15), datetime.date(2019,8,17),
            datetime.date(2019,8,19), datetime.date(2019,8,20)
        ]
        ref = Calendar(refdates)

        snapped = cdr.snap(ref)

        self.assertEqual(
            list(snapped), 
            [dates[0], dates[2], dates[4], dates[5]]
        )
        
        snapped = cdr.snap(ref, fallback="next")

        self.assertEqual(
            list(snapped), 
            [refdates[0], refdates[2], refdates[3], refdates[4], refdates[5]]
        )
        
        snapped = cdr.snap(ref, fallback="previous")

        self.assertEqual(
            list(snapped), 
            [refdates[0], refdates[1], refdates[2], refdates[4], refdates[5]]
        )

    def test_asof(self):
        #load a calendar (see CSV file)
        calendar = load()
        
        #a normal, open Monday
        self.assertEqual(
            calendar.asof(datetime.date(2019,10,21)),
            datetime.date(2019,10,21)
        )

        #saturday 21/10/2019
        self.assertEqual(
            calendar.asof(datetime.date(2019,10,19)),
            datetime.date(2019,10,18)
        )

        #sunday 20/10/2019
        self.assertEqual(
            calendar.asof(datetime.date(2019,10,20)),
            datetime.date(2019,10,18)
        )

        #a date way past the last date of the calendar
        self.assertEqual(
            calendar.asof(datetime.date(2019,12,31)),
            datetime.date(2019,11,15)
        )

        #a date way before the first date
        with self.assertRaises(Exception):
            calendar.asof(datetime.date(2000,1,1))

    def test_map(self):
        calendar = load()

        self.assertIsInstance(
            calendar.map(lambda date: datetime.datetime(date.year, date.month, 1)), 
            Calendar
        )

        self.assertIsInstance(
            calendar.map(lambda date: date.year), 
            list
        )

    def test_daysfrom(self):
        calendar = load()
        
        self.assertEqual(
            calendar.daysfrom("year-start", asof=datetime.date(2018,1,10)),
            6
        )

        self.assertEqual(
            calendar.daysfrom("week-start", asof=datetime.date(2019,10,31)),
            calendar[datetime.date(2019,10,28):datetime.date(2019,10,30)].length
        )
        self.assertEqual(
            calendar.daysfrom("ws", asof=datetime.date(2019,10,31)),
            calendar[datetime.date(2019,10,28):datetime.date(2019,10,30)].length
        )

        self.assertEqual(
            calendar.daysfrom("month-start", asof=datetime.date(2019,10,31)),
            calendar[datetime.date(2019,10,1):datetime.date(2019,10,30)].length
        )
        self.assertEqual(
            calendar.daysfrom("ms", asof=datetime.date(2019,10,31)),
            calendar[datetime.date(2019,10,1):datetime.date(2019,10,30)].length
        )

        self.assertEqual(
            calendar.daysfrom("quarter-start", asof=datetime.date(2019,10,31)),
            calendar[datetime.date(2019,10,1):datetime.date(2019,10,30)].length
        )
        self.assertEqual(
            calendar.daysfrom("qs", asof=datetime.date(2019,10,31)),
            calendar[datetime.date(2019,10,1):datetime.date(2019,10,30)].length
        )

        self.assertEqual(
            calendar.daysfrom("semester-start", asof=datetime.date(2019,10,31)),
            calendar[datetime.date(2019,7,1):datetime.date(2019,10,30)].length
        )
        self.assertEqual(
            calendar.daysfrom("ss", asof=datetime.date(2019,10,31)),
            calendar[datetime.date(2019,7,1):datetime.date(2019,10,30)].length
        )

        self.assertEqual(
            calendar.daysfrom("year-start", asof=datetime.date(2019,10,31)),
            calendar[datetime.date(2019,1,1):datetime.date(2019,10,30)].length
        )
        self.assertEqual(
            calendar.daysfrom("ys", asof=datetime.date(2019,10,31)),
            calendar[datetime.date(2019,1,1):datetime.date(2019,10,30)].length
        )
    
    def test_daysto(self):
        calendar = load()

        self.assertEqual(
            calendar.daysto("week-end", asof=datetime.date(2018,10,31)),
            2
        )
        self.assertEqual(
            calendar.daysto("we", asof=datetime.date(2018,10,31)),
            2
        )
        
        self.assertEqual(
            calendar.daysto("month-end", asof=datetime.date(2018,1,8)),
            16
        )
        self.assertEqual(
            calendar.daysto("me", asof=datetime.date(2018,1,8)),
            16
        )

        self.assertEqual(
            calendar.daysto("quarter-end", asof=datetime.date(2018,5,25)),
            calendar[datetime.date(2018,5,26):datetime.date(2018,6,30)].length
        )
        self.assertEqual(
            calendar.daysto("qe", asof=datetime.date(2018,5,25)),
            calendar[datetime.date(2018,5,26):datetime.date(2018,6,30)].length
        )

        self.assertEqual(
            calendar.daysto("semester-end", asof=datetime.date(2018,5,25)),
            calendar[datetime.date(2018,5,26):datetime.date(2018,6,30)].length
        )
        self.assertEqual(
            calendar.daysto("se", asof=datetime.date(2018,5,25)),
            calendar[datetime.date(2018,5,26):datetime.date(2018,6,30)].length
        )

        self.assertEqual(
            calendar.daysto("year-end", asof=datetime.date(2018,5,25)),
            calendar[datetime.date(2018,5,26):datetime.date(2018,12,31)].length
        )
        self.assertEqual(
            calendar.daysto("ye", asof=datetime.date(2018,5,25)),
            calendar[datetime.date(2018,5,26):datetime.date(2018,12,31)].length
        )
        self.assertEqual(
            calendar.daysto(datetime.date(2018,12,31), asof=datetime.date(2018,5,25)),
            calendar[datetime.date(2018,5,26):datetime.date(2018,12,31)].length
        )
    
    def test_between(self):
        calendar = load()

        self.assertEqual(
            calendar.daysbetween(calendar[0],calendar[99]),
            len(calendar[0:100])
        )

        self.assertEqual(
            calendar.daysbetween(calendar[50], calendar[100], "both"), 
            51
        )

        self.assertEqual(
            calendar.daysbetween(calendar[50], calendar[100], "left"), 
            50
        )

        self.assertEqual(
            calendar.daysbetween(calendar[50], calendar[100], "right"), 
            50
        )
    
    def test_iter(self):
        calendar = load()
        
        self.assertEqual(
            len([date for date in calendar.iter()]), 
            len([date for date in calendar])
        )

        self.assertEqual(
            sum([len(x) for x in calendar.iter("i", "date")]), 
            sum([2 for i, date in enumerate(calendar)])
        )

    def test__add__(self):
        calendar = load()

        #add two calendars
        combined = calendar[5:20] + calendar[10:30]
        self.assertIsInstance(calendar, Calendar)
        self.assertEqual(len(combined), 30-5)

        #add a date to a calendar
        combined = calendar[0:5] + calendar[5]
        self.assertIsInstance(calendar, Calendar)
        self.assertEqual(len(combined), 6)

    def test_calendar_utilities(self):
        calendar = load()

        self.assertEqual(
            calendar.eom(datetime.date(2018,9,19)),
            datetime.date(2018,9,28)
        )

        self.assertEqual(
            calendar.som(datetime.date(2018,9,19)),
            datetime.date(2018,9,4)
        )

        self.assertEqual(
            calendar.eoq(datetime.date(2018,9,19)),
            datetime.date(2018,9,28)
        )

        self.assertEqual(
            calendar.soq(datetime.date(2018,9,19)),
            datetime.date(2018,7,2)
        )

        self.assertEqual(
            calendar.eoy(datetime.date(2018,9,19)),
            datetime.date(2018,12,31)
        )

        self.assertEqual(
            calendar.soy(datetime.date(2018,9,19)),
            datetime.date(2018,1,2)
        )

        self.assertEqual(
            calendar.eoy(datetime.date(2019,11,14)),
            datetime.date(2019,11,15)
        )

        self.assertEqual(
            calendar.eoy(datetime.date(2019,11,15)),
            datetime.date(2019,11,15)
        )

        self.assertEqual(
            calendar.soy(datetime.date(2014,12,22)),
            datetime.date(2014,11,17)
        )

        self.assertEqual(
            calendar.soy(datetime.date(2014,11,17)),
            datetime.date(2014,11,17)
        )

class TestGrouper(unittest.TestCase):
    def test_index(self):
        cals = load().groupby("month")

        self.assertTrue(
            datetime.date(2014,12,16) in cals
        )

        self.assertFalse(
            datetime.date(2014,12,25) in cals
        )

        self.assertIsInstance(
            cals[datetime.date(2014,12,16)], 
            Calendar
        )



if __name__ == '__main__':
    unittest.main()