import os
from datetime import datetime
from typing import Optional

from mj import History, RecordList


class HistoryList:
    """ History records for this user
    """
    DEFAULT_FILENAME: str = os.path.expanduser('~/.local/share/gnome-mahjongg/history')

    def __init__(self, filename: str = DEFAULT_FILENAME):
        self.filename: str = filename
        self.levels: dict[str, RecordList] = {}

        self.earliest_date: Optional[datetime] = None
        self.latest_date: Optional[datetime] = None

        with open(self.filename, "rt") as f:
            for line in f:
                history: History = History(line)
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

    def get_record_list(self, level: str) -> RecordList:
        """ Returns the RecordList for the specified level """
        if level not in self.levels:
            self.levels[level] = RecordList()
        return self.levels[level]

    def get_count(self) -> int:
        return self.count
