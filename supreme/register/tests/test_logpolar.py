import numpy as N
from numpy.testing import *

set_local_path('../../..')
from supreme import register
from supreme.config import ftype,itype
restore_path()

class TestLogpolar(NumpyTestCase):
    def test_basic(self):
        print "\nTODO: add tests for logpolar.  In the meantime,"
        print "      run supreme/doc/examples/register_LPT_auto.py"

if __name__ == "__main__":
    NumpyTest().run()
