from datetime import datetime


class History:
    """ A single record in mahjongg history

        The file is located at ~/.local/share/gnome-mahjongg/history
    """

    @staticmethod
    def format_time(seconds) -> str:
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
        tokens = line.split()
        self.date: datetime = datetime.strptime(tokens[0], '%Y-%m-%dT%H:%M:%S%z')
        self.level: str = tokens[1]
        self.seconds: int = int(tokens[2])

    def __str__(self):
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
        return History.format_time(self.seconds)
