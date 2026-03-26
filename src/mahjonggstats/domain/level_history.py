# mahjonggstats.domain.level_history
from __future__ import annotations

from dataclasses import dataclass, field
from statistics import StatisticsError, mean, stdev

from .history_line import HistoryLine


@dataclass(slots=True)
class LevelHistory:
    """Statistical summary of all games played at a single mahjongg level.

    Aggregates every ``HistoryLine`` for one level name and exposes descriptive
    statistics — count, minimum, mean, standard deviation, and a 95% confidence
    interval — that are used by the presenter layer to format output.

    Attributes:
        level_name: Name of the mahjongg layout (e.g. ``"easy"``).
        records: All game records for this level, in file order.
    """

    level_name: str
    records: list[HistoryLine] = field(default_factory=list)

    def count(self) -> int:
        return len(self.records)

    def min(self) -> int:
        if self.count() == 0:
            return 0
        return min(record.seconds for record in self.records)

    def mean(self) -> float:
        values = [float(record.seconds) for record in self.records]
        if not values:
            return 0.0
        return mean(values)

    def standard_deviation(self) -> float:
        values = [float(record.seconds) for record in self.records]
        if len(values) < 2:
            return 0.0
        try:
            return stdev(values)
        except StatisticsError:
            return 0.0

    def confidence(self) -> tuple[float, float]:
        avg = self.mean()
        dev = self.standard_deviation()
        conf = 1.96 * dev
        lo = avg - conf
        if lo < 0:
            lo = 0.0
        hi = avg + conf
        return lo, hi
