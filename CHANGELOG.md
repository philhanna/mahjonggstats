# Change log for mahjonggstats
All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning].
The format is based on [Keep a Changelog].
	
## [Unreleased]
### Added
- Detailed docstrings on all classes, methods, and functions across every
  source file.
- `docs/calltree.md` tracing a full invocation through the stack with
  clickable file and line-number links.

### Changed
- Moved `main()` to be the first function in `cli.py`.
- Moved issue-23 test data into `tests/testdata/`.
- Removed `test23.sh` manual smoke-test script.
- Renamed all `v`-prefixed git tags (e.g. `v3.1.0` → `3.1.0`) for
  consistency with the rest of the tag history.

## [4.1.0] - 2026-03-25
### Changed
- Refactored internal architecture to Ports and Adapters (Hexagonal) pattern.
  - `domain/` — pure business logic with no I/O: `History`, `HistoryLine`, `LevelHistory`.
    `History.create(loader)` replaced by `History.from_records(records)` to eliminate the
    outbound dependency from the domain layer.
  - `ports/` — interface definitions: `HistoryLoader` Protocol (outbound), `Presenter`
    Protocol (outbound), `StatsQuery` frozen dataclass (inbound query model, replaces
    the untyped `args` dict).
  - `adapters/` — concrete implementations: `FileHistoryLoader` (reads gnome-mahjongg
    history file), `TextPresenter` (formats all text output, absorbs both former `View`
    and `Controller`).
  - `application/` — `StatsService` orchestrates loading and presentation by depending
    only on the `HistoryLoader` and `Presenter` protocols; never on concrete adapters.
  - `cli.py` — sole wiring point where concrete adapters are instantiated and injected
    into `StatsService`.
- Test suite reorganized to mirror the new package structure under `tests/domain/`,
  `tests/adapters/`, and `tests/application/`.
- Updated README and added `docs/calltree.md` documenting the full invocation flow.

### Removed
- Flat-layout modules `history.py`, `history_line.py`, `level_history.py`, `view.py`,
  and `controller.py` (superseded by the layered structure above).

## [4.0.0] - 2026-03-25
### Added
- Python package layout under `src/mahjonggstats` with argparse CLI entrypoint.
- Pytest suite covering parser, model, statistics, controller/view behavior, and CLI validation.
- Project packaging configuration via `pyproject.toml`.
- Migration planning document in `docs/plans/toPython.md`.

### Changed
- Converted the implementation from Go to Python 3.12+.
- Updated README to Python-first installation, usage, and test instructions.

### Removed
- Legacy Go application sources and tests.
- Go module files (`go.mod`, `go.sum`).

## [v3.1.0] - 2023-02-25
Change sort and prefix

## [v3.0.2] - 2023-02-24
Fixed URL in README.md

## [v3.0.1] - 2023-02-15
Adjusted format according to gofmt -s

## [v3.0.0] - 2023-02-15
First Go version

## [2.3.1] - 2022-12-24
Added changelog

## [2.3.0] - 2022-12-24
Added --version option

## [2.2.1] - 2022-12-24
Use individual methods instead of classes in unit test

## [2.2.0] - 2022-11-27
Made -q the default option

## [2.1.0] - 2022-11-26
Switched from unittest to pytest

## [2.0.1] - 2022-10-02
v2.0.0 with 100% test coverage

## [2.0.0] - 2022-09-30
Refactored version with better output

## [1.2.1] - 2019-03-19
Added --name, --levels, and --quiet options

## [1.2.0] - 2019-03-19
Added -l, -n, and -q options

## [1.1.0] - 2019-01-06
Compact display

[Semantic Versioning]: http://semver.org
[Keep a Changelog]: http://keepachangelog.com
[4.1.0]: https://github.com/philhanna/mahjonggstats/compare/4.0.0..4.1.0
[4.0.0]: https://github.com/philhanna/mahjonggstats/compare/3.1.0..4.0.0
[v3.1.0]: https://github.com/philhanna/mahjonggstats/compare/3.0.2..3.1.0
[v3.0.2]: https://github.com/philhanna/mahjonggstats/compare/3.0.1..3.0.2
[v3.0.1]: https://github.com/philhanna/mahjonggstats/compare/3.0.0..3.0.1
[v3.0.0]: https://github.com/philhanna/mahjonggstats/compare/2.3.1..3.0.0
[2.3.1]: https://github.com/philhanna/mahjonggstats/compare/2.3.0..2.3.1
[2.3.0]: https://github.com/philhanna/mahjonggstats/compare/2.2.1..2.3.0
[2.2.1]: https://github.com/philhanna/mahjonggstats/compare/2.2.0..2.2.1
[2.2.0]: https://github.com/philhanna/mahjonggstats/compare/2.1.0..2.2.0
[2.1.0]: https://github.com/philhanna/mahjonggstats/compare/2.0.1..2.1.0
[2.0.1]: https://github.com/philhanna/mahjonggstats/compare/2.0.0..2.0.1
[2.0.0]: https://github.com/philhanna/mahjonggstats/compare/1.2.1..2.0.0
[1.2.1]: https://github.com/philhanna/mahjonggstats/compare/1.2.0..1.2.1
[1.2.0]: https://github.com/philhanna/mahjonggstats/compare/1.1.0..1.2.0
[1.1.0]: https://github.com/philhanna/mahjonggstats/compare/df22598..1.1.0
