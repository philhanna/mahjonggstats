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
        return "{0:d}:{1:02d}".format(mm, ss)

    def __init__(self, line):
        tokens = line.split()
        self.date = datetime.strptime(tokens[0], '%Y-%m-%dT%H:%M:%S%z')
        self.level = tokens[1]
        self.seconds = int(tokens[2])

    def __str__(self):
        return ("{date}: {time}".format(
            date=self.date.strftime("%m/%d/%Y"),
            time=self.seconds_as_mmss()
        ))

    def timedate(self):
        return ("{time} ({date})".format(
            date=self.date.strftime("%m/%d/%Y"),
            time=self.seconds_as_mmss()
        ))

    def seconds_as_mmss(self):
        return History.format_time(self.seconds)