from datetime import datetime, date

from pytest import MonkeyPatch

from mj import History, HistoryLine
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

    def test_get_level_history_easy(self):
        actual = self.history.get_level_history("easy").records
        expected = [
            hl for hl in [HistoryLine(x) for x in testdata.splitlines()]
            if hl.level_name == 'easy'
        ]
        assert actual == expected

    def test_get_level_history_difficult(self):
        actual = self.history.get_level_history("difficult").records
        expected = [
            hl for hl in [HistoryLine(x) for x in testdata.splitlines()]
            if hl.level_name == 'difficult'
        ]
        assert actual == expected

    def test_get_level_history_bogus(self):
        actual = self.history.get_level_history("bogus").records
        expected = [
            hl for hl in [HistoryLine(x) for x in testdata.splitlines()]
            if hl.level_name == 'bogus'
        ]
        assert actual == expected

    def test_latest_date(self):
        expected_date = datetime.strptime("2022-08-06T23:07:24-0400", '%Y-%m-%dT%H:%M:%S%z')
        actual_date = self.history.latest_date
        assert actual_date == expected_date

'''
    def test_level_names(self):
        assert False

    def test_levels(self):
        assert False

    def test_load(self):
        assert False

    def test_records(self):
        assert False
'''
