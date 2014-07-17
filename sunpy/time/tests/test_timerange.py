# -*- coding: utf-8 -*-

from __future__ import absolute_import

import datetime
import pytest
import sunpy.time

tbegin_str = '2012/1/1'
tfin_str = '2012/1/2'
dt_int = 24 * 60 * 60

start = sunpy.time.parse_time(tbegin_str)
end = sunpy.time.parse_time(tfin_str)
delta = end - start


@pytest.mark.parametrize("inputs", [
    (tbegin_str, tfin_str),
    (tbegin_str, dt_int),
    (tbegin_str, datetime.timedelta(days=1))
])
def test_timerange_inputs(inputs):
    timerange = sunpy.time.TimeRange(*inputs)
    assert isinstance(timerange, sunpy.time.TimeRange)
    assert timerange.start == start
    assert timerange.end == end
    assert timerange.dt == delta


@pytest.mark.parametrize("ainput", [
    (tbegin_str, tfin_str),
    (tbegin_str, dt_int),
    (tbegin_str, datetime.timedelta(days=1)),
    (sunpy.time.TimeRange(tbegin_str, tfin_str))
    ])
def test_timerange_input(ainput):
    timerange = sunpy.time.TimeRange(ainput)
    assert isinstance(timerange, sunpy.time.TimeRange)
    assert timerange.start == start
    assert timerange.end == end
    assert timerange.dt == delta


def test_center():
    timerange = sunpy.time.TimeRange(tbegin_str, tfin_str)
    assert timerange.center() == datetime.datetime(year=2012, day=1, month=1,
                                                   hour=12)


def test_split():
    timerange = sunpy.time.TimeRange(tbegin_str, tfin_str)
    expect = [sunpy.time.TimeRange('2012/1/1T00:00:00', '2012/1/1T12:00:00'),
              sunpy.time.TimeRange('2012/1/1T12:00:00', '2012/1/2T00:00:00')]
    split = timerange.split(n=2)
    #Doing direct comparisons seem to not work
    assert all([wi.start == ex.start and wi.end == ex.end for wi, ex in zip(split, expect)])


def test_split_n_0():
    timerange = sunpy.time.TimeRange(tbegin_str, tfin_str)
    with pytest.raises(ValueError):
        timerange.split(n=0)


def test_window():
    timerange = sunpy.time.TimeRange(tbegin_str, tfin_str)
    window = timerange.window(12 * 60 * 60, 10)
    expect = [sunpy.time.TimeRange('2012/1/1T00:00:00', '2012/1/1T00:00:10'),
              sunpy.time.TimeRange('2012/1/1T12:00:00', '2012/1/1T12:00:10'),
              sunpy.time.TimeRange('2012/1/2T00:00:00', '2012/1/2T00:00:10')]
    assert isinstance(window, list)
    #Doing direct comparisons seem to not work
    assert all([wi.start == ex.start and wi.end == ex.end for wi, ex in zip(window, expect)])


def test_window_timedelta():
    timerange = sunpy.time.TimeRange(tbegin_str,tfin_str)
    window = timerange.window(datetime.timedelta(hours=12), datetime.timedelta(seconds=10))
    expect = [sunpy.time.TimeRange('2012/1/1T00:00:00', '2012/1/1T00:00:10'),
              sunpy.time.TimeRange('2012/1/1T12:00:00', '2012/1/1T12:00:10'),
              sunpy.time.TimeRange('2012/1/2T00:00:00', '2012/1/2T00:00:10')]
    assert isinstance(window, list)
    #Doing direct comparisons seem to not work
    assert all([wi.start == ex.start and wi.end == ex.end for wi, ex in zip(window, expect)])


def test_days():
    timerange = sunpy.time.TimeRange(tbegin_str, tfin_str)
    assert timerange.days() == 1


def test_start():
    timerange = sunpy.time.TimeRange(tbegin_str, tfin_str)
    assert timerange.start == start


def test_end():
    timerange = sunpy.time.TimeRange(tbegin_str, tfin_str)
    assert timerange.end == end


def test_seconds():
    timerange = sunpy.time.TimeRange(tbegin_str, tfin_str)
    assert timerange.seconds() == dt_int


def test_minutes():
    timerange = sunpy.time.TimeRange(tbegin_str, tfin_str)
    assert timerange.minutes() == 24 * 60


def test_next():
    timerange = sunpy.time.TimeRange(tbegin_str, tfin_str)
    timerange.next()
    assert isinstance(timerange, sunpy.time.TimeRange)
    assert timerange.start == start + delta
    assert timerange.end == end + delta
    assert timerange.dt == delta


def test_previous():
    timerange = sunpy.time.TimeRange(tbegin_str, tfin_str)
    timerange.previous()
    assert isinstance(timerange, sunpy.time.TimeRange)
    assert timerange.start == start - delta
    assert timerange.end == end - delta
    assert timerange.dt == delta


def test_extend():
    timerange = sunpy.time.TimeRange(tbegin_str, tfin_str)
    timerange.extend(delta, delta)
    assert isinstance(timerange, sunpy.time.TimeRange)
    assert timerange.start == start + delta
    assert timerange.end == end + delta
    assert timerange.dt == delta


def test_contains():
    before = datetime.datetime(year=1990, month=1, day=1)
    after = datetime.datetime(year=2022, month=1, day=1)
    between = datetime.datetime(year=2014, month=5, day=4)
    timerange = sunpy.time.TimeRange('2014/05/03 12:00', '2014/05/05 21:00')
    assert between in timerange
    assert before not in timerange
    assert after not in timerange
    assert timerange.start in timerange
    assert timerange.end in timerange
    assert '2014/05/04 15:21' in timerange
    assert '1975/4/13' not in timerange
    assert '2100/1/1'not in timerange
    assert '2014/05/03 12:00' in timerange
    assert '2014/05/05 21:00' in timerange


@pytest.mark.parametrize("ainput", [
    (tbegin_str, tfin_str),
    (tfin_str, -dt_int),
    (tfin_str, tbegin_str)
    ])
def test_start_lessthan_end(ainput):
    """Test that the start and end time for a timerange is always in the
    right order"""
    timerange = sunpy.time.TimeRange(ainput)
    t1 = timerange.start
    t2 = timerange.end
    assert t1 < t2
    assert timerange.start == start
    assert timerange.end == end