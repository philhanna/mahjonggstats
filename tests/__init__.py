import os.path

test_init = os.path.abspath(__file__)
tests = os.path.dirname(test_init)
project_root_dir = os.path.dirname(tests)
testdata = os.path.join(project_root_dir, "testdata")

__all__ = ['project_root_dir', 'testdata']