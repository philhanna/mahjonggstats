import pytest

from mj import HistoryLine, LevelHistory
from tests import testdata


class TestLevelHistory:

    def setup_method(self):
        record_list = [
            hl
            for hl in [HistoryLine(line)
                       for line in testdata.splitlines()]
            if hl.level_name == 'easy'
        ]
        self.lh = LevelHistory("easy", record_list)

    def teardown_method(self):
        del self.lh

    def test_level_name(self):
        assert self.lh.level_name == "easy"

    def test_records(self):
        expected = [
            HistoryLine("2022-07-31T01:51:05-0400 easy 308"),
            HistoryLine("2022-08-04T22:27:39-0400 easy 243"),
            HistoryLine("2022-08-06T23:02:17-0400 easy 171"),
            HistoryLine("2022-08-06T23:07:24-0400 easy 294"),
        ]
        actual = [x for x in self.lh.records if x.level_name == 'easy']
        assert actual == expected

    def test_count(self):
        assert len(self.lh.records) == 4

    def test_mean(self):
        assert self.lh.mean == 254

    def test_standard_deviation(self):
        assert self.lh.standard_deviation == pytest.approx(61.98386)

    def test_confidence(self):
        assert self.lh.confidence == pytest.approx((132.51162, 375.48838))
