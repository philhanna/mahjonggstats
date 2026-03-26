# tests.application.test_stats_service
from __future__ import annotations

from mahjonggstats.application.stats_service import StatsService
from mahjonggstats.domain.history import History
from mahjonggstats.ports.stats_query import StatsQuery

from tests.conftest import MockHistoryLoader


class _CapturingPresenter:
    def __init__(self) -> None:
        self.last_history: History | None = None
        self.last_query: StatsQuery | None = None

    def render(self, history: History, query: StatsQuery) -> str:
        self.last_history = history
        self.last_query = query
        return "captured"


def test_stats_service_loads_and_delegates() -> None:
    presenter = _CapturingPresenter()
    service = StatsService(loader=MockHistoryLoader(), presenter=presenter)
    result = service.run(StatsQuery())

    assert result == "captured"
    assert presenter.last_history is not None
    assert len(presenter.last_history.records) == 6
    assert presenter.last_query == StatsQuery()
