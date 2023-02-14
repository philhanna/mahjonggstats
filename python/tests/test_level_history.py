import pytest

from mj import HistoryLine, LevelHistory
from tests import testdata


@pytest.fixture
def level_history():
    record_list = [
        hl
        for hl in [HistoryLine(line) for line in testdata.splitlines()]
        if hl.level_name == 'easy'
    ]
    lh = LevelHistory("easy", record_list)
    return lh


def test_bad_eq(level_history):
    """Tests the specific ways the __eq__ test can fail (for better unit test coverage)"""

    # First way to fail: not the same type
    assert level_history != "bogus"

    # Second way to fail: different level names
    lh = LevelHistory("difficult", [
        hl
        for hl in [HistoryLine(line) for line in testdata.splitlines()]
        if hl.level_name == 'difficult'
    ])
    assert level_history != lh

    # Third way to fail: different number of records
    lh = LevelHistory("easy", [
                                  hl
                                  for hl in [HistoryLine(line) for line in testdata.splitlines()]
                                  if hl.level_name == 'easy'
                              ][1:])  # Delete the last record
    assert level_history != lh

    # Fourth way to fail: same number of records but some different
    lh = LevelHistory("easy", [
        hl
        for hl in [HistoryLine(line) for line in ("2021" + testdata[4:]).splitlines()]
        if hl.level_name == 'easy'
    ])  # First record year set to 2021
    assert level_history != lh


def test_confidence(level_history):
    assert level_history.confidence == pytest.approx((132.51162, 375.48838))


def test_confidence_lo_zero():
    """Tests that lower bound of 95% confidence is zero, rather than negative"""
    lotestdata = """\
2022-07-31T01:51:05-0400 easy 8
2022-08-04T22:27:39-0400 easy 43
2022-08-05T23:50:36-0400 difficult 18
2022-08-06T22:57:13-0400 ziggurat 28
2022-08-06T23:02:17-0400 easy 1
2022-08-06T23:07:24-0400 easy 4"""
    record_list = [
        hl
        for hl in [HistoryLine(line) for line in lotestdata.splitlines()]
        if hl.level_name == 'easy'
    ]
    lh = LevelHistory("easy", record_list)
    assert lh.confidence[0] == 0


def test_count(level_history):
    assert len(level_history.records) == 4


def test_good_eq(level_history):
    lh = LevelHistory("easy", [
        hl
        for hl in [HistoryLine(line) for line in testdata.splitlines()]
        if hl.level_name == 'easy'
    ])
    assert lh == level_history


def test_level_name(level_history):
    assert level_history.level_name == "easy"


def test_mean(level_history):
    assert level_history.mean == 254


def test_records(level_history):
    expected = [
        HistoryLine("2022-07-31T01:51:05-0400 easy 308"),
        HistoryLine("2022-08-04T22:27:39-0400 easy 243"),
        HistoryLine("2022-08-06T23:02:17-0400 easy 171"),
        HistoryLine("2022-08-06T23:07:24-0400 easy 294"),
    ]
    actual = [x for x in level_history.records if x.level_name == 'easy']
    assert actual == expected


def test_repr(level_history):
    actual = repr(level_history)
    expected = "".join([
        'LevelHistory',
        '(',
        '"easy"',
        ',',
        '[',
        repr(HistoryLine("2022-07-31T01:51:05-0400 easy 308")),
        ',',
        repr(HistoryLine("2022-08-04T22:27:39-0400 easy 243")),
        ',',
        repr(HistoryLine("2022-08-06T23:02:17-0400 easy 171")),
        ',',
        repr(HistoryLine("2022-08-06T23:07:24-0400 easy 294")),
        ']',
        ')',
    ])
    assert actual == expected


def test_standard_deviation(level_history):
    assert level_history.standard_deviation == pytest.approx(61.98386)
