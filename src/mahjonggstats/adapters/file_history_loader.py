# mahjonggstats.adapters.file_history_loader
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from mahjonggstats.domain.history_line import HistoryLine

DEFAULT_FILENAME = ".local/share/gnome-mahjongg/history"


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
                continue
        return lines
