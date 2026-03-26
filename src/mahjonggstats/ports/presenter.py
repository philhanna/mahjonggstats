# mahjonggstats.ports.presenter
from __future__ import annotations

from typing import Protocol

from mahjonggstats.domain.history import History
from mahjonggstats.ports.stats_query import StatsQuery


class Presenter(Protocol):
    """Outbound port — any formatter that turns a History into a string.

    ``StatsService`` depends on this protocol so that the output format can
    be swapped (plain text, JSON, HTML, etc.) without modifying the
    application layer.  The concrete implementation injected during normal
    operation is ``TextPresenter``.

    Implementations (structural — no explicit inheritance required):
        ``TextPresenter`` — formats human-readable text output.
    """

    def render(self, history: History, query: StatsQuery) -> str:
        """Format ``history`` according to ``query`` and return the result.

        Args:
            history: The fully built domain aggregate to present.
            query: The user's options controlling filtering, sorting, and
                verbosity.

        Returns:
            A formatted string ready to write to stdout.
        """
        ...
