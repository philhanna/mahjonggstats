# mahjonggstats.adapters.text_presenter
from __future__ import annotations

from mahjonggstats.domain.history import History
from mahjonggstats.domain.history_line import format_time
from mahjonggstats.domain.level_history import LevelHistory
from mahjonggstats.ports.stats_query_port import StatsQueryPort


def _pluralize(count: int, name: str) -> str:
    """Return ``name`` or its naive plural form depending on ``count``.

    Args:
        count: The quantity being described.
        name: The singular noun (e.g. ``"game"``).

    Returns:
        ``name`` unchanged when ``count == 1``, otherwise ``name + "s"``.
    """
    if count == 1:
        return name
    return f"{name}s"


class TextPresenter:
    """Driven adapter — formats a ``History`` as human-readable text.

    Implements the ``Presenter`` port.  ``render()`` dispatches to one of
    three private helpers depending on the flags in ``StatsQueryPort``:

    * ``_show_level_names`` — ``-l`` / ``--level-names-only``: one level
      name per line, alphabetically sorted.
    * ``_show_all_levels`` — ``-v`` / ``--verbose``: full statistics for
      each level (mean, sigma, 95% confidence range, top-5 scores),
      optionally preceded by a heading line when no ``-n`` filter is active.
    * ``_show_summary`` — default: one summary line per level showing game
      count, average time, and minimum time, sorted by the field and
      direction specified in ``StatsQueryPort``.

    Level filtering (``-n`` / ``--name``) and sort ordering are applied
    inside ``_resolve_levels`` and ``_show_summary`` respectively, so every
    output path shares the same filtering logic.
    """

    def render(self, history: History, query: StatsQueryPort) -> str:
        """Format ``history`` according to ``query`` and return the result.

        Dispatches to the appropriate private helper based on the flags in
        ``query``.  ``level_names_only`` takes priority; otherwise ``verbose``
        selects full statistics, and the default produces the summary table.

        Args:
            history: The fully built domain aggregate to present.
            query: The user's options controlling filtering, sorting, and
                verbosity.

        Returns:
            A formatted string ready to write to stdout.

        Raises:
            ValueError: If ``query.name`` is set to a level name that does
                not exist in ``history``.
        """
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
        self, history: History, query: StatsQueryPort
    ) -> tuple[list[str], list[LevelHistory]]:
        """Return the level names and histories to display.

        If ``query.name`` is set, returns only that single level.  Otherwise
        returns all levels ordered by ascending mean time (via
        ``History.level_names()``).

        Args:
            history: The domain aggregate containing all levels.
            query: The user's query; ``query.name`` is inspected for
                filtering.

        Returns:
            A ``(level_names, levels)`` tuple where the two lists are
            parallel and in the same order.

        Raises:
            ValueError: If ``query.name`` is non-empty but not present in
                ``history.levels``.
        """
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
        """Return a one-line summary heading for the verbose output mode.

        Args:
            history: The domain aggregate used to derive game count and
                date range.

        Returns:
            A newline-delimited string of the form
            ``"\\nMahjongg history of N games from YYYY-MM-DD to YYYY-MM-DD\\n"``.
        """
        count = len(history.records)
        start = history.earliest_date().date().isoformat()
        end = history.latest_date().date().isoformat()
        return f"\nMahjongg history of {count} games from {start} to {end}\n"

    def _show_level_names(self, history: History, query: StatsQueryPort) -> str:
        """Return an alphabetically sorted list of level names, one per line.

        Used when ``query.level_names_only`` is ``True`` (``-l`` flag).

        Args:
            history: The domain aggregate containing all levels.
            query: The user's query; ``query.name`` is forwarded to
                ``_resolve_levels`` for optional filtering.

        Returns:
            A newline-terminated string with one level name per line.
        """
        level_names, _ = self._resolve_levels(history, query)
        names = sorted(level_names)
        return "\n".join(names) + ("\n" if names else "")

    def _show_summary(self, history: History, query: StatsQueryPort) -> str:
        """Return a one-line-per-level summary table (the default output mode).

        Each line shows game count, average time, and minimum time for one
        level.  Lines are left-padded so that the statistic columns align.
        The sort field and direction are taken from ``query.sort_field`` and
        ``query.sort_descending``.

        Args:
            history: The domain aggregate containing all levels.
            query: The user's query controlling filtering and sort order.

        Returns:
            A newline-terminated string with one summary line per level.
        """
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

    def _show_all_levels(self, history: History, query: StatsQueryPort) -> str:
        """Return full statistics for each level (the verbose output mode).

        For every level prints: game count, mean (mu), standard deviation
        (sigma), 95% confidence interval, and the top-5 fastest scores with
        their dates.

        Args:
            history: The domain aggregate containing all levels.
            query: The user's query; ``query.name`` is forwarded to
                ``_resolve_levels`` for optional filtering.

        Returns:
            A newline-terminated string with a multi-line block per level.
        """
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
