# mahjonggstats.domain.history_line
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

TIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"


@dataclass(slots=True)
class HistoryLine:
    """A single record from the gnome-mahjongg history file.

    Each line in the history file represents one completed game and contains
    three space-separated fields: an ISO-8601 timestamp, the level name, and
    the elapsed time in seconds.  ``HistoryLine.parse()`` converts a raw text
    line into this value object.

    Attributes:
        game_datetime: Date and time the game was completed, including timezone.
        level_name: Name of the mahjongg layout that was played (e.g. ``"easy"``).
        seconds: Elapsed game time in seconds.
    """

    game_datetime: datetime
    level_name: str
    seconds: int

    @classmethod
    def parse(cls, line: str) -> "HistoryLine":
        """Parse one line from the history file into a ``HistoryLine``.

        Args:
            line: A single space-separated line in the format
                ``<ISO-8601-timestamp> <level-name> <seconds>``.

        Returns:
            A populated ``HistoryLine`` instance.

        Raises:
            ValueError: If the timestamp cannot be parsed or the seconds
                field is not a valid integer.
            IndexError: If the line contains fewer than three tokens.
        """
        tokens = line.split(" ")
        game_datetime = datetime.strptime(tokens[0], TIME_FORMAT)
        return cls(
            game_datetime=game_datetime,
            level_name=tokens[1],
            seconds=int(tokens[2]),
        )

    def time_date(self) -> str:
        """Return a human-readable time and date string for this record.

        Formats the elapsed time using ``format_time`` and appends the
        calendar date in ISO-8601 format, e.g. ``"03:54 (2019-11-30)"``.

        Returns:
            A string of the form ``"MM:SS (YYYY-MM-DD)"`` or
            ``"HH:MM:SS (YYYY-MM-DD)"`` for games over one hour.
        """
        return f"{format_time(self.seconds)} ({self.game_datetime.date().isoformat()})"

    def __str__(self) -> str:
        """Return a diagnostic string representation of this record.

        Returns:
            A comma-separated key=value string suitable for logging or
            debugging, e.g.
            ``'GameDateTime="2023-01-04T22:12:03-0500", LevelName="easy", Seconds=209'``.
        """
        date_part = self.game_datetime.strftime(TIME_FORMAT)
        return (
            f'GameDateTime="{date_part}", '
            f'LevelName="{self.level_name}", '
            f"Seconds={self.seconds}"
        )


def date_string(value: datetime) -> str:
    """Format a ``datetime`` as a zero-padded ``YYYY-MM-DD`` string.

    Args:
        value: The datetime to format.

    Returns:
        A date string such as ``"2022-07-31"``.
    """
    return f"{value.year:04d}-{value.month:02d}-{value.day:02d}"


def format_time(seconds: int) -> str:
    """Format a duration in seconds as ``MM:SS`` or ``HH:MM:SS``.

    Uses the shorter ``MM:SS`` form when the duration is under one hour,
    and the longer ``HH:MM:SS`` form otherwise.

    Args:
        seconds: Elapsed time in seconds (non-negative).

    Returns:
        A zero-padded time string, e.g. ``"03:54"`` or ``"01:00:03"``.
    """
    mm = seconds // 60
    ss = seconds % 60
    if mm >= 60:
        hh = mm // 60
        mm = mm % 60
        return f"{hh:02d}:{mm:02d}:{ss:02d}"
    return f"{mm:02d}:{ss:02d}"
