# mahjonggstats

Python program to display statistics from Gnome Mahjongg.

## Requirements
- Python 3.12+

## Install
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

## Usage
```bash
mahjonggstats [OPTIONS]
```

Options:
- `-n`, `--name`: Include only one level name
- `-l`, `--level-names-only`: Show level names only
- `-s`, `--sort`: Sort by `G|N|A|M` and order `A|D` (e.g. `MA`, `GD`)
- `-v`, `--verbose`: Show full per-level statistics

The default history file is:
- `~/.local/share/gnome-mahjongg/history`

## Tests
```bash
python -m pytest -q
```

## Software architecture

This project uses a [Ports and Adapters (Hexagonal)][idHex] architecture.

### Domain
Pure business logic with no I/O.

- `History` — aggregate built from a list of records (`src/mahjonggstats/domain/history.py`)
- `HistoryLine` — value object parsed from one line of the history file (`src/mahjonggstats/domain/history_line.py`)
- `LevelHistory` — per-level statistics: count, mean, min, std dev, confidence interval (`src/mahjonggstats/domain/level_history.py`)

### Ports
Interfaces that decouple the application core from infrastructure.

- `HistoryLoader` — Protocol for any record source (`src/mahjonggstats/ports/history_loader.py`)
- `Presenter` — Protocol for any output formatter (`src/mahjonggstats/ports/presenter.py`)
- `StatsQuery` — Frozen dataclass carrying the user's intent (`src/mahjonggstats/ports/stats_query.py`)

### Adapters
Concrete implementations of the ports.

- `FileHistoryLoader` — reads the gnome-mahjongg history file (`src/mahjonggstats/adapters/file_history_loader.py`)
- `TextPresenter` — formats all text output (`src/mahjonggstats/adapters/text_presenter.py`)

### Application
Orchestration only; depends on ports, never on concrete adapters.

- `StatsService` — loads records, builds the domain model, delegates to the presenter (`src/mahjonggstats/application/stats_service.py`)

### CLI
The primary driving adapter and the sole wiring point where concrete adapters are
instantiated and injected into `StatsService`.

- `src/mahjonggstats/cli.py`

See [docs/calltree.md](docs/calltree.md) for a full trace of one invocation through the stack.

## References
- [Github repository](https://github.com/philhanna/mahjonggstats)
- [Github repository for gnome-mahjongg](https://github.com/GNOME/gnome-mahjongg)
- [Gnome wiki for Mahjongg](https://wiki.gnome.org/Apps/Mahjongg)

[idHex]: https://en.wikipedia.org/wiki/Hexagonal_architecture_(software)
