# mahjonggstats.domain.history
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime

from .history_line import HistoryLine
from .level_history import LevelHistory


@dataclass(slots=True)
class History:
    """The complete game history loaded from the gnome-mahjongg history file.

    Acts as the top-level domain aggregate.  It holds every ``HistoryLine``
    record and a pre-grouped mapping from level name to ``LevelHistory``.
    Construction is done via ``History.from_records()`` rather than directly,
    so that grouping logic stays inside the domain and the caller only needs
    to supply a flat list of records.

    Attributes:
        records: Every game record, in the order returned by the loader.
        levels: Mapping from level name to its aggregated ``LevelHistory``.
    """

    records: list[HistoryLine] = field(default_factory=list)
    levels: dict[str, LevelHistory] = field(default_factory=dict)

    @classmethod
    def from_records(cls, records: list[HistoryLine]) -> "History":
        grouped: dict[str, list[HistoryLine]] = defaultdict(list)
        for record in records:
            grouped[record.level_name].append(record)
        levels = {
            name: LevelHistory(level_name=name, records=hist)
            for name, hist in grouped.items()
        }
        return cls(records=records, levels=levels)

    def earliest_date(self) -> datetime:
        if not self.records:
            raise ValueError("There is no history")
        return min(record.game_datetime for record in self.records)

    def latest_date(self) -> datetime:
        if not self.records:
            raise ValueError("There is no history")
        return max(record.game_datetime for record in self.records)

    def level_names(self) -> list[str]:
        names = list(self.levels.keys())
        return sorted(names, key=lambda name: self.levels[name].mean())
