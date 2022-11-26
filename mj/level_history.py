from statistics import mean, stdev
from typing import Tuple

from mj import HistoryLine


class LevelHistory:
    """A list of history lines for a particular level"""

    def __init__(self,
                 level_name: str,
                 records: list[HistoryLine]):
        self._level_name: str = level_name
        self._records: list[HistoryLine] = records

    def __eq__(self, other):
        if not isinstance(other, LevelHistory):
            return False
        if self.level_name != other.level_name:
            return False
        if len(self.records) != len(other.records):
            return False
        for i in range(len(self.records)):
            if self.records[i] != other.records[i]:
                return False
        return True

    def __repr__(self):
        output = (
            f'{__class__.__name__}('
            f'"{self.level_name}"'
            f',[{",".join([repr(history_line) for history_line in self.records])}'
            '])'
        )
        return output

    @property
    def records(self):
        return self._records

    @property
    def confidence(self) -> Tuple[float, float]:
        """Returns the low and high estimates at a 95% confidence level"""
        mean = self.mean
        stdev = self.standard_deviation
        conf = 1.96 * stdev
        lo = mean - conf
        if lo < 0:
            lo = 0
        hi = mean + conf
        return lo, hi

    @property
    def count(self):
        return len(self._records)

    @property
    def level_name(self):
        return self._level_name

    @property
    def mean(self) -> float:
        """Returns the mean of the time values for all records"""
        times = [h.seconds for h in self.records]
        return mean(times)

    @property
    def standard_deviation(self) -> float:
        """Returns the standard deviation of the time values for all records"""
        times = [h.seconds for h in self.records]
        if len(times) < 2:
            return 0
        return stdev(times)
