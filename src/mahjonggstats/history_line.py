from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

TIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"


@dataclass(slots=True)
class HistoryLine:
    game_datetime: datetime
    level_name: str
    seconds: int

    @classmethod
    def parse(cls, line: str) -> "HistoryLine":
        tokens = line.split(" ")
        game_datetime = datetime.strptime(tokens[0], TIME_FORMAT)
        return cls(
            game_datetime=game_datetime,
            level_name=tokens[1],
            seconds=int(tokens[2]),
        )

    def time_date(self) -> str:
        return f"{format_time(self.seconds)} ({self.game_datetime.date().isoformat()})"

    def __str__(self) -> str:
        date_part = self.game_datetime.strftime(TIME_FORMAT)
        return (
            f'GameDateTime="{date_part}", '
            f'LevelName="{self.level_name}", '
            f"Seconds={self.seconds}"
        )


def date_string(value: datetime) -> str:
    return f"{value.year:04d}-{value.month:02d}-{value.day:02d}"


def format_time(seconds: int) -> str:
    mm = seconds // 60
    ss = seconds % 60
    if mm >= 60:
        hh = mm // 60
        mm = mm % 60
        return f"{hh:02d}:{mm:02d}:{ss:02d}"
    return f"{mm:02d}:{ss:02d}"
