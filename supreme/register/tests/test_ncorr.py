import numpy as np
from numpy.testing import *

import supreme.register as sr

def test_xcorr_basic():
    x = (np.random.random((10, 10)) * 255).astype(np.uint8)

    y = (np.random.random((30, 30)) * 255).astype(np.uint8)
    y[13:23, 7:17] = x

    c = sr.ncc(y, x)

    assert_equal(np.unravel_index(np.argmax(c), c.shape),
                 (13, 7))

    assert_almost_equal(c[13, 7], 1)

if __name__ == '__main__':
    run_module_suite()
