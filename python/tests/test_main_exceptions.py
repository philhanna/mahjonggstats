import pytest

from mj import Main, History
from tests import testdata


def test_get_history_with_no_history(monkeypatch):
    monkeypatch.setattr(History, 'load', lambda: [])
    with pytest.raises(RuntimeError) as ae:
        parms = {}
        Main(**parms)
    assert str(ae.value) == "No mahjongg history yet"


def test_bogus_level_name(monkeypatch):
    monkeypatch.setattr(History, 'load', testdata.splitlines)
    with pytest.raises(ValueError) as ae:
        parms = {'name': 'bogus'}
        main = Main(**parms)
        main.run()
    assert str(ae.value) == "Level bogus not found"
