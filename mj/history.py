from datetime import datetime


class History:
    """ A single record in mahjongg history

        The file is located at ~/.local/share/gnome-mahjongg/history
    """

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

    def __init__(self, line):
        """Creates a new History record from a line from the history file.
        The line has the format (datetime level seconds)."""
        tokens = line.split()
        self.date: datetime = datetime.strptime(tokens[0], '%Y-%m-%dT%H:%M:%S%z')
        self.level: str = tokens[1]
        self.seconds: int = int(tokens[2])

    def __str__(self):
        """Converts this object into a string representation"""
        tokens = (
            self.date.strftime("%m/%d/%Y"),
            self.level,
            self.seconds_as_mmss()
        )
        output = " ".join(tokens)
        return output

    def timedate(self) -> str:
        return f"{self.seconds_as_mmss()} ({self.date.strftime('%m/%d/%Y')})"

    def seconds_as_mmss(self) -> str:
        """Converts a number of seconds into hh:mm:ss"""
        return History.format_time(self.seconds)
