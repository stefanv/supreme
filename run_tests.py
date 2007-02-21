import unittest
import os
import doctest

import supreme
from supreme import test
import numpy as N

# Hack to find and execute doctests
# ---------------------------------

print "Excercising documentation examples:"
print "-----------------------------------"

ignore_modules = ['example','setup','test','lib']

def setup(doctest):
    doctest.globs['numpy'] = N
    doctest.globs['N'] = N

suite = unittest.TestSuite()
supreme_root = os.path.dirname(supreme.__file__)
for root,dir,files in os.walk(supreme_root):
    root = root[len(os.path.dirname(supreme_root))+1:]

    for fn in [f for f in files if f.endswith('.py') and
               not f.startswith('__')]:
        module = os.path.join(root,fn).replace('.py','')
        module = module.replace(os.path.sep,'.')

        skip = False
        for m in ignore_modules:
            if m in module: skip = True
        if skip: continue

        try:
            suite.addTest(doctest.DocTestSuite(module,setUp=setup))
        except ImportError, e:
            # No such module
            print e
            pass
        except ValueError, e:
            print e
            # No tests
            pass

runner = unittest.TextTestRunner()
runner.run(suite)

print
print "Running standard unit tests:"
print "----------------------------"
test(level=1,verbosity=1)
