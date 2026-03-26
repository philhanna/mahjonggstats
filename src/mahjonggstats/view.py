from __future__ import annotations

from dataclasses import dataclass, field

from .history import History
from .history_line import format_time
from .level_history import LevelHistory


@dataclass(slots=True)
class View:
    model: History
    args: dict[str, object]
    level_names: list[str] = field(init=False, default_factory=list)
    levels: list[LevelHistory] = field(init=False, default_factory=list)

    def __post_init__(self) -> None:
        if self.args["n"] != "":
            name = str(self.args["n"])
            if name not in self.model.levels:
                raise ValueError(f'mahjonggstats: Level "{name}" not found in history')
            self.level_names = [name]
            self.levels = [self.model.levels[name]]
            return

        self.level_names = self.model.level_names()
        self.levels = list(self.model.levels.values())

    def show_all_levels(self) -> str:
        lines: list[str] = []
        for index, level_history in enumerate(self.levels):
            level_name = self.level_names[index]

            avg = level_history.mean()
            dev = level_history.standard_deviation()
            lo, hi = level_history.confidence()
            count = level_history.count()

            lines.append("")
            lines.append(f"{count} {pluralize(count, 'game')} at level \"{level_name}\"")
            lines.append(f"    mu     = {format_time(int(avg))}")
            lines.append(f"    sigma  = {format_time(int(dev))}")
            lines.append(
                "    range  = "
                f"{format_time(int(lo))} to {format_time(int(hi))} "
                "(at 95% confidence level)"
            )

            top_scores = sorted(level_history.records, key=lambda x: x.seconds)
            top_scores = top_scores[: min(5, len(top_scores))]
            lines.append(f"    top {pluralize(len(top_scores), 'score')}:")
            for score in top_scores:
                lines.append(f"      {score.time_date()}")
        return "\n".join(lines) + ("\n" if lines else "")

    def show_heading(self) -> str:
        count = len(self.model.records)
        start = self.model.earliest_date().date().isoformat()
        end = self.model.latest_date().date().isoformat()
        return f"\nMahjongg history of {count} games from {start} to {end}\n"

    def show_level_names(self) -> str:
        names = sorted(self.level_names)
        return "\n".join(names) + ("\n" if names else "")

    def show_summary(self) -> str:
        def prefix(level: LevelHistory) -> str:
            count = level.count()
            return f"{count:3d} {pluralize(count, 'game')} at level \"{level.level_name}\""

        prefixes = [prefix(level) for level in self.levels]
        max_prefix = max((len(p) for p in prefixes), default=0)

        sorted_levels = list(self.levels)
        field = str(self.args["sf"])
        reverse = bool(self.args["sd"])

        if field == "G":
            key_fn = lambda level: level.count()
        elif field == "N":
            key_fn = lambda level: level.level_name
        elif field == "A":
            key_fn = lambda level: level.mean()
        else:
            key_fn = lambda level: level.min()

        sorted_levels = sorted(sorted_levels, key=key_fn, reverse=reverse)

        lines: list[str] = []
        for level in sorted_levels:
            part1 = f"{prefix(level):<{max_prefix}}"
            part2 = f"average={format_time(int(level.mean()))}, min={format_time(level.min())}"
            lines.append(f"{part1} {part2}")
        return "\n".join(lines) + ("\n" if lines else "")


def pluralize(count: int, name: str) -> str:
    if count == 1:
        return name
    return f"{name}s"
