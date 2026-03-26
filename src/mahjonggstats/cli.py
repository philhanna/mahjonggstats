from __future__ import annotations

import argparse
import sys

from mahjonggstats.adapters.file_history_loader import FileHistoryLoader
from mahjonggstats.adapters.text_presenter import TextPresenter
from mahjonggstats.application.stats_service import StatsService
from mahjonggstats.ports.stats_query_port import StatsQueryPort


def main(argv: list[str] | None = None) -> int:
    """Entry point for the ``mahjonggstats`` command.

    Parses command-line arguments, validates the sort option, constructs the
    ``StatsQueryPort`` value object, wires the concrete adapters into
    ``StatsService``, and writes the result to stdout.  This function is the
    sole place in the codebase where concrete adapters (``FileHistoryLoader``
    and ``TextPresenter``) are instantiated and injected.

    Args:
        argv: Argument list to parse.  Defaults to ``sys.argv[1:]`` when
            ``None``, which is the normal command-line case.  Pass an
            explicit list when calling from tests or other code.

    Returns:
        ``0`` on success.  On a ``ValueError`` (e.g. an invalid sort option
        or an unknown level name) ``argparse.ArgumentParser.exit()`` is
        called with status ``1``, which raises ``SystemExit`` and does not
        return.
    """
    parser = build_parser()
    ns = parser.parse_args(argv)

    try:
        sort_field, sort_descending = validate_sort_option(ns.sort)
        query = StatsQueryPort(
            name=ns.name,
            level_names_only=ns.level_names_only,
            sort_field=sort_field,
            sort_descending=sort_descending,
            verbose=ns.verbose,
        )
        service = StatsService(
            loader=FileHistoryLoader(),
            presenter=TextPresenter(),
        )
        sys.stdout.write(service.run(query))
        return 0
    except ValueError as exc:
        parser.exit(status=1, message=f"{exc}\n")


def build_parser() -> argparse.ArgumentParser:
    """Create and return the argument parser for the CLI.

    Defines the four command-line options accepted by ``mahjonggstats``:

    * ``-n`` / ``--name``: restrict output to a single named level.
    * ``-l`` / ``--level-names-only``: print level names and exit.
    * ``-s`` / ``--sort``: two-character sort key (field + direction).
    * ``-v`` / ``--verbose``: show full per-level statistics.

    Returns:
        A configured ``argparse.ArgumentParser`` ready to call
        ``parse_args()`` on.
    """
    parser = argparse.ArgumentParser(
        prog="mahjonggstats",
        description="Displays statistics from Gnome mahjongg.",
    )
    parser.add_argument("-n", "--name", default="", help="Include only level name NAME")
    parser.add_argument(
        "-l",
        "--level-names-only",
        action="store_true",
        help="Show level names only",
    )
    parser.add_argument(
        "-s",
        "--sort",
        default="MA",
        help="Sort by games, name, average, or min with A or D direction",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Show complete statistics")
    return parser


def validate_sort_option(sort_opt: str) -> tuple[str, bool]:
    """Parse and validate the ``-s`` / ``--sort`` option string.

    The sort option is a one- or two-character string:

    * **Field** (first character): ``G`` — games played, ``N`` — level name,
      ``A`` — average time, ``M`` — minimum time.
    * **Direction** (second character, optional): ``A`` — ascending
      (default), ``D`` — descending.

    A bare field letter (e.g. ``"G"``) is expanded to ascending order
    (``"GA"``).  An empty string defaults to ``"MA"`` (minimum time,
    ascending).  Matching is case-insensitive.

    Args:
        sort_opt: Raw value of the ``--sort`` flag as received from argparse.

    Returns:
        A ``(sort_field, sort_descending)`` tuple where ``sort_field`` is one
        of ``"G"``, ``"N"``, ``"A"``, ``"M"`` and ``sort_descending`` is
        ``True`` when the direction character is ``"D"``.

    Raises:
        ValueError: If the string is longer than two characters, the field
            character is not one of ``G|N|A|M``, or the direction character
            is not one of ``A|D``.
    """
    value = sort_opt.upper()
    if len(value) == 0:
        value += "MA"
    elif len(value) == 1:
        value += "A"

    if len(value) != 2:
        raise ValueError("invalid sort option. Must have length <= 2")

    if value[0] not in {"G", "N", "A", "M"}:
        raise ValueError(f"invalid sort option. Field must be G|N|A|M, not {value[0]}")

    if value[1] not in {"A", "D"}:
        raise ValueError(f"invalid sort option. Order must be A|D, not {value[1]}")

    return value[0], value[1] == "D"


if __name__ == "__main__":
    raise SystemExit(main())
