# tests.adapters.test_text_presenter
from __future__ import annotations

import pytest

from mahjonggstats.adapters.text_presenter import TextPresenter
from mahjonggstats.ports.stats_query_port import StatsQueryPort


def _query(**overrides) -> StatsQueryPort:
    defaults = dict(
        name="",
        level_names_only=False,
        sort_field="M",
        sort_descending=False,
        verbose=False,
    )
    defaults.update(overrides)
    return StatsQueryPort(**defaults)


def test_presenter_summary_mode(history) -> None:
    output = TextPresenter().render(history, _query())
    assert 'games at level "easy"' in output
    assert "average=" in output


def test_presenter_level_names_only(history) -> None:
    output = TextPresenter().render(history, _query(level_names_only=True))
    assert output.splitlines() == ["difficult", "easy", "ziggurat"]


def test_presenter_verbose_has_heading(history) -> None:
    output = TextPresenter().render(history, _query(verbose=True))
    assert "Mahjongg history of 6 games" in output
    assert "95% confidence level" in output


def test_presenter_level_not_found(history) -> None:
    with pytest.raises(ValueError, match='Level "BOGUS" not found in history'):
        TextPresenter().render(history, _query(name="BOGUS"))
