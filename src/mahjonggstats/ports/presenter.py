# mahjonggstats.ports.presenter
from __future__ import annotations

from typing import Protocol

from mahjonggstats.domain.history import History
from mahjonggstats.ports.stats_query import StatsQuery


class Presenter(Protocol):
    def render(self, history: History, query: StatsQuery) -> str:
        ...
