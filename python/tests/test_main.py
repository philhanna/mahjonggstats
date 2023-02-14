from io import StringIO

import pytest

from mj import Main, History
from tests import testdata


@pytest.fixture
def main(monkeypatch):
    monkeypatch.setattr(History, "load", lambda: testdata.splitlines())


def test_init(main):
    main = Main(**{})
    assert main.level_name is None
    assert not main.level_names_only
    assert not main.verbose


def test_level_name(main):
    parms = {'name': 'bogus'}
    main = Main(**parms)
    assert main.level_name == 'bogus'


def test_run(capsys, main):
    parms = {'verbose': True}
    main = Main(**parms)
    main.run()
    output = capsys.readouterr().out
    assert "σ" in output  # Unicode sigma = U+03C3
    assert "μ" in output  # Unicode mu = U+03BC


def test_run_level_names_only(capsys, main):
    parms = {'level_names_only': True}
    main = Main(**parms)
    main.run()
    output = capsys.readouterr().out
    assert "difficult\nziggurat\neasy\n" == output


def test_run_quiet(main, capsys):
    parms = {}
    main = Main(**parms)
    main.run()
    output = capsys.readouterr().out
    for outline in output.splitlines():
        assert "average=" in outline


def test_run_level_name(main, capsys):
    parms = {'name': 'difficult'}
    main = Main(**parms)
    main.run()
    output = capsys.readouterr().out
    assert "level \"difficult\"" in output
