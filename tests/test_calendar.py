import unittest
import datetime
import os
import pandas as pd

import doubledate.utils as utils

from doubledate import Calendar, BD


def load():
    with open(os.path.join(os.path.dirname(__file__), "calendar.csv"), "r") as f:
        return Calendar(
            [
                datetime.datetime.strptime(date, "%Y-%m-%d").date()
                for date in f.read().strip().split("\n")
            ]
        )


class CalendarTests(unittest.TestCase):
    def test_init(self):
        with self.assertRaises(Exception):
            self.assertIsInstance(Calendar(), Calendar)

        self.assertIsInstance(Calendar([]), Calendar)
        self.assertIsInstance(Calendar([datetime.date.today()]), Calendar)
        self.assertIsInstance(
            Calendar(pd.date_range(datetime.date.today(), freq="D", periods=10)),
            Calendar,
        )
        with self.assertRaises(Exception):
            cdr = Calendar(True)

    def test_generate(self):
        calendar = Calendar.generate(
            datetime.date(2021, 1, 1), datetime.date(2021, 12, 31)
        )

        assert len(calendar) == 365
        assert calendar[0] == datetime.date(2021, 1, 1)
        assert calendar[-1] == datetime.date(2021, 12, 31)

        calendar = Calendar.generate(
            datetime.date(2021, 1, 1), datetime.date(2021, 1, 1)
        )

        assert len(calendar) == 1
        assert calendar[0] == calendar[-1] == datetime.date(2021, 1, 1)

        # test if starting > ending date
        calendar = Calendar.generate(
            datetime.date(2021, 12, 31), datetime.date(2021, 1, 1)
        )

        assert len(calendar) == 0

    def test_indexing(self):
        cal = Calendar(
            [datetime.date(2019, 1, 1) + datetime.timedelta(i) for i in range(45)]
        )

        self.assertEqual(cal[0], datetime.date(2019, 1, 1))
        self.assertEqual(cal[-1], datetime.date(2019, 2, 14))
        self.assertEqual(cal[0:31][-1], datetime.date(2019, 1, 31))
        self.assertEqual(cal[:31][0], datetime.date(2019, 1, 1))

    def test_slicing(self):
        dates = [
            datetime.date(2019, 8, 15),
            datetime.date(2019, 8, 16),
            datetime.date(2019, 8, 19),
            datetime.date(2019, 8, 20),
        ]
        cdr = Calendar(dates)

        self.assertEqual(cdr[0:2], Calendar(dates[0:2]))
        self.assertEqual(cdr[-2:], Calendar(dates[-2:]))
        self.assertEqual(cdr[datetime.date(2019, 8, 1) :], cdr)
        self.assertEqual(
            cdr[datetime.date(2019, 8, 15) :][0], datetime.date(2019, 8, 15)
        )
        self.assertEqual(
            cdr[datetime.date(2019, 8, 17) :][0], datetime.date(2019, 8, 19)
        )
        self.assertEqual(len(cdr[datetime.date(2019, 8, 21) :]), 0)
        self.assertEqual(
            cdr[: datetime.date(2019, 8, 18)][-1], datetime.date(2019, 8, 16)
        )
        self.assertEqual(
            cdr[: datetime.date(2019, 8, 19)][-1], datetime.date(2019, 8, 19)
        )
        self.assertEqual(
            cdr[: datetime.date(2019, 8, 22)][-1], datetime.date(2019, 8, 20)
        )
        self.assertEqual(len(cdr[: datetime.date(2019, 8, 1)]), 0)

    def test_first_last(self):
        dates = [
            datetime.date(2019, 8, 15),
            datetime.date(2019, 8, 16),
            datetime.date(2019, 8, 19),
            datetime.date(2019, 8, 20),
        ]
        cdr = Calendar(dates)

        self.assertEqual(cdr.first, datetime.date(2019, 8, 15))
        self.assertEqual(cdr.last, datetime.date(2019, 8, 20))

    def test_filter(self):
        dates = [
            datetime.date(2019, 8, 15),
            datetime.date(2019, 8, 16),
            datetime.date(2019, 8, 19),
            datetime.date(2019, 8, 20),
        ]
        cdr = Calendar(dates)

        self.assertEqual(cdr.filter(weekday=4), Calendar([datetime.date(2019, 8, 16)]))

    def test_groupby(self):
        dates = [
            datetime.date(2019, 8, 15),
            datetime.date(2019, 8, 16),
            datetime.date(2019, 8, 19),
            datetime.date(2019, 8, 20),
        ]
        cdr = Calendar(dates)

        self.assertEqual(cdr.groupby("W").first(), Calendar([dates[0], dates[2]]))
        self.assertEqual(cdr.groupby("M").first(), Calendar([dates[0]]))
        self.assertEqual(cdr.groupby("Y").last(), Calendar([dates[-1]]))
        self.assertEqual(
            cdr.groupby("W").apply(lambda c: c[0:1]).combine(),
            Calendar(dates[0:1] + dates[2:3]),
        )
        self.assertEqual(
            cdr.groupby("W").apply(lambda c: c[0]).combine(),
            Calendar(dates[0:1] + dates[2:3]),
        )

    def test_lb(self):
        dates = [
            datetime.date(2019, 8, 15),
            datetime.date(2019, 8, 16),
            datetime.date(2019, 8, 19),
            datetime.date(2019, 8, 20),
        ]
        cdr = Calendar(dates)

        self.assertEqual(dates[0] in cdr, True)

        self.assertEqual(dates[-1] in cdr, True)

        self.assertEqual(datetime.date(2019, 8, 17) in cdr, False)

    def test_fa(self):
        dates = [
            datetime.date(2019, 8, 15),
            datetime.date(2019, 8, 16),
            datetime.date(2019, 8, 19),
            datetime.date(2019, 8, 20),
        ]
        cdr = Calendar(dates)

        self.assertEqual(cdr.fa(datetime.date(2019, 8, 16)), datetime.date(2019, 8, 19))
        self.assertEqual(cdr.fa(datetime.date(2019, 8, 17)), datetime.date(2019, 8, 19))
        self.assertEqual(cdr.fa(datetime.date(2019, 8, 1)), datetime.date(2019, 8, 15))
        self.assertEqual(cdr.fa(datetime.date(2019, 9, 1), None), None)

    def test_lb(self):
        dates = [
            datetime.date(2019, 8, 15),
            datetime.date(2019, 8, 16),
            datetime.date(2019, 8, 19),
            datetime.date(2019, 8, 20),
        ]
        cdr = Calendar(dates)

        self.assertEqual(cdr.lb(datetime.date(2019, 8, 16)), datetime.date(2019, 8, 15))
        self.assertEqual(cdr.lb(datetime.date(2019, 8, 17)), datetime.date(2019, 8, 16))
        self.assertEqual(cdr.lb(datetime.date(2019, 8, 30)), datetime.date(2019, 8, 20))
        self.assertEqual(cdr.lb(datetime.date(2019, 8, 1), None), None)

    def test_dayof(self):
        dates = [
            datetime.date(2019, 7, 14),
            datetime.date(2019, 7, 29),
            datetime.date(2019, 8, 15),
            datetime.date(2019, 8, 16),
            datetime.date(2019, 8, 19),
            datetime.date(2019, 8, 20),
        ]
        cdr = Calendar(dates)

        self.assertEqual(cdr.dayof("M")[dates[0]], 1)
        self.assertEqual(cdr.dayof("M")[dates[1]], 2)
        self.assertEqual(cdr.dayof("M")[dates[3]], 2)
        self.assertEqual(cdr.dayof("Y")[dates[3]], 4)
        self.assertEqual(cdr.dayof("W")[dates[4]], 1)
        self.assertEqual(cdr.dayof("W")[dates[-1]], 2)

    def test_setmethods(self):
        c1 = Calendar(
            [
                datetime.date(2019, 7, 14),
                datetime.date(2019, 7, 29),
                datetime.date(2019, 8, 15),
                datetime.date(2019, 8, 16),
                datetime.date(2019, 8, 19),
            ]
        )

        c2 = Calendar(
            [
                datetime.date(2019, 7, 14),
                datetime.date(2019, 7, 20),
                datetime.date(2019, 8, 15),
                datetime.date(2019, 8, 17),
                datetime.date(2019, 8, 19),
            ]
        )

        self.assertEqual(c1.union(c2), Calendar(set(c1.dates).union(c2.dates)))

        self.assertEqual(
            c1.intersection(c2), Calendar(set(c1.dates).intersection(set(c2.dates)))
        )

    def test_snap(self):
        dates = [
            datetime.date(2019, 7, 14),
            datetime.date(2019, 7, 29),
            datetime.date(2019, 8, 15),
            datetime.date(2019, 8, 16),
            datetime.date(2019, 8, 19),
            datetime.date(2019, 8, 20),
        ]
        cdr = Calendar(dates)

        refdates = [
            datetime.date(2019, 7, 14),
            datetime.date(2019, 7, 20),
            datetime.date(2019, 8, 15),
            datetime.date(2019, 8, 17),
            datetime.date(2019, 8, 19),
            datetime.date(2019, 8, 20),
        ]
        ref = Calendar(refdates)

        snapped = cdr.snap(ref)

        self.assertEqual(list(snapped), [dates[0], dates[2], dates[4], dates[5]])

        snapped = cdr.snap(ref, fallback="next")

        self.assertEqual(
            list(snapped),
            [refdates[0], refdates[2], refdates[3], refdates[4], refdates[5]],
        )

        snapped = cdr.snap(ref, fallback="previous")

        self.assertEqual(
            list(snapped),
            [refdates[0], refdates[1], refdates[2], refdates[4], refdates[5]],
        )

    def test_asof(self):
        # load a calendar (see CSV file)
        calendar = load()

        # a normal, open Monday
        self.assertEqual(
            calendar.asof(datetime.date(2019, 10, 21)), datetime.date(2019, 10, 21)
        )

        # saturday 21/10/2019
        self.assertEqual(
            calendar.asof(datetime.date(2019, 10, 19)), datetime.date(2019, 10, 18)
        )

        # sunday 20/10/2019
        self.assertEqual(
            calendar.asof(datetime.date(2019, 10, 20)), datetime.date(2019, 10, 18)
        )

        # a date way past the last date of the calendar
        self.assertEqual(
            calendar.asof(datetime.date(2019, 12, 31)), datetime.date(2019, 11, 15)
        )

        # a date way before the first date
        with self.assertRaises(Exception):
            calendar.asof(datetime.date(2000, 1, 1))

    def test_apply(self):
        calendar = load()

        self.assertIsInstance(
            calendar.apply(lambda date: datetime.datetime(date.year, date.month, 1)),
            Calendar,
        )

        self.assertIsInstance(calendar.apply(lambda date: date.year), list)

    def test_daysfrom(self):
        calendar = load()

        self.assertEqual(calendar.daysfrom("YS")[datetime.date(2018, 1, 10)], 6)

        self.assertEqual(
            calendar.daysfrom("WS")[datetime.date(2019, 10, 31)],
            len(calendar[datetime.date(2019, 10, 28) : datetime.date(2019, 10, 30)]),
        )
        self.assertEqual(
            calendar.daysfrom("WS")[datetime.date(2019, 10, 31)],
            len(calendar[datetime.date(2019, 10, 28) : datetime.date(2019, 10, 30)]),
        )

        self.assertEqual(
            calendar.daysfrom("MS")[datetime.date(2019, 10, 31)],
            len(calendar[datetime.date(2019, 10, 1) : datetime.date(2019, 10, 30)]),
        )
        self.assertEqual(
            calendar.daysfrom("MS")[datetime.date(2019, 10, 31)],
            len(calendar[datetime.date(2019, 10, 1) : datetime.date(2019, 10, 30)]),
        )

        self.assertEqual(
            calendar.daysfrom("QS")[datetime.date(2019, 10, 31)],
            len(calendar[datetime.date(2019, 10, 1) : datetime.date(2019, 10, 30)]),
        )
        self.assertEqual(
            calendar.daysfrom("QS")[datetime.date(2019, 10, 31)],
            len(calendar[datetime.date(2019, 10, 1) : datetime.date(2019, 10, 30)]),
        )

        self.assertEqual(
            calendar.daysfrom("HS")[datetime.date(2019, 10, 31)],
            len(calendar[datetime.date(2019, 7, 1) : datetime.date(2019, 10, 30)]),
        )
        self.assertEqual(
            calendar.daysfrom("HS")[datetime.date(2019, 10, 31)],
            len(calendar[datetime.date(2019, 7, 1) : datetime.date(2019, 10, 30)]),
        )

        self.assertEqual(
            calendar.daysfrom("YS")[datetime.date(2019, 10, 31)],
            len(calendar[datetime.date(2019, 1, 1) : datetime.date(2019, 10, 30)]),
        )
        self.assertEqual(
            calendar.daysfrom("YS")[datetime.date(2019, 10, 31)],
            len(calendar[datetime.date(2019, 1, 1) : datetime.date(2019, 10, 30)]),
        )

    def test_daysto(self):
        calendar = load()

        self.assertEqual(calendar.daysto("WE")[datetime.date(2018, 10, 31)], 2)
        self.assertEqual(calendar.daysto("WE")[datetime.date(2018, 10, 31)], 2)

        self.assertEqual(calendar.daysto("ME")[datetime.date(2018, 1, 8)], 16)
        self.assertEqual(calendar.daysto("ME")[datetime.date(2018, 1, 8)], 16)

        self.assertEqual(
            calendar.daysto("QE")[datetime.date(2018, 5, 25)],
            len(calendar[datetime.date(2018, 5, 26) : datetime.date(2018, 6, 30)]),
        )
        self.assertEqual(
            calendar.daysto("QE")[datetime.date(2018, 5, 25)],
            len(calendar[datetime.date(2018, 5, 26) : datetime.date(2018, 6, 30)]),
        )

        self.assertEqual(
            calendar.daysto("HE")[datetime.date(2018, 5, 25)],
            len(calendar[datetime.date(2018, 5, 26) : datetime.date(2018, 6, 30)]),
        )
        self.assertEqual(
            calendar.daysto("HE")[datetime.date(2018, 5, 25)],
            len(calendar[datetime.date(2018, 5, 26) : datetime.date(2018, 6, 30)]),
        )

        self.assertEqual(
            calendar.daysto("YE")[datetime.date(2018, 5, 25)],
            len(calendar[datetime.date(2018, 5, 26) : datetime.date(2018, 12, 31)]),
        )
        self.assertEqual(
            calendar.daysto("YE")[datetime.date(2018, 5, 25)],
            len(calendar[datetime.date(2018, 5, 26) : datetime.date(2018, 12, 31)]),
        )
        # self.assertEqual(
        #     calendar.daysto(datetime.date(2018, 12, 31))[datetime.date(2018, 5, 25)],
        #     len(calendar[datetime.date(2018, 5, 26) : datetime.date(2018, 12, 31)]),
        # )

    def test_between(self):
        calendar = load()

        self.assertEqual(
            calendar.daysbetween(calendar[0], calendar[99]), len(calendar[0:99])
        )

        self.assertEqual(calendar.daysbetween(calendar[50], calendar[100], "both"), 51)

        self.assertEqual(calendar.daysbetween(calendar[50], calendar[100], "left"), 50)

        self.assertEqual(calendar.daysbetween(calendar[50], calendar[100], "right"), 50)

    def test__add__(self):
        calendar = load()

        # add two calendars
        combined = calendar[5:20] + calendar[10:30]
        self.assertIsInstance(calendar, Calendar)
        self.assertEqual(len(combined), 30 - 5)

        # add a date to a calendar
        combined = calendar[0:5] + calendar[5]
        self.assertIsInstance(calendar, Calendar)
        self.assertEqual(len(combined), 6)

    def test_calendar_utilities(self):
        calendar = load()

        self.assertEqual(
            calendar.eom(datetime.date(2018, 9, 19)), datetime.date(2018, 9, 28)
        )

        self.assertEqual(
            calendar.som(datetime.date(2018, 9, 19)), datetime.date(2018, 9, 4)
        )

        self.assertEqual(
            calendar.eoq(datetime.date(2018, 9, 19)), datetime.date(2018, 9, 28)
        )

        self.assertEqual(
            calendar.soq(datetime.date(2018, 9, 19)), datetime.date(2018, 7, 2)
        )

        self.assertEqual(
            calendar.eoy(datetime.date(2018, 9, 19)), datetime.date(2018, 12, 31)
        )

        self.assertEqual(
            calendar.soy(datetime.date(2018, 9, 19)), datetime.date(2018, 1, 2)
        )

        self.assertEqual(
            calendar.eoy(datetime.date(2019, 11, 14)), datetime.date(2019, 11, 15)
        )

        self.assertEqual(
            calendar.eoy(datetime.date(2019, 11, 15)), datetime.date(2019, 11, 15)
        )

        self.assertEqual(
            calendar.soy(datetime.date(2014, 12, 22)), datetime.date(2014, 11, 17)
        )

        self.assertEqual(
            calendar.soy(datetime.date(2014, 11, 17)), datetime.date(2014, 11, 17)
        )

    def test_splitter(self):
        cdr = load()
        self.assertIsInstance(cdr.split(BD(0, "M")).first(), Calendar)
        self.assertIsInstance(cdr.split(BD(10, "M")).first(), Calendar)
        self.assertIsInstance(cdr.split(starting=BD(10, "M")).first(), Calendar)
        self.assertIsInstance(cdr.split(ending=BD(10, "M")).first(), Calendar)

        # simply split on first day of month
        self.assertEqual(cdr.split(BD(0)).first()[0], datetime.date(2014, 11, 17))
        self.assertEqual(cdr.split(BD(0)).last()[0], datetime.date(2014, 11, 28))

        # simply split on first day of month
        self.assertEqual(
            cdr.split(starting=BD(0)).first()[0], datetime.date(2014, 11, 17)
        )
        self.assertEqual(
            cdr.split(starting=BD(0)).last()[0], datetime.date(2014, 11, 28)
        )

        # should be the same as splitting on last day of the month
        self.assertEqual(
            cdr.split(ending=BD(-1)).first()[0], datetime.date(2014, 11, 17)
        )
        self.assertEqual(
            cdr.split(ending=BD(-1)).last()[0], datetime.date(2014, 11, 28)
        )

        # simply split on first day of month
        self.assertEqual(
            cdr.split(ending=BD(0)).first()[0], datetime.date(2014, 11, 17)
        )
        self.assertEqual(
            cdr.split(ending=BD(0)).first()[1], datetime.date(2014, 11, 18)
        )
        self.assertEqual(cdr.split(ending=BD(0)).first()[2], datetime.date(2014, 12, 2))

    def test_inversing_with_no_bounds(self):
        calendar = Calendar(
            [datetime.date(2022, 1, 17), datetime.date(2022, 2, 14)]
        ).inverse()

        assert calendar[0] == datetime.date(2022, 1, 18)
        assert calendar[-1] == datetime.date(2022, 2, 13)

    def test_inversing_with_bounds(self):
        calendar = Calendar(
            [datetime.date(2022, 1, 17), datetime.date(2022, 2, 14)]
        ).inverse(datetime.date(2022, 1, 1), datetime.date(2022, 12, 31))

        assert calendar[0] == datetime.date(2022, 1, 1)
        assert calendar[-1] == datetime.date(2022, 12, 31)

        assert datetime.date(2022, 1, 17) not in calendar
        assert datetime.date(2022, 2, 14) not in calendar
        assert len(calendar) == 365 - 2

        # test with starting date equal to a holiday
        calendar = Calendar(
            [datetime.date(2022, 1, 17), datetime.date(2022, 2, 14)]
        ).inverse(datetime.date(2022, 1, 17), datetime.date(2022, 12, 31))

        assert calendar[0] == datetime.date(2022, 1, 18)


class TestCollection(unittest.TestCase):
    def test_index(self):
        cals = load().groupby("M")

        self.assertTrue(datetime.date(2014, 12, 16) in cals)

        self.assertFalse(datetime.date(2014, 12, 25) in cals)


if __name__ == "__main__":
    unittest.main()
