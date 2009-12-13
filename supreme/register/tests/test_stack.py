from numpy.testing import *
import numpy as np

from supreme.register import stack

class TestStack:
    def test_corners(self):
        corners = stack.corners((3,5))
        assert_array_almost_equal(corners, [[0,0],
                                            [0,4],
                                            [2,0],
                                            [2,4]])

    def test_with_transform(self):
        x1 = np.arange(9).reshape((3,3)) + 1
        x1[:] = 10
        x2 = x1.copy()
        theta = -np.pi/2
        M = np.array([[np.cos(theta), -np.sin(theta),  0],
                      [np.sin(theta),  np.cos(theta), +2],
                      [0,              0,              1]])

        stacked = stack.with_transform([x1, x2], [np.eye(3), M],
                                       weights=[1, 1], order=1)
        assert(np.allclose(stacked, 10))

if __name__ == "__main__":
    run_module_suite()

