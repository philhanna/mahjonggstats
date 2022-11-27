from io import StringIO

import pytest
from pytest import MonkeyPatch

from mj import Main, History
from tests import testdata, stdout_redirected


class TestMainExceptions:

    def test_get_history_with_no_history(self):
        MonkeyPatch().setattr(History, 'load', lambda: [])
        with StringIO() as out, stdout_redirected(out):
            with pytest.raises(RuntimeError) as ae:
                parms = {}
                main = Main(**parms)
            assert str(ae.value) == "No mahjongg history yet"

    def test_bogus_level_name(self):
        MonkeyPatch().setattr(History, 'load', lambda: [x for x in testdata.splitlines()])
        with StringIO() as out, stdout_redirected(out):
            with pytest.raises(ValueError) as ae:
                parms = {'name': 'bogus' }
                main = Main(**parms)
                main.run()
            assert str(ae.value) == "Level bogus not found"


