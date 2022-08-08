import unittest
from unittest import TestCase
from mj import RecordList, History


class TestHistoryList(TestCase):

    def test_something(self):
        record_list = RecordList()
        for history in [
            History("2022-08-06T23:07:24-0400 easy 294"),
            History("2022-08-04T22:27:39-0400 easy 243"),
            History("2022-08-06T23:02:17-0400 easy 171"),
            History("2022-07-31T01:51:05-0400 easy 308"),
        ]:
            record_list.add(history)
        print(f"DEBUG: {record_list}")
"""
2022-07-31T01:51:05-0400 easy 308
2022-08-04T22:27:39-0400 easy 243
2022-08-05T23:50:36-0400 difficult 218
2022-08-06T22:57:13-0400 ziggurat 228
2022-08-06T23:02:17-0400 easy 171
2022-08-06T23:07:24-0400 easy 294
"""
