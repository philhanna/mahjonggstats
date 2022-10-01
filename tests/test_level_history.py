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
