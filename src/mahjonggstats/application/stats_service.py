# mahjonggstats.application.stats_service
from __future__ import annotations

from dataclasses import dataclass

from mahjonggstats.domain.history import History
from mahjonggstats.ports.history_loader import HistoryLoader
from mahjonggstats.ports.presenter import Presenter
from mahjonggstats.ports.stats_query import StatsQuery


@dataclass(slots=True)
class StatsService:
    """Application service — the single use-case entry point.

    Orchestrates the two outbound ports to fulfil a ``StatsQuery``:

    1. Calls ``loader.load()`` to obtain raw ``HistoryLine`` records from
       whatever backing store the injected ``HistoryLoader`` represents.
    2. Passes the records to ``History.from_records()`` to build the domain
       aggregate.
    3. Delegates formatting entirely to ``presenter.render()``.

    ``StatsService`` depends only on the ``HistoryLoader`` and ``Presenter``
    protocols — never on concrete adapter classes — so any loader or
    presenter can be substituted without modifying this class.  The CLI
    adapter is the sole wiring point where the concrete adapters are chosen
    and injected.

    Attributes:
        loader: Source of raw game records (outbound port).
        presenter: Formatter that converts a ``History`` to a string
            (outbound port).
    """

    loader: HistoryLoader
    presenter: Presenter

    def run(self, query: StatsQuery) -> str:
        """Execute the stats use case and return formatted output.

        Calls ``self.loader.load()`` to fetch raw records, builds the domain
        aggregate with ``History.from_records()``, then delegates formatting
        entirely to ``self.presenter.render()``.

        Args:
            query: The user's intent — filtering, sort options, and verbosity
                flags — as a ``StatsQuery`` value object.

        Returns:
            A formatted string produced by the injected presenter.
        """
        records = self.loader.load()
        history = History.from_records(records)
        return self.presenter.render(history, query)
