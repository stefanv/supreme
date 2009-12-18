#!/usr/bin/env python
"""Script to auto-generate our API docs.
"""
# stdlib imports
import os, sys

# local imports
from apigen import ApiDocWriter

# version comparison
from distutils.version import LooseVersion as V

#*****************************************************************************

def abort(error):
    print '*WARNING* API documentation not generated: %s'%error
    exit()

if __name__ == '__main__':
    package = 'supreme'

    # Check that the 'image' package is available. If not, the API
    # documentation is not (re)generated and existing API documentation
    # sources will be used.

    try:
        __import__(package)
    except ImportError, e:
        abort("Can not import package")

    module = sys.modules[package]

    outdir = 'source/api'
    docwriter = ApiDocWriter(package)
    docwriter.package_skip_patterns += [r'\.fixes$',
                                        r'\.externals$',
                                        'lib.decorator$',
                                        'lib.pywt',
                                        'lib.nurbs',
                                        ]
    docwriter.module_skip_patterns += ['ctype_arrays$',
                                       'api$',
                                       'lib.EXIF$',
                                       'transform.transform$',
                                       'misc.io$',
                                       'ext.libsupreme$',
                                       'transform.chirp$',
                                       'register.register$',
                                       'register.image$',
                                       'feature.feature$',
                                       'geometry.grid$',
                                       'geometry.polygon$',
                                       ]
    docwriter.write_api_docs(outdir)
    docwriter.write_index(outdir, 'api', relative_to='source/api')
    print '%d files written' % len(docwriter.written_modules)

