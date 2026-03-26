# mahjonggstats.ports.history_loader
from __future__ import annotations

from typing import Protocol

from mahjonggstats.domain.history_line import HistoryLine


class HistoryLoader(Protocol):
    def load(self) -> list[HistoryLine]:
        ...
