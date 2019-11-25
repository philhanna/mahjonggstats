from datetime import datetime


class History:
    """ A single record in mahjongg history

        The file is located at ~/.local/share/gnome-mahjongg/history
    """

    @staticmethod
    def format_time(seconds):
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
        self.date = datetime.strptime(tokens[0], '%Y-%m-%dT%H:%M:%S%z')
        self.level = tokens[1]
        self.seconds = int(tokens[2])

    def __str__(self):
        return f"{self.date.strftime('%m/%d/%Y')}: {self.seconds_as_mmss()}"

    def timedate(self):
        return ("{time} ({date})".format(
            date=self.date.strftime("%m/%d/%Y"),
            time=self.seconds_as_mmss()
        ))

    def seconds_as_mmss(self):
        return History.format_time(self.seconds)
