from datetime import datetime, date

from pytest import MonkeyPatch

from mj import History
from tests import testdata


class TestHistory:

    def setup_method(self):
        def mock_load():
            return testdata.splitlines()
        monkeypatch = MonkeyPatch()
        monkeypatch.setattr(History, 'load', mock_load)
        self.history = History()

    def teardown_method(self):
        del self.history

    def test_earliest_date(self):
        expected_date = datetime.strptime("2022-07-31T01:51:05-0400", '%Y-%m-%dT%H:%M:%S%z')
        actual_date = self.history.earliest_date
        assert actual_date == expected_date

'''
    def test_get_level_history(self):
        assert False

    def test_latest_date(self):
        assert False

    def test_level_names(self):
        assert False

    def test_levels(self):
        assert False

    def test_load(self):
        assert False

    def test_records(self):
        assert False
'''
