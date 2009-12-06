# Supreme module initialisation

import config
import lib
import ext

import geometry
import transform
import register
import feature
import io
import photometry

def iterable(x):
    try:
        iter(x)
    except:
        return False
    else:
        return True
