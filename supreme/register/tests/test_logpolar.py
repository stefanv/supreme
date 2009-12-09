import numpy as np
from numpy.testing import *

import supreme.api as sr
import scipy.ndimage as ndi

class TestLogpolar:
    def test_basic(self):
        theta = 25 / 180. * np.pi
        M = sr.register.affine_tm(theta=theta, scale=1.3)
        shape = np.array([301, 301])
        M_shift = np.array([[1, 0, -shape[1]/2.],
                            [0, 1, -shape[0]/2.],
                            [0, 0,  1]])
        M = np.dot(np.linalg.inv(M_shift), np.dot(M, M_shift))
        x = (np.random.random(shape)*255).astype(np.uint8)
        y = sr.transform.matrix(x, M)

        peak, angle, est_scale = sr.register.lp_patch_match(x, y, angles=360)

        assert_almost_equal(angle, theta, decimal=1)
        assert_almost_equal(est_scale, 1.3, decimal=1)

if __name__ == "__main__":
    run_module_suite()
