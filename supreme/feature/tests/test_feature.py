import numpy as N
import unittest
from nose.tools import *
from numpy.testing import assert_array_equal, assert_array_almost_equal, assert_equal
from supreme import feature

class TestFeature(unittest.TestCase):
    def test_match(self):
        f = [[0,1,2,3],
             [3,2,1,2],
             [0,1,2,3.1]]
        featureset = [[3,2,1,0],[0,1,2,3],[9,10,11,12],[3,2,1,0.5]]
        match,dists,valid = feature.match(f,featureset)
        assert_equal(match,[1,3,1])
        assert_equal(valid,[True,False,True])
        assert_array_almost_equal(dists,[0,1.5,0.1])

if __name__ == "__main__":
    NumpyTest().run()
