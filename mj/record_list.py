import statistics


class RecordList:
    """ A list of records at a particular level
    """

    def __init__(self):
        self.records = []
        self.count = 0

    def add(self, history):
        self.records.append(history)
        self.count += 1

    def sort(self):
        self.records.sort(key=lambda history: history.seconds)

    def get_records(self):
        return self.records

    def get_count(self):
        return self.count

    def get_mean(self):
        times = [h.seconds for h in self.records]
        return statistics.mean(times)

    def get_standard_deviation(self):
        times = [h.seconds for h in self.records]
        if len(times) < 2:
            return 0
        else:
            return statistics.stdev(times)

    def get_95_confidence(self):
        mean = self.get_mean()
        stdev = self.get_standard_deviation()
        conf = 1.96 * stdev
        lo = max(0, mean - conf)
        hi = mean + conf
        return lo, hi
