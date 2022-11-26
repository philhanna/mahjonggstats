from datetime import datetime, date

from pytest import MonkeyPatch

from mj import History, HistoryLine, LevelHistory
from tests import testdata


class TestHistory:

    def setup_method(self):
        def mock_load():
            return testdata.splitlines()
        MonkeyPatch().setattr(History, 'load', mock_load)
        self.history = History()

    def teardown_method(self):
        del self.history

    def test_earliest_date(self):
        expected_date = datetime.strptime("2022-07-31T01:51:05-0400", '%Y-%m-%dT%H:%M:%S%z')
        actual_date = self.history.earliest_date
        assert actual_date == expected_date

    def help_test_level_names(self, level_name):
        actual = self.history.get_level_history(level_name).records
        expected = [
            hl for hl in [HistoryLine(x) for x in testdata.splitlines()]
            if hl.level_name == level_name
        ]
        assert actual == expected

    def test_get_level_history_easy(self):
        self.help_test_level_names("easy")

    def test_get_level_history_difficult(self):
        self.help_test_level_names("difficult")

    def test_get_level_history_bogus(self):
        self.help_test_level_names("bogus")

    def test_latest_date(self):
        expected_date = datetime.strptime("2022-08-06T23:07:24-0400", '%Y-%m-%dT%H:%M:%S%z')
        actual_date = self.history.latest_date
        assert actual_date == expected_date

    def test_level_names(self):
        # Note: the list of level names is sorted by the mean solution time of each level
        assert self.history.level_names == ['difficult', 'ziggurat', 'easy']

    def test_levels(self):
        expected = {
            'difficult': LevelHistory("difficult", [
                HistoryLine("2022-08-05T23:50:36-0400 difficult 218")
            ]),
            'ziggurat': LevelHistory("ziggurat", [
                HistoryLine("2022-08-06T22:57:13-0400 ziggurat 228")
            ]),
            'easy': LevelHistory("easy", [
                HistoryLine("2022-07-31T01:51:05-0400 easy 308"),
                HistoryLine("2022-08-04T22:27:39-0400 easy 243"),
                HistoryLine("2022-08-06T23:02:17-0400 easy 171"),
                HistoryLine("2022-08-06T23:07:24-0400 easy 294"),
            ]),
        }
        actual = self.history.levels
        assert actual == expected

    def test_records(self):
        expected = [
            HistoryLine("2022-07-31T01:51:05-0400 easy 308"),
            HistoryLine("2022-08-04T22:27:39-0400 easy 243"),
            HistoryLine("2022-08-05T23:50:36-0400 difficult 218"),
            HistoryLine("2022-08-06T22:57:13-0400 ziggurat 228"),
            HistoryLine("2022-08-06T23:02:17-0400 easy 171"),
            HistoryLine("2022-08-06T23:07:24-0400 easy 294"),
        ]
        actual = self.history.records
        assert actual == expected