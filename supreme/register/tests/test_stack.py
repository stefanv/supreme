import numpy as N
import unittest
from nose.tools import *
from numpy.testing import assert_array_equal, assert_array_almost_equal, assert_equal
from supreme.register import stack

class TestStack(unittest.TestCase):
    def test_corners(self):
        corners = stack.corners((3,5))
        assert_array_almost_equal(corners, [[0,0],
                                            [0,4],
                                            [2,0],
                                            [2,4]])

    def test_with_transform(self):
        x1 = N.arange(9).reshape((3,3))+1
        x1[:] = 10
        x2 = x1.copy()
        theta = -N.pi/2
        M = N.array([[N.cos(theta),-N.sin(theta),0],
                     [N.sin(theta), N.cos(theta),-1],
                     [0,            0,           1]])

        stacked = stack.with_transform([x1,x2],[N.eye(3),M],
                                       weights=[1,1],order=1)
        assert(N.allclose(stacked,10))
    
if __name__ == "__main__":
    NumpyTest().run()
