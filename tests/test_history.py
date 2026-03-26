from __future__ import annotations

from datetime import datetime

from mahjonggstats.history import History


def test_history_new(history: History) -> None:
    assert len(history.records) == 6
    assert len(history.levels) == 3
    assert history.levels["easy"].count() == 4
    assert history.levels["ziggurat"].count() == 1
    assert history.levels["difficult"].count() == 1
    assert history.levels.get("BOGUS", None) is None


def test_history_earliest_date(history: History) -> None:
    expected = datetime.strptime("2022-07-31T01:51:05-0400", "%Y-%m-%dT%H:%M:%S%z")
    assert history.earliest_date() == expected


def test_history_latest_date(history: History) -> None:
    expected = datetime.strptime("2022-08-06T23:07:24-0400", "%Y-%m-%dT%H:%M:%S%z")
    assert history.latest_date() == expected


def test_history_level_names(history: History) -> None:
    assert history.level_names() == ["difficult", "ziggurat", "easy"]
