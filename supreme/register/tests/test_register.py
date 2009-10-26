from numpy.testing import *
import numpy as np

from supreme import register

class test_sparse:
    def testip_rot90(self):
        n = 10
        xp = np.random.random(n)
        yp = np.random.random(n)

        theta = 15./180*np.pi
        C = np.cos(theta)
        S = np.sin(theta)

        tf = np.array([[C,-S,3],
                      [S,C,7],
                      [0,0,1.]])

        tx = C*xp - S*yp + 3
        ty = S*xp + C*yp + 7

        for mode in ('direct', 'iterative', 'RANSAC'):
            yield (self.check_sparse, ty, tx, yp, xp, tf, mode)

    def check_sparse(self, ty, tx, yp, xp, tf, mode):
        tf_est,valid = register.sparse(ty, tx, yp, xp, mode=mode)
        assert_array_almost_equal(tf, tf_est)

if __name__ == "__main__":
    run_module_suite()

