import numpy as np
from numpy.testing import *
from supreme.photometry import photometric_adjust, histogram_adjust

def test_basic():
    x = np.random.random((100, 100)) * 255
    y = x / 1.8

    a, b = photometric_adjust(y, x)

    assert_almost_equal(a, 1.8)
    assert_almost_equal(b, 0)

def test_histogram():
    x = np.random.random((100, 100)) * 200
    y = (x/x.max())**0.8

    z = histogram_adjust(y, x)

    assert np.mean((z - x)**2) < 1

if __name__ == "__main__":
    run_module_suite()
