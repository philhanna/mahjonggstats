from functools import cache
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

    def __repr__(self):
        output = "LevelHistory("
        output += self.level_name
        output += ", "
        output += "["
        records = [repr(history_line) for history_line in self.records]
        rstring = ",".join(records)
        output += rstring
        output += "]"
        output += ")"

        output = (
            f'{__class__.__name__}('
            f'"{self.level_name}"'
            f',[{",".join([repr(history_line) for history_line in self.records])}'
            '])'
        )
        return output

    @property
    def level_name(self):
        return self._level_name

    @property
    def records(self):
        return self._records

    @property
    def count(self):
        return len(self._records)

    @property
    @cache
    def mean(self) -> float:
        """Returns the mean of the time values for all records"""
        times = [h.seconds for h in self.records]
        return mean(times)

    @property
    @cache
    def standard_deviation(self) -> float:
        """Returns the standard deviation of the time values for all records"""
        times = [h.seconds for h in self.records]
        if len(times) < 2:
            return 0
        return stdev(times)

    @property
    @cache
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
