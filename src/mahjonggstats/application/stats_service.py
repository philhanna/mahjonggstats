# mahjonggstats.application.stats_service
from __future__ import annotations

from dataclasses import dataclass

from mahjonggstats.domain.history import History
from mahjonggstats.ports.history_loader import HistoryLoader
from mahjonggstats.ports.presenter import Presenter
from mahjonggstats.ports.stats_query import StatsQuery


@dataclass(slots=True)
class StatsService:
    loader: HistoryLoader
    presenter: Presenter

    def run(self, query: StatsQuery) -> str:
        records = self.loader.load()
        history = History.from_records(records)
        return self.presenter.render(history, query)
