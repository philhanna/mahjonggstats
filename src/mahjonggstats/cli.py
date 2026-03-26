from __future__ import annotations

import argparse
import sys

from mahjonggstats.adapters.file_history_loader import FileHistoryLoader
from mahjonggstats.adapters.text_presenter import TextPresenter
from mahjonggstats.application.stats_service import StatsService
from mahjonggstats.ports.stats_query import StatsQuery


def validate_sort_option(sort_opt: str) -> tuple[str, bool]:
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


def build_parser() -> argparse.ArgumentParser:
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


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    ns = parser.parse_args(argv)

    try:
        sort_field, sort_descending = validate_sort_option(ns.sort)
        query = StatsQuery(
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


if __name__ == "__main__":
    raise SystemExit(main())
