"""Global configuration and utility functions."""

import numpy as N
import os.path
import sys

__all__ = ['abs_path','add_path','remove_path','ftype','itype',
           'data_path','lib_path']

ftype = N.float64
itype = N.int32
eps = N.finfo(ftype).eps

def abs_path(relpath):
    """Given a relative path, return the absolute path."""
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
