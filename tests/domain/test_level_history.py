# tests.domain.test_level_history
from __future__ import annotations

from mahjonggstats.domain.history import History

from tests.conftest import almost_equal


def _level_records(history: History, level_name: str):
    return [record for record in history.records if record.level_name == level_name]


def test_level_history_min(history: History) -> None:
    assert history.levels["easy"].min() == 171
    assert history.levels["ziggurat"].min() == 228
    assert _empty_level(history).min() == 0


def test_level_history_mean(history: History) -> None:
    assert almost_equal(history.levels["easy"].mean(), 254.0)
    assert almost_equal(history.levels["ziggurat"].mean(), 228)
    assert almost_equal(_empty_level(history).mean(), 0)


def test_level_history_standard_deviation(history: History) -> None:
    assert almost_equal(history.levels["easy"].standard_deviation(), 61.98386)
    assert almost_equal(history.levels["ziggurat"].standard_deviation(), 0)
    assert almost_equal(_empty_level(history).standard_deviation(), 0)


def test_level_history_confidence(history: History) -> None:
    easy_lo, easy_hi = history.levels["easy"].confidence()
    assert almost_equal(easy_lo, 132.51162, 1e-2)
    assert almost_equal(easy_hi, 375.48838, 1e-2)

    z_lo, z_hi = history.levels["ziggurat"].confidence()
    assert almost_equal(z_lo, 228)
    assert almost_equal(z_hi, 228)

    e_lo, e_hi = _empty_level(history).confidence()
    assert almost_equal(e_lo, 0)
    assert almost_equal(e_hi, 0)


def _empty_level(history: History):
    return history.levels.get("BOGUS") or type(history.levels["easy"])("BOGUS", [])
