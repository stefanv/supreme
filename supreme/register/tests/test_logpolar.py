import numpy as N
import unittest
from nose.tools import *
from numpy.testing import assert_array_equal, assert_array_almost_equal, assert_equal
from supreme import register
from supreme.config import ftype,itype

class TestLogpolar(unittest.TestCase):
    def test_basic(self):
        print "\nTODO: add tests for logpolar.  In the meantime,"
        print "      run supreme/doc/examples/register_LPT_auto.py"

if __name__ == "__main__":
    NumpyTest().run()
