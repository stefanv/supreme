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

test = NumpyTest('supreme').test

def iterable(x):
    try:
        iter(x)
    except:
        return False
    else:
        return True
