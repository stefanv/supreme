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
        n = 1000
        xp = N.random.random(n)*100
        yp = N.random.random(n)*100

        theta = 15./180*N.pi
        C = N.cos(theta)
        S = N.sin(theta)

        tf = N.array([[C,-S,3],
                      [S,C,7],
                      [0,0,1.]])

        tx = C*xp - S*yp + 3
        ty = S*xp + C*yp + 7

        # Add some noise
        tx += N.random.random(n)-0.5
        ty += N.random.random(n)-0.5

        tf_est,ier = register.sparse(ty,tx,yp,xp)
        assert(N.linalg.norm(tf - tf_est) < 0.1)

if __name__ == "__main__":
    NumpyTest().run()
