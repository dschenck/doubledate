import pytest
import doubledate as dtwo
import datetime


def test_today():
    assert dtwo.today() == datetime.date.today()


def test_tomorrow():
    assert dtwo.tomorrow() == datetime.date.today() + datetime.timedelta(days=1)


def test_yesterday():
    assert dtwo.yesterday() == datetime.date.today() - datetime.timedelta(days=1)


def test_last_weekday_default():
    # last returns a date stricty before today; can never be today
    assert dtwo.today() > dtwo.last("MON")
    assert dtwo.today() - datetime.timedelta(days=7) <= dtwo.last("MON")


@pytest.mark.parametrize(
    ("date", "semester"),
    [
        (datetime.date(2019, 1, 1), 1),
        (datetime.date(2019, 6, 30), 1),
        (datetime.date(2019, 7, 1), 2),
        (datetime.date(2019, 12, 31), 2),
    ],
)
def test_semester(date, semester):
    assert dtwo.semester(date) == semester


@pytest.mark.parametrize(
    ("date", "quarter"),
    [
        (datetime.date(2019, 1, 1), 1),
        (datetime.date(2019, 6, 30), 2),
        (datetime.date(2019, 7, 1), 3),
        (datetime.date(2019, 12, 31), 4),
    ],
)
def test_quarter(date, quarter):
    assert dtwo.quarter(date) == quarter


@pytest.mark.parametrize(
    ("date", "trimester"),
    [
        (datetime.date(2019, 1, 1), 1),
        (datetime.date(2019, 6, 30), 2),
        (datetime.date(2019, 7, 1), 2),
        (datetime.date(2019, 12, 31), 3),
    ],
)
def test_trimester(date, trimester):
    assert dtwo.trimester(date) == trimester


@pytest.mark.parametrize(
    ["date", "offset", "weekday", "eow"],
    [
        (datetime.date(2020, 1, 4), 0, "SUN", datetime.date(2020, 1, 5)),
        (datetime.date(2020, 1, 4), 1, "SUN", datetime.date(2020, 1, 12)),
        (datetime.date(2020, 1, 4), -1, "SUN", datetime.date(2019, 12, 29)),
        (datetime.date(2020, 1, 4), 0, "SAT", datetime.date(2020, 1, 4)),
        (datetime.date(2020, 1, 4), 0, "FRI", datetime.date(2020, 1, 10)),
        (datetime.date(2020, 1, 4), 0, "THU", datetime.date(2020, 1, 9)),
        (datetime.date(2020, 1, 4), 0, "WED", datetime.date(2020, 1, 8)),
        (datetime.date(2020, 1, 4), 0, "TUE", datetime.date(2020, 1, 7)),
        (datetime.date(2020, 1, 4), 0, "MON", datetime.date(2020, 1, 6)),
        (datetime.date(2019, 11, 12), 0, "TUE", datetime.date(2019, 11, 12)),
    ],
)
def test_end_of_week(date, offset, weekday, eow):
    assert dtwo.eow(date, offset=offset, weekday=weekday) == eow


def test_end_of_week_defaults():
    assert dtwo.eow(datetime.date(2020, 1, 4)), datetime.date(2020, 1, 5)
    assert dtwo.eow(datetime.date(2020, 1, 4), 0), datetime.date(2020, 1, 5)


@pytest.mark.parametrize(
    ("date", "offset", "weekday", "sow"),
    [
        (datetime.date(2020, 1, 4), 0, "SUN", datetime.date(2019, 12, 29)),
        (datetime.date(2020, 1, 4), 0, "SAT", datetime.date(2020, 1, 4)),
        (datetime.date(2020, 1, 4), 0, "FRI", datetime.date(2020, 1, 3)),
        (datetime.date(2020, 1, 4), 0, "THU", datetime.date(2020, 1, 2)),
        (datetime.date(2020, 1, 4), 0, "WED", datetime.date(2020, 1, 1)),
        (datetime.date(2020, 1, 4), 0, "TUE", datetime.date(2019, 12, 31)),
        (datetime.date(2020, 1, 4), 0, "MON", datetime.date(2019, 12, 30)),
    ],
)
def test_start_of_week(date, offset, weekday, sow):
    assert dtwo.sow(date, offset=offset, weekday=weekday) == sow


def test_start_of_week_defaults():
    assert dtwo.sow(datetime.date(2020, 1, 4)) == datetime.date(2019, 12, 30)
    assert dtwo.sow(datetime.date(2020, 1, 4), 0), datetime.date(2019, 12, 30)


@pytest.mark.parametrize(
    ("weekday", "date", "target"),
    [
        ("MON", datetime.date(2021, 12, 5), datetime.date(2021, 12, 6)),
        ("TUE", datetime.date(2021, 12, 5), datetime.date(2021, 12, 7)),
        ("SUN", datetime.date(2021, 12, 5), datetime.date(2021, 12, 12)),
    ],
)
def test_next(weekday, date, target):
    assert dtwo.next(weekday, asof=date) == target


@pytest.mark.parametrize(
    ("weekday", "date", "target"),
    [
        ("MON", datetime.date(2021, 12, 5), datetime.date(2021, 11, 29)),
        ("SUN", datetime.date(2021, 12, 5), datetime.date(2021, 11, 28)),
    ],
)
def test_last(weekday, date, target):
    assert dtwo.last(weekday, asof=date) == target


@pytest.mark.parametrize(
    ("frequency", "date", "target"),
    [
        ("Y", datetime.date(2020, 1, 27), 4),
        ("Y", datetime.date(2020, 6, 17), 25),
        ("M", datetime.date(2020, 3, 31), 5),
    ],
)
def test_weekdayof(frequency, date, target):
    assert dtwo.weekdayof(frequency=frequency, date=date) == target
    assert dtwo.weekdayof(frequency=frequency, date=date, base=1) == target
    assert dtwo.weekdayof(frequency=frequency, date=date, base=0) == target - 1


@pytest.mark.parametrize(
    ("date", "offset", "target"),
    [
        (datetime.date(2019, 6, 17), 0, datetime.date(2019, 6, 30)),
        (datetime.date(2019, 6, 17), 1, datetime.date(2019, 7, 31)),
        (datetime.date(2019, 6, 17), -1, datetime.date(2019, 5, 31)),
        (datetime.date(2016, 2, 29), 0, datetime.date(2016, 2, 29)),
        (datetime.date(2016, 2, 29), 12, datetime.date(2017, 2, 28)),
    ],
)
def test_end_of_month(date, offset, target):
    assert dtwo.eom(date, offset=offset) == target


@pytest.mark.parametrize(
    "date, offset, target",
    [
        (datetime.date(2019, 6, 17), 0, datetime.date(2019, 6, 1)),
        (datetime.date(2016, 3, 15), -1, datetime.date(2016, 2, 1)),
        (datetime.date(2015, 4, 20), 1, datetime.date(2015, 5, 1)),
    ],
)
def test_som(date, offset, target):
    assert dtwo.som(date, offset) == target


@pytest.mark.parametrize(
    "input_date, offset, expected_date",
    [
        (datetime.date(2020, 1, 4), 0, datetime.date(2020, 1, 1)),
        (datetime.date(2020, 3, 31), 0, datetime.date(2020, 1, 1)),
        (datetime.date(2020, 2, 4), 0, datetime.date(2020, 1, 1)),
        (datetime.date(2020, 2, 4), 1, datetime.date(2020, 4, 1)),
        (datetime.date(2020, 2, 4), -1, datetime.date(2019, 10, 1)),
    ],
)
def test_soq(input_date, offset, expected_date):
    result = dtwo.soq(input_date, offset)
    assert result == expected_date


@pytest.mark.parametrize(
    "input_date, offset, expected_date",
    [
        (datetime.date(2020, 1, 4), 0, datetime.date(2020, 3, 31)),
        (datetime.date(2020, 3, 31), 0, datetime.date(2020, 3, 31)),
        (datetime.date(2020, 1, 4), 0, datetime.date(2020, 3, 31)),
        (datetime.date(2020, 1, 4), 1, datetime.date(2020, 6, 30)),
        (datetime.date(2020, 1, 4), -1, datetime.date(2019, 12, 31)),
    ],
)
def test_eoq(input_date, offset, expected_date):
    result = dtwo.eoq(input_date, offset)
    assert result == expected_date


@pytest.mark.parametrize(
    "input_date, offset, expected_date",
    [
        (datetime.date(2019, 11, 4), 0, datetime.date(2019, 9, 1)),
        (datetime.date(2019, 11, 4), 0, datetime.date(2019, 9, 1)),
        (datetime.date(2019, 11, 4), 1, datetime.date(2020, 1, 1)),
        (datetime.date(2019, 11, 4), -1, datetime.date(2019, 5, 1)),
    ],
)
def test_sot(input_date, offset, expected_date):
    result = dtwo.sot(input_date, offset)
    assert result == expected_date


@pytest.mark.parametrize(
    "input_date, offset, expected_date",
    [
        (datetime.date(2019, 11, 4), 0, datetime.date(2019, 12, 31)),
        (datetime.date(2019, 11, 4), 0, datetime.date(2019, 12, 31)),
        (datetime.date(2019, 11, 4), 1, datetime.date(2020, 4, 30)),
        (datetime.date(2019, 11, 4), -1, datetime.date(2019, 8, 31)),
    ],
)
def test_eot(input_date, offset, expected_date):
    result = dtwo.eot(input_date, offset)
    assert result == expected_date


@pytest.mark.parametrize(
    "input_date, offset, expected_date",
    [
        (datetime.date(2019, 11, 4), 0, datetime.date(2019, 7, 1)),
        (datetime.date(2019, 11, 4), 0, datetime.date(2019, 7, 1)),
        (datetime.date(2019, 11, 4), 1, datetime.date(2020, 1, 1)),
        (datetime.date(2019, 11, 4), -1, datetime.date(2019, 1, 1)),
    ],
)
def test_sos(input_date, offset, expected_date):
    result = dtwo.sos(input_date, offset)
    assert result == expected_date


@pytest.mark.parametrize(
    "input_date, offset, expected_date",
    [
        (datetime.date(2019, 11, 4), 0, datetime.date(2019, 12, 31)),
        (datetime.date(2019, 11, 4), 0, datetime.date(2019, 12, 31)),
        (datetime.date(2019, 11, 4), 1, datetime.date(2020, 6, 30)),
        (datetime.date(2019, 11, 4), -1, datetime.date(2019, 6, 30)),
    ],
)
def test_eos(input_date, offset, expected_date):
    result = dtwo.eos(input_date, offset)
    assert result == expected_date


@pytest.mark.parametrize(
    "input_date, offset, expected_date",
    [
        (datetime.date(2019, 11, 4), 0, datetime.date(2019, 12, 31)),
        (datetime.date(2019, 11, 4), 0, datetime.date(2019, 12, 31)),
        (datetime.date(2019, 11, 4), 1, datetime.date(2020, 12, 31)),
        (datetime.date(2019, 11, 4), -1, datetime.date(2018, 12, 31)),
    ],
)
def test_eoy(input_date, offset, expected_date):
    result = dtwo.eoy(input_date, offset)
    assert result == expected_date


@pytest.mark.parametrize(
    "interval, input_date, base, expected_result",
    [
        ("M", datetime.date(2020, 2, 29), 1, 29),
        ("M", datetime.date(2020, 2, 29), 0, 28),
        ("Q", datetime.date(2020, 2, 29), 1, 60),
        ("Q", datetime.date(2020, 2, 29), 0, 59),
        ("Y", datetime.date(2020, 2, 29), 1, 60),
        ("Y", datetime.date(2020, 2, 29), 0, 59),
    ],
)
def test_dayof(interval, input_date, expected_result, base):
    result = dtwo.dayof(interval, input_date, base=base)
    assert result == expected_result


@pytest.mark.parametrize(
    ("date", "target"), [("05/03/2019", datetime.date(2019, 3, 5))]
)
def test_parse(date, target):
    assert dtwo.parse(date) == target


@pytest.mark.parametrize(
    "days, expected_date",
    [
        (+1, datetime.date(2020, 1, 11)),
        (-1, datetime.date(2020, 1, 9)),
    ],
)
def test_offset_days(days, expected_date):
    today = datetime.date(2020, 1, 10)
    result = dtwo.offset(today, days=days)
    assert result == expected_date


@pytest.mark.parametrize(
    "weekdays, expected_date",
    [
        (+1, datetime.date(2020, 1, 13)),
        (-1, datetime.date(2020, 1, 9)),
    ],
)
def test_offset_weekdays(weekdays, expected_date):
    today = datetime.date(2020, 1, 10)
    result = dtwo.offset(today, weekdays=weekdays)
    assert result == expected_date


@pytest.mark.parametrize(
    "weeks, expected_date",
    [
        (+1, datetime.date(2020, 1, 17)),
        (-1, datetime.date(2020, 1, 3)),
    ],
)
def test_offset_weeks(weeks, expected_date):
    today = datetime.date(2020, 1, 10)
    result = dtwo.offset(today, weeks=weeks)
    assert result == expected_date


@pytest.mark.parametrize(
    "months, expected_date",
    [
        (+1, datetime.date(2020, 2, 10)),
        (-1, datetime.date(2019, 12, 10)),
    ],
)
def test_offset_months(months, expected_date):
    today = datetime.date(2020, 1, 10)
    result = dtwo.offset(today, months=months)
    assert result == expected_date


@pytest.mark.parametrize(
    "years, expected_date",
    [
        (1, datetime.date(2021, 1, 10)),
    ],
)
def test_offset_years(years, expected_date):
    today = datetime.date(2020, 1, 10)
    result = dtwo.offset(today, years=years)
    assert result == expected_date


def test_offset_exceptions():
    assert dtwo.offset(datetime.date(2020, 2, 29), years=-1) == datetime.date(
        2019, 2, 28
    )


@pytest.mark.parametrize(
    "years, handle, expected_date",
    [
        (-1, 0, datetime.date(2019, 2, 28)),
        (-1, 1, datetime.date(2019, 3, 1)),
        (-1, lambda eom, days: days, datetime.date(2019, 3, 1)),
    ],
)
def test_offset_years_with_handler(years, handle, expected_date):
    result = dtwo.offset(datetime.date(2020, 2, 29), years=years, handle=handle)
    assert result == expected_date


@pytest.mark.parametrize(
    "interval, input_date, expected_result",
    [
        ("MS", datetime.date(2020, 2, 29), 28),
        ("QS", datetime.date(2020, 2, 29), 59),
        ("YS", datetime.date(2020, 2, 29), 59),
    ],
)
def test_daysfrom_and_daysto(interval, input_date, expected_result):
    result_from = dtwo.daysfrom(interval, input_date)
    assert result_from == expected_result


@pytest.mark.parametrize(
    "interval, input_date, expected_result",
    [
        ("ME", datetime.date(2020, 2, 29), 0),
        ("QE", datetime.date(2020, 2, 29), 31),
        ("YE", datetime.date(2020, 2, 29), 306),
    ],
)
def test_daysto(interval, input_date, expected_result):
    result_to = dtwo.daysto(interval, input_date)
    assert result_to == expected_result


@pytest.mark.usefixtures("calendar")
@pytest.mark.parametrize(
    ("frequency", "base", "date", "target"),
    [
        ("M", 0, datetime.date(2014, 11, 17), 0),
        ("M", 1, datetime.date(2014, 11, 17), 1),
        ("M", 0, datetime.date(2014, 12, 1), 0),
        ("M", 1, datetime.date(2014, 12, 1), 1),
        ("M", 1, datetime.date(2016, 7, 29), 20),
        ("Y", 1, datetime.date(2019, 11, 15), 222),
    ],
)
def test_dayof(calendar, frequency, base, date, target):
    assert dtwo.dayof(frequency, calendar=calendar, base=base)[date] == target


@pytest.mark.usefixtures("calendar")
@pytest.mark.parametrize(
    ("frequency", "date", "target"),
    [
        ("MS", datetime.date(2014, 11, 17), 0),
        ("MS", datetime.date(2014, 11, 17), 0),
        ("MS", datetime.date(2014, 12, 1), 0),
        ("MS", datetime.date(2014, 12, 1), 0),
        ("MS", datetime.date(2016, 7, 29), 19),
        ("YS", datetime.date(2019, 11, 15), 221),
    ],
)
def test_daysfrom(calendar, frequency, date, target):
    assert dtwo.daysfrom(frequency, calendar=calendar)[date] == target


@pytest.mark.usefixtures("calendar")
@pytest.mark.parametrize(
    ("frequency", "date", "target"),
    [
        ("ME", datetime.date(2014, 11, 17), 8),
        ("ME", datetime.date(2014, 12, 1), 21),
        ("ME", datetime.date(2016, 7, 29), 0),
        ("YE", datetime.date(2019, 11, 15), 0),
    ],
)
def test_daysto(calendar, frequency, date, target):
    assert dtwo.daysto(frequency, calendar=calendar)[date] == target
