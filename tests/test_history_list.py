import os.path
from unittest import TestCase

from mj import HistoryList
from tests import testdata


class TestHistoryList(TestCase):
    """Unit tests for HistoryList"""

    def setUp(self):
        filename = os.path.join(testdata, "history")
        self.hl = HistoryList(filename)

    def test_get_record_list(self):
        expected = 1
        actual = len(self.hl.get_record_list("difficult").get_records())
        self.assertEqual(expected, actual)

    def test_get_record_list_empty(self):
        expected = 0
        actual = len(self.hl.get_record_list("bogus").get_records())
        self.assertEqual(expected, actual)

    def test_get_count(self):
        expected = 12
        actual = self.hl.get_count()
        self.assertEqual(expected, actual)