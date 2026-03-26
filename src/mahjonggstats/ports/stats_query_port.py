# mahjonggstats.ports.stats_query_port
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class StatsQueryPort:
    """Inbound query model — the user's intent expressed as a value object.

    Captures every option parsed from the command line and passes them as a
    single immutable object through the application layer to the presenter.
    Using a typed dataclass instead of a raw ``dict`` makes the contract
    between the CLI adapter and the application service explicit and
    statically verifiable.

    Attributes:
        name: If non-empty, restrict output to this level name only.
        level_names_only: When ``True``, print only the list of level names.
        sort_field: Column to sort by: ``G`` (games), ``N`` (name),
            ``A`` (average time), or ``M`` (minimum time, the default).
        sort_descending: When ``True``, reverse the sort order.
        verbose: When ``True``, show full per-level statistics including
            mean, standard deviation, confidence interval, and top scores.
    """

    name: str = ""
    level_names_only: bool = False
    sort_field: str = "M"
    sort_descending: bool = False
    verbose: bool = False
