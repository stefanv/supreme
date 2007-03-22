import numpy as N
from numpy.testing import *

set_local_path('../../..')
from supreme import register
from supreme.config import ftype,itype
restore_path()

class test_logpolar(NumpyTestCase):
    pass

class test_sparse(NumpyTestCase):
    def test_rot90(self):
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

        valid,tf_est = register.sparse(ty,tx,yp,xp)
        assert_array_almost_equal(tf,tf_est)

if __name__ == "__main__":
    NumpyTest().run()
