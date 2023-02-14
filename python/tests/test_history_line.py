from datetime import date, time

import pytest

from mj import HistoryLine


def test_eq():
    a = HistoryLine("2022-07-31T01:51:05-0400 easy 308")
    b = HistoryLine("2022-07-31T01:51:05-0400 easy " + str(300 + 8))
    assert a == b


@pytest.mark.parametrize("seconds,expected", [
    (60 * 60 * 24 - 1, "23:59:59"),     # all day
    (0, "00:00"),                       # empty
    (3603, "01:00:03"),                 # hour plus
    (60, "01:00"),                      # one minute
    (2, "00:02"),                       # two seconds
])
def test_format_time(seconds, expected):
    assert HistoryLine.format_time(seconds) == expected


def test_game_date():
    line = "2019-11-30T20:05:00-0500 Normal 234"
    h = HistoryLine(line)
    assert h.game_date.date() == date(2019, 11, 30)
    assert h.game_date.time() == time(20, 5, 0)


def test_repr():
    line = "2019-11-25T12:21:58-0500 cloud 3603"
    history = HistoryLine(line)
    assert repr(history) == f'HistoryLine("{line}")'


def test_str_9_30():
    line = "2019-11-25T12:21:58-0500 cloud 570"
    history = HistoryLine(line)
    assert str(history) == "2019-11-25 cloud 09:30"


def test_str_hour_plus():
    line = "2019-11-25T12:21:58-0500 cloud 3603"
    history = HistoryLine(line)
    assert str(history) == "2019-11-25 cloud 01:00:03"


def test_timedate_normal():
    line = "2019-11-30T20:05:00-0500 Normal 234"
    h = HistoryLine(line)
    assert h.timedate() == "03:54 (2019-11-30)"
