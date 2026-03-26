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
        """Build a ``History`` aggregate from a flat list of records.

        Groups the records by ``level_name`` and constructs one
        ``LevelHistory`` per group.  This is the canonical factory method;
        prefer it over calling the dataclass constructor directly.

        Args:
            records: All game records returned by a ``HistoryLoader``,
                in any order.

        Returns:
            A fully populated ``History`` instance.
        """
        grouped: dict[str, list[HistoryLine]] = defaultdict(list)
        for record in records:
            grouped[record.level_name].append(record)
        levels = {
            name: LevelHistory(level_name=name, records=hist)
            for name, hist in grouped.items()
        }
        return cls(records=records, levels=levels)

    def earliest_date(self) -> datetime:
        """Return the datetime of the oldest game in the history.

        Returns:
            The minimum ``game_datetime`` across all records.

        Raises:
            ValueError: If ``self.records`` is empty.
        """
        if not self.records:
            raise ValueError("There is no history")
        return min(record.game_datetime for record in self.records)

    def latest_date(self) -> datetime:
        """Return the datetime of the most recent game in the history.

        Returns:
            The maximum ``game_datetime`` across all records.

        Raises:
            ValueError: If ``self.records`` is empty.
        """
        if not self.records:
            raise ValueError("There is no history")
        return max(record.game_datetime for record in self.records)

    def resolve_level_name(self, partial: str) -> str:
        """Resolve a partial or full level name to the unique matching name.

        Comparison is case-insensitive and matches any level name that
        contains ``partial`` as a substring.  An exact match (case-sensitive)
        is returned immediately without ambiguity checking.

        Args:
            partial: The full or partial level name supplied by the user.

        Returns:
            The unique level name from the history that matches ``partial``.

        Raises:
            ValueError: If no level name matches, or if more than one does.
        """
        if partial in self.levels:
            return partial

        needle = partial.lower()
        matches = [name for name in self.levels if needle in name.lower()]

        if not matches:
            raise ValueError(f"No level found matching '{partial}'")
        if len(matches) > 1:
            ambiguous = ", ".join(sorted(matches))
            raise ValueError(f"'{partial}' is ambiguous: {ambiguous}")
        return matches[0]

    def level_names(self) -> list[str]:
        """Return all level names sorted by ascending mean game time.

        Levels with a lower average completion time appear first.  This is
        the default ordering used by ``TextPresenter`` when no explicit sort
        option is supplied.

        Returns:
            A list of level name strings.
        """
        names = list(self.levels.keys())
        return sorted(names, key=lambda name: self.levels[name].mean())
