import io
import statistics
from typing import List, Tuple

from mj import History


class RecordList:
    """ A list of records at a particular level """

    def __init__(self):
        """ Creates a new, empty record list """
        self.records: List[History] = []
        self.count: int = 0

    def add(self, history: History):
        """ Adds a history record to the record list """
        self.records.append(history)
        self.count += 1

    def sort(self):
        """ Sorts the record list by number of seconds """
        self.records.sort(key=lambda history: history.seconds)

    def get_records(self) -> List[History]:
        return self.records

    def get_count(self) -> int:
        return self.count

    def get_mean(self) -> float :
        times = [h.seconds for h in self.records]
        return statistics.mean(times)

    def get_standard_deviation(self) -> float:
        times = [h.seconds for h in self.records]
        if len(times) < 2:
            return 0
        return statistics.stdev(times)

    def get_95_confidence(self) -> Tuple[float, float]:
        mean = self.get_mean()
        stdev = self.get_standard_deviation()
        conf = 1.96 * stdev
        lo = mean - conf
        if lo < 0:
            lo = 0
        hi = mean + conf
        return lo, hi

    def __str__(self):
        output = "\n".join([str(history) for history in self.records])
        return output
