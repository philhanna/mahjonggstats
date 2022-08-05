from unittest import TestCase
from mj import History


class TestHistory(TestCase):

    def testNormal(self):
        line = "2019-11-30T20:05:00-0500 Normal 234"
        h = History(line)
        expected = "03:54 (11/30/2019)"
        actual = h.timedate()
        self.assertEqual(expected, actual)
