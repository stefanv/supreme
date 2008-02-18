# Supreme module initialisation

from numpy.testing import NumpyTest

import config
import lib
import ext

import geometry
import transform
import register
import feature
import misc
import photometry

import functools as _functools
import os.path as _path

try:
    import nose
    cfg = nose.config.Config()
    cfg.includeExe = True
    test = _functools.partial(nose.run, argv=['',_path.dirname(__file__)],
                              config=cfg)
except:
    raise UserWarning('Cannot load nose.  Test suite not available.')

def iterable(x):
    try:
        iter(x)
    except:
        return False
    else:
        return True
