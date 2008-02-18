import numpy as N
import unittest
from nose.tools import *
from numpy.testing import assert_array_equal, assert_array_almost_equal, assert_equal
from supreme import register
from supreme.config import ftype,itype

class test_sparse(unittest.TestCase):
    def testip_rot90(self):
        n = 10
        xp = N.random.random(n)
        yp = N.random.random(n)

        theta = 15./180*N.pi
        C = N.cos(theta)
        S = N.sin(theta)

        tf = N.array([[C,-S,3],
                      [S,C,7],
                      [0,0,1.]])

        tx = C*xp - S*yp + 3
        ty = S*xp + C*yp + 7

        yield ((self.check_sparse,ty,tx,yp,xp,tf,mode) for mode in
               ('direct','iterative','RANSAC'))

    def check_sparse(self,ty,tx,yp,xp,tf,mode):
        tf_est,valid = register.sparse(ty,tx,yp,xp,mode=mode)
        assert_array_almost_equal(tf,tf_est)

if __name__ == "__main__":
    NumpyTest().run()
