from datetime import datetime

import pytest

from mj import History, HistoryLine, LevelHistory
from tests import testdata


@pytest.fixture
def history(monkeypatch):
    monkeypatch.setattr(History, 'load', lambda: testdata.splitlines())
    history = History()
    return history


def test_ordinary_load(history):
    assert len(history.records) > 4


def test_earliest_date(history):
    expected_date = datetime.strptime("2022-07-31T01:51:05-0400", '%Y-%m-%dT%H:%M:%S%z')
    actual_date = history.earliest_date
    assert actual_date == expected_date


@pytest.mark.parametrize("level_name", ["easy", "difficult", "bogus"])
def test_level_names(history, level_name):
    actual = history.get_level_history(level_name).records
    expected = [
        hl for hl in [HistoryLine(x) for x in testdata.splitlines()]
        if hl.level_name == level_name
    ]
    assert actual == expected


def test_latest_date(history):
    expected_date = datetime.strptime("2022-08-06T23:07:24-0400", '%Y-%m-%dT%H:%M:%S%z')
    actual_date = history.latest_date
    assert actual_date == expected_date


def test_names(history):
    # Note: the list of level names is sorted by the mean solution time of each level
    assert history.level_names == ['difficult', 'ziggurat', 'easy']


def test_levels(history):
    expected = {
        'difficult': LevelHistory("difficult", [
            HistoryLine("2022-08-05T23:50:36-0400 difficult 218")
        ]),
        'ziggurat': LevelHistory("ziggurat", [
            HistoryLine("2022-08-06T22:57:13-0400 ziggurat 228")
        ]),
        'easy': LevelHistory("easy", [
            HistoryLine("2022-07-31T01:51:05-0400 easy 308"),
            HistoryLine("2022-08-04T22:27:39-0400 easy 243"),
            HistoryLine("2022-08-06T23:02:17-0400 easy 171"),
            HistoryLine("2022-08-06T23:07:24-0400 easy 294"),
        ]),
    }
    actual = history.levels
    assert actual == expected


def test_records(history):
    expected = [
        HistoryLine("2022-07-31T01:51:05-0400 easy 308"),
        HistoryLine("2022-08-04T22:27:39-0400 easy 243"),
        HistoryLine("2022-08-05T23:50:36-0400 difficult 218"),
        HistoryLine("2022-08-06T22:57:13-0400 ziggurat 228"),
        HistoryLine("2022-08-06T23:02:17-0400 easy 171"),
        HistoryLine("2022-08-06T23:07:24-0400 easy 294"),
    ]
    actual = history.records
    assert actual == expected
