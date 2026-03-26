# mahjonggstats.application.stats_service
from __future__ import annotations

from dataclasses import dataclass, replace

from mahjonggstats.domain.history import History
from mahjonggstats.ports.history_loader_port import HistoryLoaderPort
from mahjonggstats.ports.presenter_port import PresenterPort
from mahjonggstats.ports.stats_query_port import StatsQueryPort


@dataclass(slots=True)
class StatsService:
    """Application service — the single use-case entry point.

    Orchestrates the two outbound ports to fulfil a ``StatsQueryPort``:

    1. Calls ``loader.load()`` to obtain raw ``HistoryLine`` records from
       whatever backing store the injected ``HistoryLoaderPort`` represents.
    2. Passes the records to ``History.from_records()`` to build the domain
       aggregate.
    3. Delegates formatting entirely to ``presenter.render()``.

    ``StatsService`` depends only on the ``HistoryLoaderPort`` and ``PresenterPort``
    protocols — never on concrete adapter classes — so any loader or
    presenter can be substituted without modifying this class.  The CLI
    adapter is the sole wiring point where the concrete adapters are chosen
    and injected.

    Attributes:
        loader: Source of raw game records (outbound port).
        presenter: Formatter that converts a ``History`` to a string
            (outbound port).
    """

    loader: HistoryLoaderPort
    presenter: PresenterPort

    def run(self, query: StatsQueryPort) -> str:
        """Execute the stats use case and return formatted output.

        Calls ``self.loader.load()`` to fetch raw records, builds the domain
        aggregate with ``History.from_records()``, then delegates formatting
        entirely to ``self.presenter.render()``.

        Args:
            query: The user's intent — filtering, sort options, and verbosity
                flags — as a ``StatsQueryPort`` value object.

        Returns:
            A formatted string produced by the injected presenter.
        """
        records = self.loader.load()
        history = History.from_records(records)
        if query.name:
            resolved = history.resolve_level_name(query.name)
            query = replace(query, name=resolved)
        return self.presenter.render(history, query)
