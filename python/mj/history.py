from mj import HistoryLine, DEFAULT_FILENAME, LevelHistory


class History:
    """ History records for this user"""

    def __init__(self):
        """Creates a new HistoryList containing all user history records"""
        self._records = [HistoryLine(line) for line in History.load()]

        # self._levels is a map of level names
        # to lists of all history records with that level name
        self._levels = {
            level_name: LevelHistory(level_name,
                                     [x
                                      for x in self._records
                                      if x.level_name == level_name])
            for level_name in
            set([hl.level_name for hl in self._records])
        }

    @property
    def earliest_date(self):
        return min([history_record.game_date
                    for history_record in self.records])

    def get_level_history(self, level_name: str) -> LevelHistory:
        """Returns the records for a specified level name"""
        return self.levels.get(level_name, LevelHistory(level_name, []))

    @property
    def latest_date(self):
        return max([history_record.game_date
                    for history_record in self.records])

    @property
    def level_names(self) -> list[str]:
        """Returns the list of all distinct level names in this history.
        The list is sorted in ascending order of the mean game time
        of each level."""
        level_names = sorted([k for k in self.levels.keys()],
                             key=lambda x: self.get_level_history(x).mean)
        return level_names

    @property
    def levels(self) -> dict[str, LevelHistory]:
        """Returns a map of level names to LevelHistory for that level"""
        return self._levels

    @staticmethod
    def load() -> list[str]:
        """Loads all history records.

        This method can be patched with a mock object that provides
        hard-coded data
        """
        with open(DEFAULT_FILENAME) as fp:
            return [line for line in fp]

    @property
    def records(self) -> list[HistoryLine]:
        """Returns the list of all HistoryLine records"""
        return self._records
