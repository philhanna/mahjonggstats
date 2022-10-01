from unittest import TestCase

from mj import HistoryLine


class TestHistoryLine(TestCase):

    def test_str_hour_plus(self):
        line = "2019-11-25T12:21:58-0500 cloud 3603"
        history = HistoryLine(line)
        expected = "11/25/2019 cloud 01:00:03"
        actual = str(history)
        self.assertEqual(expected, actual)

    def test_str_9_30(self):
        line = "2019-11-25T12:21:58-0500 cloud 570"
        history = HistoryLine(line)
        expected = "11/25/2019 cloud 09:30"
        actual = str(history)
        self.assertEqual(expected, actual)

    def test_timedate_normal(self):
        line = "2019-11-30T20:05:00-0500 Normal 234"
        h = HistoryLine(line)
        expected = "03:54 (11/30/2019)"
        actual = h.timedate()
        self.assertEqual(expected, actual)

    def test_format_time_hour_plus(self):
        seconds = 3603
        expected = "01:00:03"
        actual = HistoryLine.format_time(seconds)
        self.assertEqual(expected, actual)

    def test_format_time_empty(self):
        seconds = 0
        expected = "00:00"
        actual = HistoryLine.format_time(seconds)
        self.assertEqual(expected, actual)

    def test_format_time_one_minute(self):
        seconds = 60
        expected = "01:00"
        actual = HistoryLine.format_time(seconds)
        self.assertEqual(expected, actual)

    def test_format_time_two_seconds(self):
        seconds = 2
        expected = "00:02"
        actual = HistoryLine.format_time(seconds)
        self.assertEqual(expected, actual)

    def test_format_time_all_day(self):
        seconds = 60 * 60 * 24 - 1
        expected = "23:59:59"
        actual = HistoryLine.format_time(seconds)
        self.assertEqual(expected, actual)
