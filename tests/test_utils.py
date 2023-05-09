import unittest
import datetime
import os

import doubledate.utils as utils
import doubledate


def load():
    return (
        doubledate.Calendar(
            [
                utils.parse(d, dayfirst=False)
                for d in [
                    "2014-11-27",
                    "2014-12-25",
                    "2015-01-01",
                    "2015-01-19",
                    "2015-02-16",
                    "2015-04-03",
                    "2015-05-25",
                    "2015-07-03",
                    "2015-09-07",
                    "2015-11-26",
                    "2015-12-25",
                    "2016-01-01",
                    "2016-01-18",
                    "2016-02-15",
                    "2016-03-25",
                    "2016-05-30",
                    "2016-07-04",
                    "2016-09-05",
                    "2016-11-24",
                    "2016-12-26",
                    "2017-01-02",
                    "2017-01-16",
                    "2017-02-20",
                    "2017-04-14",
                    "2017-05-29",
                    "2017-07-04",
                    "2017-09-04",
                    "2017-11-23",
                    "2017-12-25",
                    "2018-01-01",
                    "2018-01-15",
                    "2018-02-19",
                    "2018-03-30",
                    "2018-05-28",
                    "2018-07-04",
                    "2018-09-03",
                    "2018-11-22",
                    "2018-12-05",
                    "2018-12-25",
                    "2019-01-01",
                    "2019-01-21",
                    "2019-02-18",
                    "2019-04-19",
                    "2019-05-27",
                    "2019-07-04",
                    "2019-09-02",
                ]
            ]
        )
        .inverse(
            starting=datetime.date(2014, 11, 17), ending=datetime.date(2019, 11, 15)
        )
        .weekdays()
        .dates
    )


class TestUtils(unittest.TestCase):
    def test_semester(self):
        dates = [
            datetime.date(2019, 1, 1),
            datetime.date(2019, 6, 30),
            datetime.date(2019, 7, 1),
            datetime.date(2019, 12, 31),
        ]
        self.assertEqual([utils.semester(date) for date in dates], [1, 1, 2, 2])

    def test_trimester(self):
        dates = [
            datetime.date(2019, 1, 1),
            datetime.date(2019, 6, 30),
            datetime.date(2019, 7, 1),
            datetime.date(2019, 12, 31),
        ]
        self.assertEqual([utils.trimester(date) for date in dates], [1, 2, 2, 3])

    def test_quarter(self):
        dates = [
            datetime.date(2019, 1, 1),
            datetime.date(2019, 6, 30),
            datetime.date(2019, 7, 1),
            datetime.date(2019, 12, 31),
        ]
        self.assertEqual([utils.quarter(date) for date in dates], [1, 2, 3, 4])

    def test_eow(self):
        self.assertEqual(
            utils.eow(datetime.date(2020, 1, 4)), datetime.date(2020, 1, 5)
        )
        self.assertEqual(
            utils.eow(datetime.date(2020, 1, 4), 0), datetime.date(2020, 1, 5)
        )
        self.assertEqual(
            utils.eow(datetime.date(2020, 1, 4), 0, "SUN"), datetime.date(2020, 1, 5)
        )
        self.assertEqual(
            utils.eow(datetime.date(2020, 1, 4), 1, "SUN"), datetime.date(2020, 1, 12)
        )
        self.assertEqual(
            utils.eow(datetime.date(2020, 1, 4), -1, "SUN"), datetime.date(2019, 12, 29)
        )
        self.assertEqual(
            utils.eow(datetime.date(2020, 1, 4), 0, "SAT"), datetime.date(2020, 1, 4)
        )
        self.assertEqual(
            utils.eow(datetime.date(2020, 1, 4), 0, "FRI"), datetime.date(2020, 1, 10)
        )
        self.assertEqual(
            utils.eow(datetime.date(2020, 1, 4), 0, "THU"), datetime.date(2020, 1, 9)
        )
        self.assertEqual(
            utils.eow(datetime.date(2020, 1, 4), 0, "WED"), datetime.date(2020, 1, 8)
        )
        self.assertEqual(
            utils.eow(datetime.date(2020, 1, 4), 0, "TUE"), datetime.date(2020, 1, 7)
        )
        self.assertEqual(
            utils.eow(datetime.date(2020, 1, 4), 0, "MON"), datetime.date(2020, 1, 6)
        )

    def test_sow(self):
        self.assertEqual(
            utils.sow(datetime.date(2020, 1, 4)), datetime.date(2019, 12, 30)
        )
        self.assertEqual(
            utils.sow(datetime.date(2020, 1, 4), 0), datetime.date(2019, 12, 30)
        )
        self.assertEqual(
            utils.sow(datetime.date(2020, 1, 4), 0, "SUN"), datetime.date(2019, 12, 29)
        )
        self.assertEqual(
            utils.sow(datetime.date(2020, 1, 4), 0, "SAT"), datetime.date(2020, 1, 4)
        )
        self.assertEqual(
            utils.sow(datetime.date(2020, 1, 4), 0, "FRI"), datetime.date(2020, 1, 3)
        )
        self.assertEqual(
            utils.sow(datetime.date(2020, 1, 4), 0, "THU"), datetime.date(2020, 1, 2)
        )
        self.assertEqual(
            utils.sow(datetime.date(2020, 1, 4), 0, "WED"), datetime.date(2020, 1, 1)
        )
        self.assertEqual(
            utils.sow(datetime.date(2020, 1, 4), 0, "TUE"), datetime.date(2019, 12, 31)
        )
        self.assertEqual(
            utils.sow(datetime.date(2020, 1, 4), 0, "MON"), datetime.date(2019, 12, 30)
        )

    def test_eom(self):
        self.assertEqual(
            utils.eom(datetime.date(2019, 6, 17)), datetime.date(2019, 6, 30)
        )

        self.assertEqual(
            utils.eom(datetime.date(2019, 6, 17), 0), datetime.date(2019, 6, 30)
        )

        self.assertEqual(
            utils.eom(datetime.date(2019, 6, 17), 1), datetime.date(2019, 7, 31)
        )

        self.assertEqual(
            utils.eom(datetime.date(2019, 6, 17), -1), datetime.date(2019, 5, 31)
        )

        self.assertEqual(
            utils.eom(datetime.date(2016, 2, 29), 0), datetime.date(2016, 2, 29)
        )

        self.assertEqual(
            utils.eom(datetime.date(2016, 2, 29), 12), datetime.date(2017, 2, 28)
        )

    def test_som(self):
        self.assertEqual(
            utils.som(datetime.date(2019, 6, 17)), datetime.date(2019, 6, 1)
        )

        self.assertEqual(
            utils.som(datetime.date(2016, 3, 15), -1), datetime.date(2016, 2, 1)
        )

        self.assertEqual(
            utils.som(datetime.date(2015, 4, 20), 1), datetime.date(2015, 5, 1)
        )

    def test_soq(self):
        self.assertEqual(
            utils.soq(datetime.date(2020, 1, 4)), datetime.date(2020, 1, 1)
        )
        self.assertEqual(
            utils.soq(datetime.date(2020, 3, 31)), datetime.date(2020, 1, 1)
        )
        self.assertEqual(
            utils.soq(datetime.date(2020, 2, 4), 0), datetime.date(2020, 1, 1)
        )
        self.assertEqual(
            utils.soq(datetime.date(2020, 2, 4), 1), datetime.date(2020, 4, 1)
        )
        self.assertEqual(
            utils.soq(datetime.date(2020, 2, 4), -1), datetime.date(2019, 10, 1)
        )

    def test_eoq(self):
        self.assertEqual(
            utils.eoq(datetime.date(2020, 1, 4)), datetime.date(2020, 3, 31)
        )
        self.assertEqual(
            utils.eoq(datetime.date(2020, 3, 31)), datetime.date(2020, 3, 31)
        )
        self.assertEqual(
            utils.eoq(datetime.date(2020, 1, 4), 0), datetime.date(2020, 3, 31)
        )
        self.assertEqual(
            utils.eoq(datetime.date(2020, 1, 4), 1), datetime.date(2020, 6, 30)
        )
        self.assertEqual(
            utils.eoq(datetime.date(2020, 1, 4), -1), datetime.date(2019, 12, 31)
        )

    def test_sot(self):
        self.assertEqual(
            utils.sot(datetime.date(2019, 11, 4)), datetime.date(2019, 9, 1)
        )
        self.assertEqual(
            utils.sot(datetime.date(2019, 11, 4), 0), datetime.date(2019, 9, 1)
        )
        self.assertEqual(
            utils.sot(datetime.date(2019, 11, 4), 1), datetime.date(2020, 1, 1)
        )
        self.assertEqual(
            utils.sot(datetime.date(2019, 11, 4), -1), datetime.date(2019, 5, 1)
        )

    def test_eot(self):
        self.assertEqual(
            utils.eot(datetime.date(2019, 11, 4)), datetime.date(2019, 12, 31)
        )
        self.assertEqual(
            utils.eot(datetime.date(2019, 11, 4), 0), datetime.date(2019, 12, 31)
        )
        self.assertEqual(
            utils.eot(datetime.date(2019, 11, 4), 1), datetime.date(2020, 4, 30)
        )
        self.assertEqual(
            utils.eot(datetime.date(2019, 11, 4), -1), datetime.date(2019, 8, 31)
        )

    def test_sos(self):
        self.assertEqual(
            utils.sos(datetime.date(2019, 11, 4)), datetime.date(2019, 7, 1)
        )
        self.assertEqual(
            utils.sos(datetime.date(2019, 11, 4), 0), datetime.date(2019, 7, 1)
        )
        self.assertEqual(
            utils.sos(datetime.date(2019, 11, 4), 1), datetime.date(2020, 1, 1)
        )
        self.assertEqual(
            utils.sos(datetime.date(2019, 11, 4), -1), datetime.date(2019, 1, 1)
        )

    def test_eos(self):
        self.assertEqual(
            utils.eos(datetime.date(2019, 11, 4)), datetime.date(2019, 12, 31)
        )
        self.assertEqual(
            utils.eos(datetime.date(2019, 11, 4), 0), datetime.date(2019, 12, 31)
        )
        self.assertEqual(
            utils.eos(datetime.date(2019, 11, 4), 1), datetime.date(2020, 6, 30)
        )
        self.assertEqual(
            utils.eos(datetime.date(2019, 11, 4), -1), datetime.date(2019, 6, 30)
        )

    def test_eoy(self):
        self.assertEqual(
            utils.eoy(datetime.date(2019, 11, 4)), datetime.date(2019, 12, 31)
        )
        self.assertEqual(
            utils.eoy(datetime.date(2019, 11, 4), 0), datetime.date(2019, 12, 31)
        )
        self.assertEqual(
            utils.eoy(datetime.date(2019, 11, 4), 1), datetime.date(2020, 12, 31)
        )
        self.assertEqual(
            utils.eoy(datetime.date(2019, 11, 4), -1), datetime.date(2018, 12, 31)
        )

    def test_parse(self):
        self.assertTrue(utils.parse("05/03/2019"), datetime.date(2019, 5, 3))

    def test_offset(self):
        today = datetime.date(2020, 1, 10)  # Friday

        # by days
        self.assertEqual(utils.offset(today, days=+1), datetime.date(2020, 1, 11))
        self.assertEqual(utils.offset(today, days=-1), datetime.date(2020, 1, 9))

        # by weekdays
        self.assertEqual(
            utils.offset(today, weekdays=+1), datetime.date(2020, 1, 13)
        )  # Monday
        self.assertEqual(
            utils.offset(today, weekdays=-1), datetime.date(2020, 1, 9)
        )  # Thursday

        # by weeks
        self.assertEqual(utils.offset(today, weeks=+1), datetime.date(2020, 1, 17))
        self.assertEqual(utils.offset(today, weeks=-1), datetime.date(2020, 1, 3))

        # by months
        self.assertEqual(utils.offset(today, months=+1), datetime.date(2020, 2, 10))
        self.assertEqual(utils.offset(today, months=-1), datetime.date(2019, 12, 10))

        self.assertEqual(
            utils.offset(datetime.date(2020, 1, 31), months=+1),
            datetime.date(2020, 2, 29),
        )  # 2020 is a leap year

        self.assertEqual(
            utils.offset(datetime.date(2020, 1, 31), months=+1, handle=0),
            datetime.date(2020, 2, 29),
        )  # 2020 is a leap year

        self.assertEqual(
            utils.offset(datetime.date(2020, 1, 31), months=+1, handle=1),
            datetime.date(2020, 3, 1),
        )  # 2020 is a leap year

        self.assertEqual(
            utils.offset(datetime.date(2019, 1, 31), months=+1, handle=1),
            datetime.date(2019, 3, 1),
        )  # 2019 is not a leap year

        self.assertEqual(
            utils.offset(
                datetime.date(2020, 1, 31), months=+1, handle=lambda eom, days: 0
            ),
            datetime.date(2020, 2, 29),
        )  # 2020 is a leap year

        self.assertEqual(
            utils.offset(
                datetime.date(2020, 1, 31), months=+1, handle=lambda eom, days: 1
            ),
            datetime.date(2020, 3, 1),
        )  # 2020 is a leap year

        self.assertEqual(
            utils.offset(
                datetime.date(2020, 1, 31), months=+1, handle=lambda eom, days: days
            ),
            datetime.date(2020, 3, 2),
        )  # 2020 is a leap year

        self.assertEqual(
            utils.offset(
                datetime.date(2019, 1, 31), months=+1, handle=lambda eom, days: days
            ),
            datetime.date(2019, 3, 3),
        )  # note this example carefully!

        # by years
        self.assertEqual(utils.offset(today, years=1), datetime.date(2021, 1, 10))

        # exception handling
        self.assertEqual(
            utils.offset(datetime.date(2020, 2, 29), years=-1),
            datetime.date(2019, 2, 28),
        )

        self.assertEqual(
            utils.offset(datetime.date(2020, 2, 29), years=-1, handle=0),
            datetime.date(2019, 2, 28),
        )

        self.assertEqual(
            utils.offset(datetime.date(2020, 2, 29), years=-1, handle=1),
            datetime.date(2019, 3, 1),
        )

        self.assertEqual(
            utils.offset(
                datetime.date(2020, 2, 29), years=-1, handle=lambda eom, days: days
            ),
            datetime.date(2019, 3, 1),
        )

    def test_dayof(self):
        self.assertEqual(utils.dayof("M", datetime.date(2020, 2, 29)), 29)
        self.assertEqual(utils.dayof("M", datetime.date(2020, 2, 29), base=0), 28)
        self.assertEqual(utils.dayof("Q", datetime.date(2020, 2, 29)), 60)
        self.assertEqual(utils.dayof("Q", datetime.date(2020, 2, 29), base=0), 59)
        self.assertEqual(utils.dayof("Y", datetime.date(2020, 2, 29)), 60)
        self.assertEqual(utils.dayof("Y", datetime.date(2020, 2, 29), base=0), 59)

        dates = load()

        self.assertEqual(
            utils.dayof("M", calendar=dates, base=0)[datetime.date(2014, 11, 17)], 0
        )
        self.assertEqual(
            utils.dayof("M", calendar=dates, base=1)[datetime.date(2014, 11, 17)], 1
        )
        self.assertEqual(
            utils.dayof("M", calendar=dates, base=0)[datetime.date(2014, 12, 1)], 0
        )
        self.assertEqual(
            utils.dayof("M", calendar=dates, base=1)[datetime.date(2014, 12, 1)], 1
        )
        self.assertEqual(
            utils.dayof("M", calendar=dates, base=1)[datetime.date(2016, 7, 29)], 20
        )
        self.assertEqual(
            utils.dayof("Y", calendar=dates, base=1)[datetime.date(2019, 11, 15)], 222
        )

        try:
            for date, position in zip(dates, utils.dayof("Q", calendar=dates)):
                pass
        except Exception as e:
            self.fail(f"Failed to iterate over dayof ({e})")

    def test_daysfrom(self):
        self.assertEqual(utils.daysfrom("MS", datetime.date(2020, 2, 29)), 28)
        self.assertEqual(utils.daysfrom("QS", datetime.date(2020, 2, 29)), 59)
        self.assertEqual(utils.daysfrom("YS", datetime.date(2020, 2, 29)), 59)

        dates = load()

        self.assertEqual(
            utils.daysfrom("MS", calendar=dates)[datetime.date(2014, 11, 17)], 0
        )
        self.assertEqual(
            utils.daysfrom("MS", calendar=dates)[datetime.date(2014, 11, 17)], 0
        )
        self.assertEqual(
            utils.daysfrom("MS", calendar=dates)[datetime.date(2014, 12, 1)], 0
        )
        self.assertEqual(
            utils.daysfrom("MS", calendar=dates)[datetime.date(2014, 12, 1)], 0
        )
        self.assertEqual(
            utils.daysfrom("MS", calendar=dates)[datetime.date(2016, 7, 29)], 19
        )
        self.assertEqual(
            utils.daysfrom("YS", calendar=dates)[datetime.date(2019, 11, 15)], 221
        )

        try:
            for date, position in zip(dates, utils.daysfrom("QS", calendar=dates)):
                pass
        except Exception as e:
            self.fail(f"Failed to iterate over dayof ({e})")

    def test_daysto(self):
        self.assertEqual(utils.daysto("ME", datetime.date(2020, 2, 29)), 0)
        self.assertEqual(utils.daysto("QE", datetime.date(2020, 2, 29)), 31)
        self.assertEqual(utils.daysto("YE", datetime.date(2020, 2, 29)), 306)

        dates = load()

        self.assertEqual(
            utils.daysto("ME", calendar=dates)[datetime.date(2014, 11, 17)], 8
        )
        self.assertEqual(
            utils.daysto("ME", calendar=dates)[datetime.date(2014, 12, 1)], 21
        )
        self.assertEqual(
            utils.daysto("ME", calendar=dates)[datetime.date(2016, 7, 29)], 0
        )
        self.assertEqual(
            utils.daysto("YE", calendar=dates)[datetime.date(2019, 11, 15)], 0
        )

        try:
            for date, position in zip(dates, utils.daysto("QE", calendar=dates)):
                pass
        except Exception as e:
            self.fail(f"Failed to iterate over dayof ({e})")

    def test_weekdayof(self):
        assert utils.weekdayof("Y", datetime.date(2020, 1, 27)) == 4

        assert utils.weekdayof("Y", datetime.date(2020, 6, 17)) == 25

        assert utils.weekdayof("M", datetime.date(2020, 3, 31)) == 5

    def test_next(self):
        assert utils.next("MON", asof=datetime.date(2021, 12, 5)) == datetime.date(
            2021, 12, 6
        )

        assert utils.next("TUE", asof=datetime.date(2021, 12, 5)) == datetime.date(
            2021, 12, 7
        )

        assert utils.next("SUN", asof=datetime.date(2021, 12, 5)) == datetime.date(
            2021, 12, 12
        )

    def test_last(self):
        assert utils.last("MON", asof=datetime.date(2021, 12, 5)) == datetime.date(
            2021, 11, 29
        )

        assert utils.last("SUN", asof=datetime.date(2021, 12, 5)) == datetime.date(
            2021, 11, 28
        )
