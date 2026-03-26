# mahjonggstats.adapters.text_presenter
from __future__ import annotations

from mahjonggstats.domain.history import History
from mahjonggstats.domain.history_line import format_time
from mahjonggstats.domain.level_history import LevelHistory
from mahjonggstats.ports.stats_query import StatsQuery


def _pluralize(count: int, name: str) -> str:
    if count == 1:
        return name
    return f"{name}s"


class TextPresenter:
    """Driven adapter — formats a ``History`` as human-readable text.

    Implements the ``Presenter`` port.  ``render()`` dispatches to one of
    three private helpers depending on the flags in ``StatsQuery``:

    * ``_show_level_names`` — ``-l`` / ``--level-names-only``: one level
      name per line, alphabetically sorted.
    * ``_show_all_levels`` — ``-v`` / ``--verbose``: full statistics for
      each level (mean, sigma, 95% confidence range, top-5 scores),
      optionally preceded by a heading line when no ``-n`` filter is active.
    * ``_show_summary`` — default: one summary line per level showing game
      count, average time, and minimum time, sorted by the field and
      direction specified in ``StatsQuery``.

    Level filtering (``-n`` / ``--name``) and sort ordering are applied
    inside ``_resolve_levels`` and ``_show_summary`` respectively, so every
    output path shares the same filtering logic.
    """

    def render(self, history: History, query: StatsQuery) -> str:
        if query.level_names_only:
            return self._show_level_names(history, query)

        output: list[str] = []
        if query.verbose and query.name == "":
            output.append(self._show_heading(history))
        if query.verbose:
            output.append(self._show_all_levels(history, query))
        else:
            output.append(self._show_summary(history, query))
        return "".join(output)

    def _resolve_levels(
        self, history: History, query: StatsQuery
    ) -> tuple[list[str], list[LevelHistory]]:
        if query.name != "":
            if query.name not in history.levels:
                raise ValueError(
                    f'mahjonggstats: Level "{query.name}" not found in history'
                )
            return [query.name], [history.levels[query.name]]
        level_names = history.level_names()
        levels = [history.levels[name] for name in level_names]
        return level_names, levels

    def _show_heading(self, history: History) -> str:
        count = len(history.records)
        start = history.earliest_date().date().isoformat()
        end = history.latest_date().date().isoformat()
        return f"\nMahjongg history of {count} games from {start} to {end}\n"

    def _show_level_names(self, history: History, query: StatsQuery) -> str:
        level_names, _ = self._resolve_levels(history, query)
        names = sorted(level_names)
        return "\n".join(names) + ("\n" if names else "")

    def _show_summary(self, history: History, query: StatsQuery) -> str:
        _, levels = self._resolve_levels(history, query)

        def prefix(level: LevelHistory) -> str:
            count = level.count()
            return f"{count:3d} {_pluralize(count, 'game')} at level \"{level.level_name}\""

        prefixes = [prefix(level) for level in levels]
        max_prefix = max((len(p) for p in prefixes), default=0)

        if query.sort_field == "G":
            key_fn = lambda level: level.count()
        elif query.sort_field == "N":
            key_fn = lambda level: level.level_name
        elif query.sort_field == "A":
            key_fn = lambda level: level.mean()
        else:
            key_fn = lambda level: level.min()

        sorted_levels = sorted(levels, key=key_fn, reverse=query.sort_descending)

        lines: list[str] = []
        for level in sorted_levels:
            part1 = f"{prefix(level):<{max_prefix}}"
            part2 = f"average={format_time(int(level.mean()))}, min={format_time(level.min())}"
            lines.append(f"{part1} {part2}")
        return "\n".join(lines) + ("\n" if lines else "")

    def _show_all_levels(self, history: History, query: StatsQuery) -> str:
        level_names, levels = self._resolve_levels(history, query)

        lines: list[str] = []
        for level_name, level_history in zip(level_names, levels):
            avg = level_history.mean()
            dev = level_history.standard_deviation()
            lo, hi = level_history.confidence()
            count = level_history.count()

            lines.append("")
            lines.append(f"{count} {_pluralize(count, 'game')} at level \"{level_name}\"")
            lines.append(f"    mu     = {format_time(int(avg))}")
            lines.append(f"    sigma  = {format_time(int(dev))}")
            lines.append(
                "    range  = "
                f"{format_time(int(lo))} to {format_time(int(hi))} "
                "(at 95% confidence level)"
            )

            top_scores = sorted(level_history.records, key=lambda x: x.seconds)
            top_scores = top_scores[: min(5, len(top_scores))]
            lines.append(f"    top {_pluralize(len(top_scores), 'score')}:")
            for score in top_scores:
                lines.append(f"      {score.time_date()}")
        return "\n".join(lines) + ("\n" if lines else "")
