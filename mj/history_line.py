from datetime import datetime


class HistoryLine:
    """ A single record in mahjongg history
    """

    def __init__(self, line):
        """Creates a new History record from a line from the history file.
        The line has the format (datetime level seconds)."""
        self._line = line
        tokens = line.split()
        self._game_date: datetime = datetime.strptime(tokens[0], '%Y-%m-%dT%H:%M:%S%z')
        self._level_name: str = tokens[1]
        self._seconds: int = int(tokens[2])

    def __eq__(self, other):
        return str(self) == str(other)

    @staticmethod
    def format_time(seconds) -> str:
        """Creates a string with hh:mm:ss from the specified number of seconds"""
        seconds = int(seconds)
        mm = seconds // 60
        ss = seconds % 60
        time_string = f"{mm:02d}:{ss:02d}"
        if mm >= 60:
            hh = mm // 60
            mm = mm % 60
            time_string = f"{hh:02d}:{mm:02d}:{ss:02d}"
        return time_string

    @property
    def game_date(self) -> datetime:
        """Returns the game date"""
        return self._game_date

    @property
    def level_name(self) -> str:
        """Returns the level name"""
        return self._level_name

    @property
    def line(self) -> str:
        return self._line

    def __repr__(self) -> str:
        output = "HistoryLine("
        output += ")"
        output = f"""{__class__.__name__}("{self.line}")"""
        return output

    @property
    def seconds(self) -> int:
        """Returns the number of seconds in this game"""
        return self._seconds

    def seconds_as_mmss(self) -> str:
        """Converts a number of seconds into hh:mm:ss"""
        return HistoryLine.format_time(self.seconds)

    def __str__(self) -> str:
        """Converts this object into a string representation"""
        tokens = (
            self.game_date.date().isoformat(),
            self.level_name,
            self.seconds_as_mmss()
        )
        output = " ".join(tokens)
        return output

    def timedate(self) -> str:
        """Returns the number of seconds found in this record
        in the format hh:mm:ss (MM/DD/YYYY)"""
        return f"{self.seconds_as_mmss()} ({self.game_date.date().isoformat()})"
