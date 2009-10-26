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

import functools as _functools
import os.path as _path

basedir = _path.abspath(_path.join(__file__, '../'))
args = ['', '--exe', '--with-doctest',
'-w','%s' % basedir,
'-e','supreme.lib.zope']
try:
    import nose as _nose
    test = _functools.partial(_nose.run, 'supreme', argv=args)
except:
    print "Could not load nose.  Unit tests not available."


def iterable(x):
    try:
        iter(x)
    except:
        return False
    else:
        return True
