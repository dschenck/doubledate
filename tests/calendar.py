import pytest
import datetime
import doubledate as dtwo


def test_generate():
    calendar = dtwo.Calendar.generate(
        datetime.date(2021, 1, 1), datetime.date(2021, 12, 31)
    )

    assert len(calendar) == 365
    assert calendar[0] == datetime.date(2021, 1, 1)
    assert calendar[-1] == datetime.date(2021, 12, 31)

    calendar = dtwo.Calendar.generate(
        datetime.date(2021, 1, 1), datetime.date(2021, 1, 1)
    )

    assert len(calendar) == 1
    assert calendar[0] == calendar[-1] == datetime.date(2021, 1, 1)

    # test if starting > ending date
    calendar = dtwo.Calendar.generate(
        datetime.date(2021, 12, 31), datetime.date(2021, 1, 1)
    )

    assert len(calendar) == 0


def test_indexing():
    cal = dtwo.Calendar(
        [datetime.date(2019, 1, 1) + datetime.timedelta(i) for i in range(45)]
    )

    assert cal[0] == datetime.date(2019, 1, 1)
    assert cal[-1] == datetime.date(2019, 2, 14)
    assert cal[0:31][-1] == datetime.date(2019, 1, 31)
    assert cal[:31][0] == datetime.date(2019, 1, 1)


def test_slicing():
    dates = [
        datetime.date(2019, 8, 15),
        datetime.date(2019, 8, 16),
        datetime.date(2019, 8, 19),
        datetime.date(2019, 8, 20),
    ]

    calendar = dtwo.Calendar(dates)

    assert calendar[0:2] == dtwo.Calendar(
        [datetime.date(2019, 8, 15), datetime.date(2019, 8, 16)]
    )
    assert calendar[-2:] == dtwo.Calendar(
        [datetime.date(2019, 8, 19), datetime.date(2019, 8, 20)]
    )
    assert calendar[datetime.date(2019, 8, 1) :] == calendar
    assert calendar[datetime.date(2019, 8, 15) :][0] == datetime.date(2019, 8, 15)
    assert calendar[datetime.date(2019, 8, 17) :][0] == datetime.date(2019, 8, 19)

    assert calendar[: datetime.date(2019, 8, 18)][-1] == datetime.date(2019, 8, 16)
    assert calendar[: datetime.date(2019, 8, 19)][-1] == datetime.date(2019, 8, 19)
    assert calendar[: datetime.date(2019, 8, 22)][-1] == datetime.date(2019, 8, 20)

    assert len(calendar[datetime.date(2019, 8, 21) :]) == 0
    assert len(calendar[: datetime.date(2019, 8, 1)]) == 0


def test_first_last():
    dates = [
        datetime.date(2019, 8, 15),
        datetime.date(2019, 8, 16),
        datetime.date(2019, 8, 19),
        datetime.date(2019, 8, 20),
    ]
    cdr = dtwo.Calendar(dates)

    assert cdr.first == datetime.date(2019, 8, 15)
    assert cdr.last == datetime.date(2019, 8, 20)


def test_filter():
    dates = [
        datetime.date(2019, 8, 15),
        datetime.date(2019, 8, 16),
        datetime.date(2019, 8, 19),
        datetime.date(2019, 8, 20),
    ]
    cdr = dtwo.Calendar(dates)

    assert cdr.filter(weekday=4) == dtwo.Calendar([datetime.date(2019, 8, 16)])


def test_groupby():
    dates = [
        datetime.date(2019, 8, 15),
        datetime.date(2019, 8, 16),
        datetime.date(2019, 8, 19),
        datetime.date(2019, 8, 20),
    ]

    cdr = dtwo.Calendar(dates)

    assert cdr.groupby("W").first() == dtwo.Calendar([dates[0], dates[2]])
    assert cdr.groupby("M").first() == dtwo.Calendar([dates[0]])
    assert cdr.groupby("Y").last() == dtwo.Calendar([dates[-1]])

    assert (
        cdr.groupby("W").apply(lambda c: c[0:1]).combine()
        == dtwo.Calendar(dates[0:1] + dates[2:3]),
    )

    assert (
        cdr.groupby("W").apply(lambda c: c[0]).combine()
        == dtwo.Calendar(dates[0:1] + dates[2:3]),
    )


def test_fa():
    dates = [
        datetime.date(2019, 8, 15),
        datetime.date(2019, 8, 16),
        datetime.date(2019, 8, 19),
        datetime.date(2019, 8, 20),
    ]
    cdr = dtwo.Calendar(dates)

    assert cdr.fa(datetime.date(2019, 8, 16)) == datetime.date(2019, 8, 19)
    assert cdr.fa(datetime.date(2019, 8, 17)) == datetime.date(2019, 8, 19)
    assert cdr.fa(datetime.date(2019, 8, 1)) == datetime.date(2019, 8, 15)
    assert cdr.fa(datetime.date(2019, 9, 1), None) == None


def test_lb():
    dates = [
        datetime.date(2019, 8, 15),
        datetime.date(2019, 8, 16),
        datetime.date(2019, 8, 19),
        datetime.date(2019, 8, 20),
    ]
    cdr = dtwo.Calendar(dates)

    assert cdr.lb(datetime.date(2019, 8, 16)) == datetime.date(2019, 8, 15)
    assert cdr.lb(datetime.date(2019, 8, 17)) == datetime.date(2019, 8, 16)
    assert cdr.lb(datetime.date(2019, 8, 30)) == datetime.date(2019, 8, 20)
    assert cdr.lb(datetime.date(2019, 8, 1), None) == None


def test_contains():
    dates = [
        datetime.date(2019, 8, 15),
        datetime.date(2019, 8, 16),
        datetime.date(2019, 8, 19),
        datetime.date(2019, 8, 20),
    ]
    cdr = dtwo.Calendar(dates)

    assert dates[0] in cdr

    assert dates[-1] in cdr

    assert not (datetime.date(2019, 8, 17) in cdr)


def test_dayof():
    dates = [
        datetime.date(2019, 7, 14),
        datetime.date(2019, 7, 29),
        datetime.date(2019, 8, 15),
        datetime.date(2019, 8, 16),
        datetime.date(2019, 8, 19),
        datetime.date(2019, 8, 20),
    ]

    cdr = dtwo.Calendar(dates)

    assert cdr.dayof("M")[dates[0]] == 1
    assert cdr.dayof("M")[dates[1]] == 2
    assert cdr.dayof("M")[dates[3]] == 2
    assert cdr.dayof("Y")[dates[3]] == 4
    assert cdr.dayof("W")[dates[4]] == 1
    assert cdr.dayof("W")[dates[-1]] == 2


def test_setmethods():
    c1 = dtwo.Calendar(
        [
            datetime.date(2019, 7, 14),
            datetime.date(2019, 7, 29),
            datetime.date(2019, 8, 15),
            datetime.date(2019, 8, 16),
            datetime.date(2019, 8, 19),
        ]
    )

    c2 = dtwo.Calendar(
        [
            datetime.date(2019, 7, 14),
            datetime.date(2019, 7, 20),
            datetime.date(2019, 8, 15),
            datetime.date(2019, 8, 17),
            datetime.date(2019, 8, 19),
        ]
    )

    assert c1.union(c2) == dtwo.Calendar(set(c1.dates).union(c2.dates))

    assert c1.intersection(c2) == dtwo.Calendar(
        set(c1.dates).intersection(set(c2.dates))
    )


def test_snap():
    dates = [
        datetime.date(2019, 7, 14),
        datetime.date(2019, 7, 29),
        datetime.date(2019, 8, 15),
        datetime.date(2019, 8, 16),
        datetime.date(2019, 8, 19),
        datetime.date(2019, 8, 20),
    ]
    cdr = dtwo.Calendar(dates)

    refdates = [
        datetime.date(2019, 7, 14),
        datetime.date(2019, 7, 20),
        datetime.date(2019, 8, 15),
        datetime.date(2019, 8, 17),
        datetime.date(2019, 8, 19),
        datetime.date(2019, 8, 20),
    ]
    ref = dtwo.Calendar(refdates)

    snapped = cdr.snap(ref)

    assert list(snapped) == [dates[0], dates[2], dates[4], dates[5]]

    snapped = cdr.snap(ref, fallback="next")

    assert (
        list(snapped)
        == [refdates[0], refdates[2], refdates[3], refdates[4], refdates[5]],
    )

    snapped = cdr.snap(ref, fallback="previous")

    assert (
        list(snapped)
        == [refdates[0], refdates[1], refdates[2], refdates[4], refdates[5]],
    )


def test_asof(calendar):
    # a normal, open Monday
    assert calendar.asof(datetime.date(2019, 10, 21)) == datetime.date(2019, 10, 21)

    # saturday 21/10/2019
    assert calendar.asof(datetime.date(2019, 10, 19)) == datetime.date(2019, 10, 18)

    # sunday 20/10/2019
    assert calendar.asof(datetime.date(2019, 10, 20)) == datetime.date(2019, 10, 18)

    # a date way past the last date of the calendar
    assert calendar.asof(datetime.date(2019, 12, 31)) == datetime.date(2019, 11, 15)

    # a date way before the first date
    with pytest.raises(Exception):
        calendar.asof(datetime.date(2000, 1, 1))


def test_daysfrom(calendar):
    assert calendar.daysfrom("YS")[datetime.date(2018, 1, 10)] == 6

    assert (
        calendar.daysfrom("WS")[datetime.date(2019, 10, 31)]
        == len(calendar[datetime.date(2019, 10, 28) : datetime.date(2019, 10, 30)]),
    )
    assert (
        calendar.daysfrom("WS")[datetime.date(2019, 10, 31)]
        == len(calendar[datetime.date(2019, 10, 28) : datetime.date(2019, 10, 30)]),
    )

    assert (
        calendar.daysfrom("MS")[datetime.date(2019, 10, 31)]
        == len(calendar[datetime.date(2019, 10, 1) : datetime.date(2019, 10, 30)]),
    )
    assert (
        calendar.daysfrom("MS")[datetime.date(2019, 10, 31)]
        == len(calendar[datetime.date(2019, 10, 1) : datetime.date(2019, 10, 30)]),
    )

    assert (
        calendar.daysfrom("QS")[datetime.date(2019, 10, 31)]
        == len(calendar[datetime.date(2019, 10, 1) : datetime.date(2019, 10, 30)]),
    )
    assert (
        calendar.daysfrom("QS")[datetime.date(2019, 10, 31)]
        == len(calendar[datetime.date(2019, 10, 1) : datetime.date(2019, 10, 30)]),
    )

    assert (
        calendar.daysfrom("HS")[datetime.date(2019, 10, 31)]
        == len(calendar[datetime.date(2019, 7, 1) : datetime.date(2019, 10, 30)]),
    )
    assert (
        calendar.daysfrom("HS")[datetime.date(2019, 10, 31)]
        == len(calendar[datetime.date(2019, 7, 1) : datetime.date(2019, 10, 30)]),
    )

    assert (
        calendar.daysfrom("YS")[datetime.date(2019, 10, 31)]
        == len(calendar[datetime.date(2019, 1, 1) : datetime.date(2019, 10, 30)]),
    )
    assert (
        calendar.daysfrom("YS")[datetime.date(2019, 10, 31)]
        == len(calendar[datetime.date(2019, 1, 1) : datetime.date(2019, 10, 30)]),
    )


def test_daysto(calendar):
    assert calendar.daysto("WE")[datetime.date(2018, 10, 31)] == 2
    assert calendar.daysto("WE")[datetime.date(2018, 10, 31)] == 2

    assert calendar.daysto("ME")[datetime.date(2018, 1, 8)] == 16
    assert calendar.daysto("ME")[datetime.date(2018, 1, 8)] == 16

    assert (
        calendar.daysto("QE")[datetime.date(2018, 5, 25)]
        == len(calendar[datetime.date(2018, 5, 26) : datetime.date(2018, 6, 30)]),
    )
    assert (
        calendar.daysto("QE")[datetime.date(2018, 5, 25)]
        == len(calendar[datetime.date(2018, 5, 26) : datetime.date(2018, 6, 30)]),
    )

    assert (
        calendar.daysto("HE")[datetime.date(2018, 5, 25)]
        == len(calendar[datetime.date(2018, 5, 26) : datetime.date(2018, 6, 30)]),
    )
    assert (
        calendar.daysto("HE")[datetime.date(2018, 5, 25)]
        == len(calendar[datetime.date(2018, 5, 26) : datetime.date(2018, 6, 30)]),
    )

    assert (
        calendar.daysto("YE")[datetime.date(2018, 5, 25)]
        == len(calendar[datetime.date(2018, 5, 26) : datetime.date(2018, 12, 31)]),
    )
    assert (
        calendar.daysto("YE")[datetime.date(2018, 5, 25)]
        == len(calendar[datetime.date(2018, 5, 26) : datetime.date(2018, 12, 31)]),
    )


def test_between(calendar):
    assert calendar.daysbetween(calendar[0], calendar[99]) == len(calendar[0:99])
    assert calendar.daysbetween(calendar[50], calendar[100], "both") == 51
    assert calendar.daysbetween(calendar[50], calendar[100], "left") == 50
    assert calendar.daysbetween(calendar[50], calendar[100], "right") == 50


def test__add__(calendar):
    # add two calendars
    combined = calendar[5:20] + calendar[10:30]
    assert isinstance(calendar, dtwo.Calendar)
    assert len(combined) == 30 - 5

    # add a date to a calendar
    combined = calendar[0:5] + calendar[5]
    assert isinstance(calendar, dtwo.Calendar)
    assert len(combined) == 6


def test_calendar_utilities(calendar):
    assert calendar.eom(datetime.date(2018, 9, 19)) == datetime.date(2018, 9, 28)
    assert calendar.som(datetime.date(2018, 9, 19)) == datetime.date(2018, 9, 4)
    assert calendar.eoq(datetime.date(2018, 9, 19)) == datetime.date(2018, 9, 28)
    assert calendar.soq(datetime.date(2018, 9, 19)) == datetime.date(2018, 7, 2)
    assert calendar.eoy(datetime.date(2018, 9, 19)) == datetime.date(2018, 12, 31)
    assert calendar.soy(datetime.date(2018, 9, 19)) == datetime.date(2018, 1, 2)
    assert calendar.eoy(datetime.date(2019, 11, 14)) == datetime.date(2019, 11, 15)
    assert calendar.eoy(datetime.date(2019, 11, 15)) == datetime.date(2019, 11, 15)
    assert calendar.soy(datetime.date(2014, 12, 22)) == datetime.date(2014, 11, 17)
    assert calendar.soy(datetime.date(2014, 11, 17)) == datetime.date(2014, 11, 17)


def test_splitter(calendar):
    assert isinstance(calendar.split(dtwo.BD(0, "M")).first(), dtwo.Calendar)
    assert isinstance(calendar.split(dtwo.BD(10, "M")).first(), dtwo.Calendar)
    assert isinstance(calendar.split(starting=dtwo.BD(10, "M")).first(), dtwo.Calendar)
    assert isinstance(calendar.split(ending=dtwo.BD(10, "M")).first(), dtwo.Calendar)

    # simply split on first day of month
    assert calendar.split(dtwo.BD(0)).first()[0] == datetime.date(2014, 11, 17)
    assert calendar.split(dtwo.BD(0)).last()[0] == datetime.date(2014, 11, 28)

    # simply split on first day of month
    assert calendar.split(starting=dtwo.BD(0)).first()[0] == datetime.date(2014, 11, 17)
    assert calendar.split(starting=dtwo.BD(0)).last()[0] == datetime.date(2014, 11, 28)

    # should be the same as splitting on last day of the month
    assert calendar.split(ending=dtwo.BD(-1)).first()[0] == datetime.date(2014, 11, 17)
    assert calendar.split(ending=dtwo.BD(-1)).last()[0] == datetime.date(2014, 11, 28)

    # simply split on first day of month
    assert calendar.split(ending=dtwo.BD(0)).first()[0] == datetime.date(2014, 11, 17)
    assert calendar.split(ending=dtwo.BD(0)).first()[1] == datetime.date(2014, 11, 18)
    assert calendar.split(ending=dtwo.BD(0)).first()[2] == datetime.date(2014, 12, 2)


def test_inversing_with_bounds():
    calendar = dtwo.Calendar(
        [datetime.date(2022, 1, 17), datetime.date(2022, 2, 14)]
    ).inverse(datetime.date(2022, 1, 1), datetime.date(2022, 12, 31))

    assert calendar[0] == datetime.date(2022, 1, 1)
    assert calendar[-1] == datetime.date(2022, 12, 31)

    assert datetime.date(2022, 1, 17) not in calendar
    assert datetime.date(2022, 2, 14) not in calendar
    assert len(calendar) == 365 - 2

    # test with starting date equal to a holiday
    calendar = dtwo.Calendar(
        [datetime.date(2022, 1, 17), datetime.date(2022, 2, 14)]
    ).inverse(datetime.date(2022, 1, 17), datetime.date(2022, 12, 31))

    assert calendar[0] == datetime.date(2022, 1, 18)


def test_inversing_with_no_bounds():
    calendar = dtwo.Calendar(
        [datetime.date(2022, 1, 17), datetime.date(2022, 2, 14)]
    ).inverse()

    assert calendar[0] == datetime.date(2022, 1, 18)
    assert calendar[-1] == datetime.date(2022, 2, 13)


def test_equals():
    calendar = dtwo.Calendar([datetime.date(2022, 1, 17), datetime.date(2022, 2, 14)])

    assert calendar == calendar
    assert calendar == [datetime.date(2022, 1, 17), datetime.date(2022, 2, 14)]
    assert calendar == {datetime.date(2022, 1, 17), datetime.date(2022, 2, 14)}
    assert calendar != [datetime.date(2022, 1, 18), datetime.date(2022, 2, 14)]
    assert calendar != False
    assert calendar != "a string"
    assert calendar != 1


def test_apply(calendar):
    assert isinstance(
        calendar.apply(lambda date: datetime.datetime(date.year, date.month, 1)),
        dtwo.Calendar,
    )

    assert isinstance(calendar.apply(lambda date: date.year), list)


def test_resample_calendar_by_weekday(calendar):
    groups = calendar.resample("W-MON")
    assert all(len(week) < 7 for week in groups)
    assert groups.calendars[-1][0] == datetime.date(2019, 11, 12)  # Tuesday

    dates = calendar.resample("W-TUE").first()
    assert dates[-1] == datetime.date(2019, 11, 13)  # Wednesday


def test_join():
    cdr1 = dtwo.Calendar(
        [
            datetime.date(2019, 7, 13),
            datetime.date(2019, 7, 29),
            datetime.date(2019, 8, 15),
            datetime.date(2019, 8, 16),
            datetime.date(2019, 8, 19),
            datetime.date(2019, 8, 20),
        ]
    )

    cdr2 = dtwo.Calendar(
        [
            datetime.date(2019, 7, 14),
            datetime.date(2019, 7, 29),
            datetime.date(2019, 8, 15),
            datetime.date(2019, 8, 16),
            datetime.date(2019, 8, 17),
            datetime.date(2019, 8, 21),
            datetime.date(2019, 8, 22),
            datetime.date(2019, 8, 23),
        ]
    )

    join = cdr1.join(cdr2)

    assert datetime.date(2019, 7, 13) in join
    assert datetime.date(2019, 7, 14) not in join

    assert datetime.date(2019, 8, 17) not in join
    assert datetime.date(2019, 8, 23) in join

    join = cdr1.join(cdr2, on=datetime.date(2019, 8, 1))

    assert datetime.date(2019, 7, 13) in join
    assert datetime.date(2019, 7, 14) not in join

    assert datetime.date(2019, 8, 17) in join
    assert datetime.date(2019, 8, 20) not in join


def test_create():
    cdr = dtwo.Calendar.create(
        freq="D", starting=datetime.date(2020, 1, 1), ending=datetime.date(2023, 12, 31)
    )
    assert len(cdr) == 4 * 365 + 1
