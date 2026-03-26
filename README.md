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
This project uses a [Model-View-Controller][idMVC] approach.
Here are the key Python types associated with each:

### Model
- `History` (`src/mahjonggstats/history.py`)
- `HistoryLine` (`src/mahjonggstats/history_line.py`)
- `LevelHistory` (`src/mahjonggstats/level_history.py`)
  
### View
- `View` (`src/mahjonggstats/view.py`)

### Controller
- `Controller` (`src/mahjonggstats/controller.py`)

The CLI entrypoint is `src/mahjonggstats/cli.py`.

## References
- [Github repository](https://github.com/philhanna/mahjonggstats)
- [Github repository for gnome-mahjongg](https://github.com/GNOME/gnome-mahjongg)
- [Gnome wiki for Mahjongg](https://wiki.gnome.org/Apps/Mahjongg)

[idMVC]: https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller
