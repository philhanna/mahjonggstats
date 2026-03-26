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
        """Return the total number of games played at this level.

        Returns:
            Number of records in ``self.records``.
        """
        return len(self.records)

    def min(self) -> int:
        """Return the fastest (shortest) game time in seconds.

        Returns:
            The minimum ``seconds`` value across all records, or ``0`` if
            there are no records.
        """
        if self.count() == 0:
            return 0
        return min(record.seconds for record in self.records)

    def mean(self) -> float:
        """Return the arithmetic mean of all game times in seconds.

        Returns:
            The average elapsed time, or ``0.0`` if there are no records.
        """
        values = [float(record.seconds) for record in self.records]
        if not values:
            return 0.0
        return mean(values)

    def standard_deviation(self) -> float:
        """Return the sample standard deviation of all game times in seconds.

        Uses Bessel's correction (ddof=1), which requires at least two
        records.

        Returns:
            The sample standard deviation, or ``0.0`` if there are fewer
            than two records.
        """
        values = [float(record.seconds) for record in self.records]
        if len(values) < 2:
            return 0.0
        try:
            return stdev(values)
        except StatisticsError:
            return 0.0

    def confidence(self) -> tuple[float, float]:
        """Return the 95% confidence interval for the mean game time.

        Computed as ``mean ± 1.96 * standard_deviation``.  The lower bound
        is clamped to ``0.0`` because a negative time is not meaningful.

        Returns:
            A ``(lo, hi)`` tuple of floats representing the lower and upper
            bounds of the interval in seconds.
        """
        avg = self.mean()
        dev = self.standard_deviation()
        conf = 1.96 * dev
        lo = avg - conf
        if lo < 0:
            lo = 0.0
        hi = avg + conf
        return lo, hi
