import os.path

project_root_dir = os.path.abspath("..")
testdata = os.path.join(project_root_dir, "testdata")

__all__ = ['project_root_dir', 'testdata']