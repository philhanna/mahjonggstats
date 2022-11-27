import pytest

from mj import HistoryLine, LevelHistory
from tests import testdata


class TestLevelHistory:

    def setup_method(self):
        record_list = [
            hl
            for hl in [HistoryLine(line) for line in testdata.splitlines()]
            if hl.level_name == 'easy'
        ]
        self.lh = LevelHistory("easy", record_list)

    def teardown_method(self):
        del self.lh

    def test_bad_eq(self):
        """Tests the specific ways the __eq__ test can fail (for better unit test coverage)"""

        # First way to fail: not the same type
        assert not self.lh == "bogus"

        # Second way to fail: different level names
        lh = LevelHistory("difficult", [
            hl
            for hl in [HistoryLine(line) for line in testdata.splitlines()]
            if hl.level_name == 'difficult'
        ])
        assert not self.lh == lh

        # Third way to fail: different number of records
        lh = LevelHistory("easy", [
                                      hl
                                      for hl in [HistoryLine(line) for line in testdata.splitlines()]
                                      if hl.level_name == 'easy'
                                  ][1:])  # Delete the last record
        assert not self.lh == lh

        # Fourth way to fail: same number of records but some different
        lh = LevelHistory("easy", [
            hl
            for hl in [HistoryLine(line) for line in ("2021" + testdata[4:]).splitlines()]
            if hl.level_name == 'easy'
        ])  # First record year set to 2021
        assert not self.lh == lh

    def test_confidence(self):
        assert self.lh.confidence == pytest.approx((132.51162, 375.48838))

    def test_confidence_lo_zero(self):
        """Tests that lower bound of 95% confidence is zero, rather than negative"""
        lotestdata = """\
2022-07-31T01:51:05-0400 easy 8
2022-08-04T22:27:39-0400 easy 43
2022-08-05T23:50:36-0400 difficult 18
2022-08-06T22:57:13-0400 ziggurat 28
2022-08-06T23:02:17-0400 easy 1
2022-08-06T23:07:24-0400 easy 4"""
        record_list = [
            hl
            for hl in [HistoryLine(line) for line in lotestdata.splitlines()]
            if hl.level_name == 'easy'
        ]
        lh = LevelHistory("easy", record_list)
        assert lh.confidence[0] == 0

    def test_count(self):
        assert len(self.lh.records) == 4

    def test_good_eq(self):
        lh = LevelHistory("easy", [
            hl
            for hl in [HistoryLine(line) for line in testdata.splitlines()]
            if hl.level_name == 'easy'
        ])
        assert self.lh == lh

    def test_level_name(self):
        assert self.lh.level_name == "easy"

    def test_mean(self):
        assert self.lh.mean == 254

    def test_records(self):
        expected = [
            HistoryLine("2022-07-31T01:51:05-0400 easy 308"),
            HistoryLine("2022-08-04T22:27:39-0400 easy 243"),
            HistoryLine("2022-08-06T23:02:17-0400 easy 171"),
            HistoryLine("2022-08-06T23:07:24-0400 easy 294"),
        ]
        actual = [x for x in self.lh.records if x.level_name == 'easy']
        assert actual == expected

    def test_repr(self):
        actual = repr(self.lh)
        expected = "".join([
            'LevelHistory',
            '(',
            '"easy"',
            ',',
            '[',
            repr(HistoryLine("2022-07-31T01:51:05-0400 easy 308")),
            ',',
            repr(HistoryLine("2022-08-04T22:27:39-0400 easy 243")),
            ',',
            repr(HistoryLine("2022-08-06T23:02:17-0400 easy 171")),
            ',',
            repr(HistoryLine("2022-08-06T23:07:24-0400 easy 294")),
            ']',
            ')',
        ])
        assert actual == expected

    def test_standard_deviation(self):
        assert self.lh.standard_deviation == pytest.approx(61.98386)
