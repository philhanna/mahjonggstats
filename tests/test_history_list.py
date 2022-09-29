import unittest
from datetime import date
from unittest import TestCase
from mj import RecordList, History


class TestHistoryList(TestCase):

    def test_record_list(self):
        record_list = RecordList()
        for history in [
            History("2022-08-06T23:07:24-0400 easy 294"),
            History("2022-08-04T22:27:39-0400 easy 243"),
            History("2022-08-06T23:02:17-0400 easy 171"),
            History("2022-07-31T01:51:05-0400 easy 308"),
        ]:
            record_list.add(history)
        self.assertEqual(4, record_list.get_count())
        expected = [
            f"08/06/2022 easy 04:54",
            f"08/04/2022 easy 04:03",
            f"08/06/2022 easy 02:51",
            f"07/31/2022 easy 05:08",
        ]
        actual = [str(x) for x in record_list.get_records()]
        self.assertListEqual(expected, actual)
