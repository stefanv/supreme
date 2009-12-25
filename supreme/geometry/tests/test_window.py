import numpy as np
from numpy.testing import *

from supreme.geometry.window import gauss

def test_gauss():
    w = gauss(3, std=1e-3)
    w /= w.max()

    expected = np.zeros((3, 3))
    expected[1, 1] = 1

    assert_array_equal(w, expected)

