from io import StringIO
from unittest import TestCase
from unittest.mock import patch, PropertyMock

from mj import History, Main, LevelHistory, HistoryLine
from tests import testdata, stdout_redirected


class TestMain(TestCase):
    """Unit tests for the mainline"""

    def setUp(self):
        with patch.object(History, "load", return_value=testdata.splitlines()):
            self.main = Main()

    def test_get_history(self):
        self.assertIsNotNone(self.main.history)

    def test_get_no_history(self):
        with self.assertRaises(RuntimeError) as ex:
            with patch.object(History, "load", return_value=[]):
                Main()
        expected = "No mahjongg history yet"
        actual = str(ex.exception)
        self.assertEqual(expected, actual)

    def test_get_game_data(self):
        expected = (6, "07/31/2022", "08/06/2022")
        actual = self.main.get_game_data()
        self.assertTupleEqual(expected, actual)

    def test_get_level_names(self):
        expected = [
            "difficult",
            "ziggurat",
            "easy",
        ]
        actual = self.main.get_level_names()
        self.assertListEqual(expected, actual)

    def test_get_level_names_single_name(self):
        main = Main(**{"name": "difficult"})
        expected = ["difficult"]
        actual = main.get_level_names()
        self.assertListEqual(expected, actual)

    def test_print_summary(self):
        with StringIO() as out, stdout_redirected(out):
            self.main.print_summary(["difficult"])
            output = out.getvalue()
        self.assertIn("1 game", output)

    def test_print_summary_all(self):
        with StringIO() as out, stdout_redirected(out):
            self.main.print_summary(["difficult", "ziggurat", "easy"])
            output = out.getvalue()
        self.assertEqual(2, output.count("1 game"))
        self.assertEqual(1, output.count("4 games"))

    def test_run(self):
        with StringIO() as out, stdout_redirected(out):
            self.main.run()
            output = out.getvalue()
        self.assertEqual(2, output.count("1 game"))
        self.assertEqual(1, output.count("4 games"))

    def test_run_quiet(self):
        with StringIO() as out, stdout_redirected(out):
            with patch.object(History, "load", return_value=testdata.splitlines()):
                kwargs = {
                    "quiet": True
                }
                main = Main(**kwargs)
                main.run()
                output = out.getvalue()
        nlines = len(output.splitlines())
        self.assertEqual(3, nlines)
        self.assertEqual(2, output.count("1 game"))
        self.assertEqual(1, output.count("4 games"))

    def test_run_level_names_only(self):
        with StringIO() as out, stdout_redirected(out):
            with patch.object(History, "load", return_value=testdata.splitlines()):
                kwargs = {
                    "level_names_only": True
                }
                main = Main(**kwargs)
                main.run()
                output = out.getvalue()
        expected = ['difficult', 'ziggurat', 'easy']
        actual = output.splitlines()
        self.assertListEqual(expected, actual)

    def test_run_bogus_level_names(self):
        with self.assertRaises(ValueError) as ex:
            with patch.object(History, "load", return_value=testdata.splitlines()):
                main = Main(**{'name': 'bogus'})
                main.run()
        expected = "Level bogus not found"
        actual = str(ex.exception)
        self.assertEqual(expected, actual)
