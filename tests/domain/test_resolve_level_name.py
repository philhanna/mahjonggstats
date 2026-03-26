# tests.domain.test_resolve_level_name
from __future__ import annotations

import pytest

from mahjonggstats.domain.history import History


def test_exact_match_returns_name(history: History) -> None:
    assert history.resolve_level_name("easy") == "easy"


def test_partial_match_single_result(history: History) -> None:
    assert history.resolve_level_name("eas") == "easy"


def test_partial_match_case_insensitive(history: History) -> None:
    assert history.resolve_level_name("EAS") == "easy"


def test_partial_match_no_results_raises(history: History) -> None:
    with pytest.raises(ValueError, match="No level found matching 'bogus'"):
        history.resolve_level_name("bogus")


def test_partial_match_ambiguous_raises(history: History) -> None:
    # "i" appears in both "difficult" and "ziggurat"
    with pytest.raises(ValueError, match="is ambiguous"):
        history.resolve_level_name("i")


def test_ambiguous_error_lists_matches(history: History) -> None:
    with pytest.raises(ValueError, match="difficult") as exc_info:
        history.resolve_level_name("i")
    assert "ziggurat" in str(exc_info.value)
