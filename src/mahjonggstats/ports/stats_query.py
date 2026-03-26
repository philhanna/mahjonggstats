# mahjonggstats.ports.stats_query
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class StatsQuery:
    name: str = ""
    level_names_only: bool = False
    sort_field: str = "M"
    sort_descending: bool = False
    verbose: bool = False
