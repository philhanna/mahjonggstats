from unittest import TestCase
from mj import History


class TestHistoryStr(TestCase):

    def test_str_hour_plus(self):
        line = "2019-11-25T12:21:58-0500 cloud 3603"
        history = History(line)
        expected = "11/25/2019 cloud 01:00:03"
        actual = str(history)
        self.assertEqual(expected, actual)

    def test_str_9_30(self):
        line = "2019-11-25T12:21:58-0500 cloud 570"
        history = History(line)
        expected = "11/25/2019 cloud 09:30"
        actual = str(history)
        self.assertEqual(expected, actual)
