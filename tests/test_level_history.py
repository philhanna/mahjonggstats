from unittest import TestCase
from unittest.mock import patch

from mj import History
from tests import testdata


class TestLevelHistory(TestCase):

    def setUp(self):
        with patch.object(History, "load", return_value=testdata.split("\n")):
            self.history = History()

    def test_mean(self):
        lh = self.history.get_level_history("easy")
        expected = 254
        actual = lh.mean
        self.assertEqual(expected, actual)

    def test_standard_deviation(self):
        lh = self.history.get_level_history("easy")
        expected = 61.98386887
        actual = lh.standard_deviation
        self.assertAlmostEqual(expected, actual)

    def test_confidence(self):
        lh = self.history.get_level_history("easy")
        expected = (132, 375)
        lo, hi = lh.confidence
        actual = (int(lo), int(hi))
        self.assertTupleEqual(expected, actual)

    def test_repr(self):
        expected = (
            'LevelHistory("easy",['
            'HistoryLine("2022-07-31T01:51:05-0400 easy 308"),'
            'HistoryLine("2022-08-04T22:27:39-0400 easy 243"),'
            'HistoryLine("2022-08-06T23:02:17-0400 easy 171"),'
            'HistoryLine("2022-08-06T23:07:24-0400 easy 294")])'
        )
        actual = repr(self.history.get_level_history("easy"))
        self.assertEqual(expected, actual)