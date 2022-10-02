from datetime import datetime

from mj import History, HistoryLine


def get_date_format() -> str:
    """Returns the preferred date format string"""
    datefmt: str = "%m/%d/%Y"
    return datefmt


def get_history() -> History:
    """Returns the mahjongg history"""
    history: History = History()
    if len(history.records) == 0:
        raise RuntimeError(f'No mahjongg history yet')
    return history


class Main:
    """Mainline for printing statistics from the mahjongg history"""

    def __init__(self, **kwargs):
        self._level_name: str = kwargs.get("name", None)
        self._level_names_only: bool = kwargs.get("level_names_only", False)
        self._quiet: bool = kwargs.get("quiet", False)
        self._history: History = get_history()

    @property
    def level_name(self) -> str:
        return self._level_name

    @property
    def level_names_only(self) -> bool:
        return self._level_names_only

    @property
    def quiet(self) -> bool:
        return self._quiet

    @property
    def history(self) -> History:
        return self._history

    def run(self):
        """Runs the mainline"""
        level_names = self.get_level_names()

        # If the level names only option was specified,
        # just print the level names and return
        if self.level_names_only:
            for level_name in level_names:
                print(level_name)
            return

        # Print the number of games between the earliest and latest date
        if not self.quiet and self.level_name is None:
            count, start, end = self.get_game_data()
            print(f"\nMahjongg history of {count} games from {start} to {end}")

        # If quiet, just print the history summary
        if self.quiet:
            self.print_summary(level_names)
            return

        # Print the history for each level
        for level_name in level_names:
            level_history = self.history.get_level_history(level_name)

            mean = level_history.mean
            stndev = level_history.standard_deviation
            lo, hi = level_history.confidence
            count = level_history.count

            mean_string = HistoryLine.format_time(mean)
            stndev_string = HistoryLine.format_time(stndev)
            lo_string = HistoryLine.format_time(lo)
            hi_string = HistoryLine.format_time(lo)
            count_string = "game" if count == 1 else "games"

            print()
            print(f'{count} {count_string} at level "{level_name}"')
            print(f"\tμ\t= {mean_string}")
            print(f"\tσ\t= {stndev_string}")
            print(f"\trange\t= {lo_string} to {hi_string} (at 95% confidence level)")
            top5 = sorted(level_history.records[:5], key=lambda x: x.seconds)
            score_string = "score" if len(top5) == 1 else "scores"
            print(f"\ttop {score_string}:")
            for h in top5:
                print(f"\t\t  {h.timedate()}")
        print()

    def print_summary(self, level_names):
        """Prints a summary of average times for each level"""

        def get_prefix(level_history):
            count = level_history.count
            level_name = level_history.level_name
            return f"{count} {'games' if count > 1 else 'game'} at level \"{level_name}\""

        prefixes = [get_prefix(self.history.get_level_history(level_name))
                    for level_name in level_names]
        maxprefix = max([len(x) for x in prefixes])

        for level_name in level_names:
            level_history = self.history.get_level_history(level_name)
            prefix = get_prefix(level_history)
            print(f'{prefix:{maxprefix}} average={HistoryLine.format_time(level_history.mean)}')

    def get_game_data(self) -> tuple[int, str, str]:
        """Prints the heading for the number of games"""
        count = len(self.history.records)
        start = self.history.earliest_date.strftime(get_date_format())
        end = self.history.latest_date.strftime(get_date_format())
        return count, start, end

    def get_level_names(self):
        """Returns the list of levels names in history, sorted by mean seconds"""
        level_name = self.level_name
        if level_name is not None:
            if level_name not in self.history.levels.keys():
                raise ValueError(f'Level {level_name} not found')
            level_names = [level_name]
        else:
            level_names = self.history.level_names
        return level_names
