import pytest
import datetime

from doubledate import diem


def test_instanciation():
    ann = diem(3, 31)

    with pytest.raises(TypeError):
        diem("a", 2020)

    with pytest.raises(TypeError):
        diem(10, "not a valid year")


def test_out_of_range():
    with pytest.raises(Exception):
        diem(1, 32)

    with pytest.raises(Exception):
        diem(1, 0)

    with pytest.raises(Exception):
        diem(1, 100)

    with pytest.raises(Exception):
        diem(13, 1)

    with pytest.raises(Exception):
        diem(0, 1)


def test_string_representation():
    day = diem(3, 31)
    assert str(day) == "--3-31"


def test_representation():
    day = diem(3, 31)
    assert repr(day) == 'doubledate.diem(3, 31, fold="back")'


def test_comparison():
    assert diem(3, 31) == diem(3, 31)
    assert diem(3, 31) != diem(3, 30)
    assert diem(12, 1) > diem(11, 30)
    assert diem(12, 1) >= diem(12, 1)
    assert diem(12, 1) < diem(12, 2)
    assert diem(12, 1) <= diem(12, 1)

    assert (diem(1, 1) == datetime.date(2020, 1, 1)) is False
    assert (diem(1, 1) != datetime.date(2020, 1, 1)) is True

    with pytest.raises(TypeError):
        assert diem(1, 1) > datetime.date(2020, 1, 1)

    with pytest.raises(TypeError):
        assert diem(1, 1) >= datetime.date(2020, 1, 1)

    with pytest.raises(TypeError):
        assert diem(1, 1) < datetime.date(2020, 1, 1)

    with pytest.raises(TypeError):
        assert diem(1, 1) <= datetime.date(2020, 1, 1)


def test_resolve():
    day = diem(2, 29, fold="back")
    assert day.resolve(2020) == datetime.date(2020, 2, 29)
    assert day.resolve(2019) == datetime.date(2019, 2, 28)

    day = diem(2, 29, fold="forward")
    assert day.resolve(2020) == datetime.date(2020, 2, 29)
    assert day.resolve(2019) == datetime.date(2019, 3, 1)

    day = diem(1, 31)
    assert day.resolve(2020) == datetime.date(2020, 1, 31)
    assert day.resolve(2019) == datetime.date(2019, 1, 31)

    # folds should have no impact other than on 29 Feb
    day = diem(1, 31, fold="forward")
    assert day.resolve(2020) == datetime.date(2020, 1, 31)
    assert day.resolve(2019) == datetime.date(2019, 1, 31)

    day = diem(1, 31, fold="back")
    assert day.resolve(2020) == datetime.date(2020, 1, 31)
    assert day.resolve(2019) == datetime.date(2019, 1, 31)

    # override default fold
    day = diem(2, 29, fold="forward")
    assert day.resolve(2021, fold="back") == datetime.date(2021, 2, 28)

    day = diem(2, 29, fold="back")
    assert day.resolve(2021, fold="forward") == datetime.date(2021, 3, 1)

    with pytest.raises(TypeError):
        assert diem(1, 1).resolve(year="not an integer")

    with pytest.raises(ValueError):
        assert diem(2, 29).resolve(year=2021, fold="not a valid fold")


def test_parsing():
    day = diem.parse("JAN")
    assert day.month == 1 and day.day == 31

    day = diem.parse("FEB")
    assert day.month == 2 and day.day == 29 and day.fold == "back"

    day = diem.parse("MAR")
    assert day.month == 3 and day.day == 31

    day = diem.parse("--12-03")
    assert day.month == 12 and day.day == 3

    day = diem.parse("--03-04")
    assert day.month == 3 and day.day == 4

    day == diem.parse("--3-4")
    assert day.month == 3 and day.day == 4

    day = diem.parse("Jan-31")
    assert day.month == 1 and day.day == 31

    day = diem.parse("Jan31")
    assert day.month == 1 and day.day == 31

    day = diem.parse(datetime.date(2020, 1, 4))
    assert day.month == 1 and day.day == 4


def test_last_date_before():
    date = diem(3, 31).lb(datetime.date(2020, 2, 1))
    assert date == datetime.date(2019, 3, 31)

    date = diem(3, 31).lb(datetime.date(2020, 4, 1))
    assert date == datetime.date(2020, 3, 31)

    date = diem(3, 31).lb(datetime.date(2020, 3, 31))
    assert date == datetime.date(2019, 3, 31)

    date = diem(2, 29).lb(datetime.date(2020, 3, 1))
    assert date == datetime.date(2020, 2, 29)

    date = diem(2, 29).lb(datetime.date(2019, 3, 1))
    assert date == datetime.date(2019, 2, 28)


def test_first_date_after():
    date = diem(3, 31).fa(datetime.date(2020, 2, 1))
    assert date == datetime.date(2020, 3, 31)

    date = diem(3, 31).fa(datetime.date(2020, 4, 1))
    assert date == datetime.date(2021, 3, 31)

    date = diem(3, 31).fa(datetime.date(2020, 3, 31))
    assert date == datetime.date(2021, 3, 31)

    date = diem(2, 29).fa(datetime.date(2020, 3, 1))
    assert date == datetime.date(2021, 2, 28)

    date = diem(2, 29).fa(datetime.date(2019, 3, 1))
    assert date == datetime.date(2020, 2, 29)


def test_asof():
    date = diem(3, 31).asof(datetime.date(2020, 2, 1))
    assert date == datetime.date(2019, 3, 31)

    date = diem(3, 31).asof(datetime.date(2020, 2, 1), side="left")
    assert date == datetime.date(2019, 3, 31)

    date = diem(3, 31).asof(datetime.date(2020, 2, 1), side="right")
    assert date == datetime.date(2020, 3, 31)

    date = diem(2, 29).asof(datetime.date(2020, 2, 1))
    assert date == datetime.date(2019, 2, 28)

    date = diem(2, 29).asof(datetime.date(2020, 2, 1), side="right")
    assert date == datetime.date(2020, 2, 29)

    date = diem(2, 29).asof(datetime.date(2020, 2, 29), side="right")
    assert date == datetime.date(2020, 2, 29)

    date = diem(2, 29).asof(datetime.date(2020, 2, 29), side="left")
    assert date == datetime.date(2020, 2, 29)


def test_replace():
    d = diem(3, 31).replace(month=4, day=30)
    assert d == diem(4, 30)
