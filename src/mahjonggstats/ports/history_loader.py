# mahjonggstats.ports.history_loader
from __future__ import annotations

from typing import Protocol

from mahjonggstats.domain.history_line import HistoryLine


class HistoryLoader(Protocol):
    """Outbound port — any source of raw game records.

    Implementors read game records from some backing store (file, database,
    in-memory fixture, etc.) and return them as a flat list of
    ``HistoryLine`` objects.  The application service depends on this
    protocol rather than on any concrete loader, keeping I/O outside the
    core.

    Implementations (structural — no explicit inheritance required):
        ``FileHistoryLoader`` — reads the gnome-mahjongg history file.
        ``MockHistoryLoader`` — in-memory fixture used by the test suite.
    """

    def load(self) -> list[HistoryLine]:
        """Load and return all game records from the backing store.

        Returns:
            A flat list of ``HistoryLine`` objects.  May be empty if no
            records exist.
        """
        ...
