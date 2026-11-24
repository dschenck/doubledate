import datetime
import doubledate as dtwo


def test_index(calendar):
    assert datetime.date(2014, 12, 16) in calendar.groupby("M")
    assert datetime.date(2014, 12, 25) not in calendar.groupby("M")


def test_collection_from_generator(calendar):
    collection = dtwo.calendar.Collection(group for group in calendar.groupby("M"))
    assert len(collection) == len(calendar.groupby("M"))
