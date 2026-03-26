from __future__ import annotations

from mahjonggstats.controller import Controller
from mahjonggstats.view import View


def _args(**overrides):
    base = {"n": "", "l": False, "sf": "M", "sd": False, "v": False}
    base.update(overrides)
    return base


def test_controller_summary_mode(history) -> None:
    view = View(model=history, args=_args())
    controller = Controller.create(view=view, args=_args())
    output = controller.run()
    assert 'games at level "easy"' in output
    assert "average=" in output


def test_controller_level_names_only(history) -> None:
    args = _args(l=True)
    view = View(model=history, args=args)
    controller = Controller.create(view=view, args=args)
    output = controller.run()
    assert output.splitlines() == ["difficult", "easy", "ziggurat"]


def test_controller_verbose_has_heading(history) -> None:
    args = _args(v=True)
    view = View(model=history, args=args)
    controller = Controller.create(view=view, args=args)
    output = controller.run()
    assert "Mahjongg history of 6 games" in output
    assert "95% confidence level" in output


def test_view_level_not_found(history) -> None:
    args = _args(n="BOGUS")
    try:
        View(model=history, args=args)
        assert False
    except ValueError as exc:
        assert 'Level "BOGUS" not found in history' in str(exc)
