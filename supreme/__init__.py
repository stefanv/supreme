# Supreme module initialisation

from numpy.testing import NumpyTest
import scipy

import config
import geometry
import transform
import register
import ext
import feature
import lib
import misc

test = NumpyTest('supreme').test

def iterable(x):
    try:
        iter(x)
    except:
        return False
    else:
        return True
