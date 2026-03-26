from __future__ import annotations

from dataclasses import dataclass

from .view import View


@dataclass(slots=True)
class Controller:
    view: View
    name: str
    level_names_only: bool
    verbose: bool

    @classmethod
    def create(cls, view: View, args: dict[str, object]) -> "Controller":
        return cls(
            view=view,
            name=str(args["n"]),
            level_names_only=bool(args["l"]),
            verbose=bool(args["v"]),
        )

    def run(self) -> str:
        if self.level_names_only:
            return self.view.show_level_names()

        output: list[str] = []
        if self.verbose and self.name == "":
            output.append(self.view.show_heading())

        if not self.verbose:
            output.append(self.view.show_summary())
            return "".join(output)

        output.append(self.view.show_all_levels())
        return "".join(output)
