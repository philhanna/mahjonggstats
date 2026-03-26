# tests.domain.test_history_line
from __future__ import annotations

from datetime import datetime

import pytest

from mahjonggstats.domain.history_line import HistoryLine, date_string, format_time


def test_history_line_constructor() -> None:
    hl = HistoryLine.parse("2023-01-04T22:12:03-0500 easy 209")
    assert hl.level_name == "easy"
    assert hl.seconds == 209


def test_history_line_time_date() -> None:
    line = "2019-11-30T20:05:00-0500 Normal 234"
    hl = HistoryLine.parse(line)
    assert hl.time_date() == "03:54 (2019-11-30)"


def test_history_line_string() -> None:
    hl = HistoryLine.parse("2023-01-04T22:12:03-0500 easy 209")
    expected = 'GameDateTime="2023-01-04T22:12:03-0500", LevelName="easy", Seconds=209'
    assert str(hl) == expected


def test_history_line_game_datetime_valid() -> None:
    hl = HistoryLine.parse("2019-11-30T20:05:00-0500 Normal 234")
    assert date_string(hl.game_datetime) == "2019-11-30"


def test_history_line_game_datetime_invalid() -> None:
    with pytest.raises(ValueError):
        HistoryLine.parse("2019-11-30T20:05:00-050 Normal 234")


@pytest.mark.parametrize(
    "seconds,expected",
    [
        (60 * 60 * 24 - 1, "23:59:59"),
        (0, "00:00"),
        (3603, "01:00:03"),
        (60, "01:00"),
        (2, "00:02"),
    ],
)
def test_format_time(seconds: int, expected: str) -> None:
    assert format_time(seconds) == expected
