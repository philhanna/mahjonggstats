# mahjonggstats.adapters.file_history_loader
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from mahjonggstats.domain.history_line import HistoryLine

DEFAULT_FILENAME = ".local/share/gnome-mahjongg/history"


@dataclass(slots=True)
class FileHistoryLoader:
    """Driven adapter — loads game records from the gnome-mahjongg history file.

    Implements the ``HistoryLoader`` port by reading the plain-text history
    file written by gnome-mahjongg.  Each non-blank line is parsed into a
    ``HistoryLine``; malformed lines are silently skipped so that a single
    corrupt entry does not abort the entire load.

    If ``filename`` is not provided, the loader resolves the default path
    ``~/.local/share/gnome-mahjongg/history`` at call time.  A missing file
    is treated as an empty history rather than an error.

    Attributes:
        filename: Explicit path to the history file, or ``None`` to use the
            default location under the user's home directory.
    """

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
