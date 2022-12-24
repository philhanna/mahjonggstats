import re
from pathlib import Path


def get_version():
    import subprocess
    version = None
    cp = subprocess.run(['pip', 'show', "mahjonggstats"], check=True, text=True, capture_output=True)
    output = cp.stdout
    for token in output.split('\n'):
        m = re.match(r'^Version: (.*)', token)
        if m:
            version = m.group(1)
            break
    return version


DEFAULT_FILENAME = Path.home().joinpath(".local/share/gnome-mahjongg/history")
from .history_line import HistoryLine
from .level_history import LevelHistory
from .history import History
from .main import Main

__all__ = [
    'get_version',
    'DEFAULT_FILENAME',
    'HistoryLine',
    'LevelHistory',
    'History',
    'Main',
]
