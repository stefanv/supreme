from numpy.testing import *
import numpy as np

from supreme import transform
from supreme.transform.transform import stackcopy, _lpcoords

class TestTransform:
    def test_logpolar(self, level=1):
        x = np.zeros((3, 3))
        z = transform.logpolar(x)
        assert_equal(z.shape, (12, 3))

        x = np.zeros((3, 3, 3))
        z = transform.logpolar(x)
        assert_equal(z.shape, (12, 3, 3))

        x = np.zeros((3, 3, 4))
        z = transform.logpolar(x)
        assert_equal(z.shape, (12, 3, 4))
        z = transform.logpolar(x, angles=np.linspace(0, 2*np.pi, 400))
        assert_equal(z.shape, (400, 3, 4))

    @raises(ValueError)
    def test_logpolar_on_zeros(self):
        x = np.zeros((3))
        transform.logpolar(x)

    def test__lpcoords(self,level=1):
        z = np.empty((6, 6, 3))
        coords_x,coords_y,angles,log_base = \
                          _lpcoords(z.shape, 5, np.linspace(0,2 * np.pi, 10))
        assert_equal([10, 5], coords_x.shape)
        assert_equal(coords_x.shape, coords_y.shape)
        assert_equal(len(angles), 10)

        z = np.empty((6, 6, 1))
        coords_x,coords_y,_,_ = \
                              _lpcoords(z.shape, 5, np.linspace(0, 2*np.pi, 10))
        assert_equal([10, 5], coords_x.shape)
        assert_equal(coords_x.shape, coords_y.shape)

    def test_stackcopy(self, level=1):
        layers = 4
        x = np.empty((3, 3, layers))
        y = np.eye(3, 3)
        stackcopy(x, y)
        for i in range(layers):
            assert_array_almost_equal(x[...,i], y)

    def test_matrix(self,level=1):
        x = np.arange(9).reshape((3,3)) + 1
        theta = -np.pi/2
        M = np.array([[np.cos(theta), -np.sin(theta), 0],
                      [np.sin(theta),  np.cos(theta), 2],
                      [0,              0,             1]])
        x90 = transform.matrix(x, M, order=1)
        assert_array_almost_equal(x90, np.rot90(x))

if __name__ == "__main__":
    run_module_suite()
