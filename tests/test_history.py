from unittest import TestCase
from unittest.mock import patch
from mj import History
from tests import testdata


class TestHistory(TestCase):
    """Unit tests for HistoryList"""

    def setUp(self):
        with patch.object(History, "load", return_value=testdata.split("\n")):
            self.hl = History()

    def test_get_history_for_level(self):
        level_history = self.hl.get_level_history("difficult")
        expected = 1
        actual = level_history.count
        self.assertEqual(expected, actual)

    def test_get_history_for_level_bogus(self):
        level_history = self.hl.get_level_history("bogus")
        expected = 0
        actual = level_history.count
        self.assertEqual(expected, actual)

    def test_get_count(self):
        expected = 6
        actual = len(self.hl.records)
        self.assertEqual(expected, actual)

    def test_level_names(self):
        # The level names are sorted by the mean time in seconds of each
        expected = ["difficult", "ziggurat", "easy"]
        actual = self.hl.level_names
        self.assertListEqual(expected, actual)
