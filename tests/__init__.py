import os.path
import sys
from contextlib import contextmanager

test_init = os.path.abspath(__file__)
tests = os.path.dirname(test_init)
project_root_dir = os.path.dirname(tests)
testdata = """\
2022-07-31T01:51:05-0400 easy 308
2022-08-04T22:27:39-0400 easy 243
2022-08-05T23:50:36-0400 difficult 218
2022-08-06T22:57:13-0400 ziggurat 228
2022-08-06T23:02:17-0400 easy 171
2022-08-06T23:07:24-0400 easy 294"""


# redirect stdout technique from https://www.python.org/dev/peps/pep-0343/

@contextmanager
def stdout_redirected(new_stdout):
    save_stdout = sys.stdout
    sys.stdout = new_stdout
    try:
        yield None
    finally:
        sys.stdout = save_stdout


__all__ = [
    'stdout_redirected',
    'project_root_dir',
    'testdata',
]
