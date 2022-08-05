import os

from mj import History, RecordList


class HistoryList:
    """ History records for this user
    """
    DEFAULT_FILENAME = os.path.expanduser('~/.local/share/gnome-mahjongg/history')

    def __init__(self, filename=DEFAULT_FILENAME):
        self.filename = filename
        self.levels = {}
        self.earliest_date = None
        self.latest_date = None
        with open(self.filename, "rt") as f:
            for line in f:
                history = History(line)
                if self.earliest_date is None or history.date < self.earliest_date:
                    self.earliest_date = history.date
                if self.latest_date is None or history.date > self.latest_date:
                    self.latest_date = history.date
                level = history.level
                record_list = self.get_record_list(level)
                record_list.add(history)

        self.count = 0
        for level in self.levels:
            record_list = self.get_record_list(level)
            record_list.sort()
            self.count += record_list.get_count()

    def get_record_list(self, level):
        if level not in self.levels:
            self.levels[level] = RecordList()
        return self.levels[level]

    def get_count(self):
        return self.count

