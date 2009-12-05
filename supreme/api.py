# Supreme module initialisation

import config
import lib
import ext

import geometry
import transform
import register
import feature
import misc
import photometry

def iterable(x):
    try:
        iter(x)
    except:
        return False
    else:
        return True
