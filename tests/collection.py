import pytest
import datetime
import doubledate as dtwo


def test_index(calendar):
    assert datetime.date(2014, 12, 16) in calendar.groupby("M")
    assert datetime.date(2014, 12, 25) not in calendar.groupby("M")
