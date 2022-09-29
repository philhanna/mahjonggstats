from unittest import TestCase

from mj import History, RecordList


class TestRecordList(TestCase):

    def test_only_1_record(self):
        data = "2022-08-05T23:50:36-0400 difficult 218"
        history: History = History(data)
        rl: RecordList = RecordList()
        rl.add(history)

    def test_get_records(self):
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

    def test_get_mean(self):
        record_list = RecordList()
        for history in [
            History("2022-08-06T23:07:24-0400 easy 294"),
            History("2022-08-04T22:27:39-0400 easy 240"),
        ]:
            record_list.add(history)
        expected = 267
        actual = record_list.get_mean()
        self.assertEqual(expected, actual)

    def test_get_stndev(self):
        record_list = RecordList()
        for history in [
            History("2022-08-06T23:07:24-0400 easy 294"),
            History("2022-08-04T22:27:39-0400 easy 240"),
        ]:
            record_list.add(history)
        expected = 38.18376618407356631764559555366
        actual = record_list.get_standard_deviation()
        self.assertAlmostEqual(expected, actual)

    def test_get_stndev_only_1(self):
        record_list = RecordList()
        for history in [
            History("2022-08-06T23:07:24-0400 easy 294"),
        ]:
            record_list.add(history)
        expected = 0
        actual = record_list.get_standard_deviation()
        self.assertAlmostEqual(expected, actual)

    def test_get_95(self):
        record_list = RecordList()
        for history in [
            History("2022-08-06T23:07:24-0400 easy 294"),
            History("2022-08-04T22:27:39-0400 easy 240"),
        ]:
            record_list.add(history)
        mean = 267
        stndev = 38.18376618407356631764559555366
        band = 1.96 * stndev
        expected = (mean - band, mean + band)
        actual = record_list.get_95_confidence()
        self.assertEqual(expected, actual)

    def test_get_95_negative(self):
        record_list = RecordList()
        for history in [
            History("2022-08-06T23:07:24-0400 easy 1"),
            History("2022-08-04T22:27:39-0400 easy 5"),
        ]:
            record_list.add(history)
        expected = (0, 8.543717164502532)
        actual = record_list.get_95_confidence()
        self.assertEqual(expected, actual)

    def test_str(self):
        record_list = RecordList()
        for history in [
            History("2022-08-06T23:07:24-0400 easy 294"),
            History("2022-08-04T22:27:39-0400 easy 240"),
        ]:
            record_list.add(history)
        expected = "\n".join([
            "08/06/2022 easy 04:54",
            "08/04/2022 easy 04:00",
        ])
        actual = str(record_list)
        self.assertEqual(expected, actual)