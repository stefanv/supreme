import numpy as np
from numpy.testing import *
from supreme.photometry import photometric_adjust

def test_basic():
    x = np.random.random((100, 100)) * 255
    y = x / 1.8

    a, b = photometric_adjust(y, x)

    assert_almost_equal(a, 1.8)
    assert_almost_equal(b, 0)

if __name__ == "__main__":
    run_module_suite()
