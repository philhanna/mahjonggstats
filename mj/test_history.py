from unittest import TestCase

from mj.history import History


class TestHistory(TestCase):

    def test_hour_plus(self):
        seconds = 3603
        expected = "01:00:03"
        actual = History.format_time(seconds)
        self.assertEqual(expected, actual)

    def test_empty(self):
        seconds = 0
        expected = "00:00"
        actual = History.format_time(seconds)
        self.assertEqual(expected, actual)

    def test_one_minute(self):
        seconds = 60
        expected = "01:00"
        actual = History.format_time(seconds)
        self.assertEqual(expected, actual)

    def test_two_seconds(self):
        seconds = 2
        expected = "00:02"
        actual = History.format_time(seconds)
        self.assertEqual(expected, actual)

    def test_all_day(self):
        seconds = 60*60*24 - 1
        expected = "23:59:59"
        actual = History.format_time(seconds)
        self.assertEqual(expected, actual)
