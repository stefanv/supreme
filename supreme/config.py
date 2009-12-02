"""Global configuration and utility functions."""

import numpy as _np
import os.path as _osp
import sys as _sys

__all__ = ['abs_path', 'ftype', 'itype', 'data_path', 'lib_path', 'get_log']

ftype = _np.float64
itype = _np.int32
eps = _np.finfo(ftype).eps

def abs_path(relpath):
    """Given a relative path, return the absolute path."""
    return _osp.abspath(_osp.join(_osp.dirname(__file__), relpath))

data_path = ''
for dp in ('../data', '../../supreme-data'):
    abs_dp = abs_path(dp)
    if _osp.isdir(abs_dp):
        data_path = abs_dp

lib_path = abs_path('./lib')

def mkdir(d):
    """Equivalent of mkdir -f

    """
    if _osp.isdir(d):
        return

    import os
    os.mkdir(d)

def get_log(name):
    import logging, sys
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    return logging.getLogger(name)
