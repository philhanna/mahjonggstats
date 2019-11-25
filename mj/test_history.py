from unittest import TestCase

from mj.history import History


class TestHistory(TestCase):

    def test_format_time(self):
        seconds = 3603
        expected = "01:00:03"
        actual = History.format_time(seconds)
        self.assertEqual(expected, actual)
