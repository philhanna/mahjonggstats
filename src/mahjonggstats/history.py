from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Protocol

from .history_line import HistoryLine
from .level_history import LevelHistory

DEFAULT_FILENAME = ".local/share/gnome-mahjongg/history"


class Loader(Protocol):
    def load(self) -> list[HistoryLine]:
        ...


@dataclass(slots=True)
class FileHistoryLoader:
    filename: Path | None = None

    def load(self) -> list[HistoryLine]:
        filename = self.filename
        if filename is None:
            filename = Path.home() / DEFAULT_FILENAME

        lines: list[HistoryLine] = []
        if not filename.exists():
            return lines

        for line in filename.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                lines.append(HistoryLine.parse(line))
            except (IndexError, ValueError):
                # Keep behavior tolerant of malformed lines.
                continue
        return lines


@dataclass(slots=True)
class History:
    records: list[HistoryLine] = field(default_factory=list)
    levels: dict[str, LevelHistory] = field(default_factory=dict)

    @classmethod
    def create(cls, loader: Loader | None = None) -> "History":
        use_loader = loader if loader is not None else FileHistoryLoader()
        records = use_loader.load()

        grouped: dict[str, list[HistoryLine]] = defaultdict(list)
        for record in records:
            grouped[record.level_name].append(record)

        levels = {
            level_name: LevelHistory(level_name=level_name, records=history)
            for level_name, history in grouped.items()
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
