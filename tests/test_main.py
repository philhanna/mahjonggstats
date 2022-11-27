from io import StringIO

from pytest import MonkeyPatch
from mj import Main, History
from tests import stdout_redirected, testdata


class TestMain:

    def setup_method(self):
        MonkeyPatch().setattr(History, 'load', lambda: [x for x in testdata.splitlines()])

    def test_init(self):
        main = Main(**{})
        assert main.level_name is None
        assert not main.level_names_only
        assert not main.verbose

    def test_level_name(self):
        parms = {'name': 'bogus'}
        main = Main(**parms)
        assert main.level_name == 'bogus'

    def test_run(self):
        with StringIO() as out, stdout_redirected(out):
            parms = {'verbose': True}
            main = Main(**parms)
            main.run()
            output = out.getvalue()
        assert "σ" in output    # Unicode sigma = U+03C3
        assert "μ" in output    # Unicode mu = U+03BC

    def test_run_level_names_only(self):
        with StringIO() as out, stdout_redirected(out):
            parms = {'level_names_only': True}
            main = Main(**parms)
            main.run()
            output = out.getvalue()
        assert "difficult\nziggurat\neasy\n" == output

    def test_run_quiet(self):
        with StringIO() as out, stdout_redirected(out):
            parms = {}
            main = Main(**parms)
            main.run()
            output = out.getvalue()
        for outline in output.splitlines():
            assert "average=" in outline

    def test_run_level_name(self):
        MonkeyPatch().setattr(History, 'load', lambda: [x for x in testdata.splitlines()])
        with StringIO() as out, stdout_redirected(out):
            parms = {'name': 'difficult' }
            main = Main(**parms)
            main.run()
            output = out.getvalue()
        assert "level \"difficult\"" in output

