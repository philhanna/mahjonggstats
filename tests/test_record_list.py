from unittest import TestCase

from mj import History, RecordList


class TestRecordList(TestCase):

    def test_only_1_record(self):
        data = "2022-08-05T23:50:36-0400 difficult 218"
        history: History = History(data)
        rl: RecordList = RecordList()
        rl.add(history)
