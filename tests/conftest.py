from __future__ import annotations

import math
from dataclasses import dataclass

import pytest

from mahjonggstats.domain.history import History
from mahjonggstats.domain.history_line import HistoryLine

TESTDATA = """2022-07-31T01:51:05-0400 easy 308
2022-08-04T22:27:39-0400 easy 243
2022-08-05T23:50:36-0400 difficult 218
2022-08-06T22:57:13-0400 ziggurat 228
2022-08-06T23:02:17-0400 easy 171
2022-08-06T23:07:24-0400 easy 294"""


@dataclass(slots=True)
class MockHistoryLoader:
    def load(self) -> list[HistoryLine]:
        lines: list[HistoryLine] = []
        for line in TESTDATA.splitlines():
            lines.append(HistoryLine.parse(line))
        return lines


def almost_equal(a: float, b: float, delta: float = 1e-5) -> bool:
    return math.fabs(a - b) <= delta


@pytest.fixture
def history() -> History:
    return History.from_records(MockHistoryLoader().load())
