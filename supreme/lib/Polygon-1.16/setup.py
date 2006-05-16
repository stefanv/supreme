#!/usr/bin/env python
#       $Id: setup.py,v 1.33 2006/04/19 09:41:12 joerg Exp $    

from distutils.core import setup, Extension

# Tolerance is used to evaluate coincident points:
#  * None for a variable value adjustable from python, or
#  * a macro name like 'DBL_EPSILON', or
#  * a numerical value as string like '1.0e-5'
Tolerance=None

# withNumeric enables some extensions:
#  * faster adding of contours from Numeric arrays
#  * data style STYLE_ARRAY to get contours and TriStrips
#    as Numeric arrays
withNumeric=1

# defaultStyle may be used to set the default style to one of:
#  * STYLE_TUPLE to get tuples of points
#  * STYLE_LIST to get lists of points
#  * STYLE_ARRAY to get points as Numeric array
#    withNumeric must be enabled for this!
defaultStyle='STYLE_LIST'

# ------ no changes below! If you need to change, it's a bug! -------
import os, sys
version = '1.16'

mac = [('POLYVERSION', version), ('DEFAULT_STYLE', defaultStyle)]
if Tolerance:
    mac.append(('GPC_EPSILON', Tolerance))

if withNumeric:
    try:
        import Numeric
        print "Using Numeric extension"
        mac.append(('WITH_NUMERIC', 1))
    except:
        print "Numeric extension not found!"

# alloca() needs malloc.h under Windows
if sys.platform == 'win32':
    mac.append(('SYSTEM_WIN32', 1))
        
# there is an error in distutils when building rpms with PYTHONOPTIMIZE set:
if os.environ.has_key('PYTHONOPTIMIZE'):
    del os.environ['PYTHONOPTIMIZE']

    
longdesc = """The Polygon package consists of two modules. One is an extension written in C
wrapping the gpc library (http://www.cs.man.ac.uk/aig/staff/alan/software/)
and its polygon clipping operations in an object oriented fashion. There are
lots of additional methods. The other is written in pure python and provides
some additional functions.

The wrapping and extension code is free software, but the core gpc library is
free for non-commercial usage only. The author says:
   "This library is provided free of charge for non-commercial users. Reaching
    its current state took up almost two years of personal development effort.
    If you have found this software to be useful for your purposes please make
    a donation and help support the continuation of this project. Thanks!"
Please respect this statement and contact the author (see gpc homepage) if you
wish to use this software in commercial projects!
"""

args = { 'name' : "Polygon",
         'version' : version,
         'description' : "Python bindings to the 'General Polygon Clipping Library' (gpc) and additional functions",
         'long_description' : longdesc,
         'license' : "LGPL for Polygon, other for gpc",
         'author' : "Joerg Raedler",
         'author_email' : "joerg@dezentral.de",
         'maintainer' : "dezentral gbr Berlin",
         'maintainer_email' : "software@dezentral.de",
         'url' : "http://www.dezentral.de/soft/Polygon",
         'py_modules' : ["Polygon"],
         'ext_modules' : [Extension('cPolygon', ['gpc.c', 'cPolygon.c', 'PolyUtil.c'],
                                    include_dirs=['.'], define_macros=mac)]
         }
if sys.version_info[:3] >= (2,2,3):
    args['download_url'] = "http://download.dezentral.de/soft/Python/Polygon/"
    args['classifiers'] = ['Development Status :: 5 - Production/Stable',
                           'Intended Audience :: Developers',
                           'Intended Audience :: Science/Research',
                           'License :: Freely Distributable',
                           'License :: Other/Proprietary License',
                           'Programming Language :: C',
                           'Programming Language :: Python',
                           'Operating System :: OS Independent',
                           'Topic :: Scientific/Engineering :: Mathematics',
                           'Topic :: Scientific/Engineering :: Visualization',
                           'Topic :: Multimedia :: Graphics'
                           ]
setup(**args)
