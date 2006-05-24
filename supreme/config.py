import numpy as N
import os.path
import sys

ftype = N.float64
itype = N.int64

def abs_path(relpath):
    return os.path.join(os.path.dirname(__file__),
                        relative_data_path)

def add_path(absdir):
    """Add given directory as the first element of the system path."""
    sys.path.insert(0,absdir)

def remove_path():
    """Remove the first element of the system path."""
    del sys.path[0]

relative_data_path = '../data'
relative_lib_path = './lib'
data_path = abs_path(relative_data_path)
lib_path = abs_path(relative_lib_path)

class ShapeError(Exception):
    pass
