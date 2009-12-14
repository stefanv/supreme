import numpy as np
from numpy.testing import *

from supreme.register.radial_sum import radial_sum

def test_basic():
    x = np.array([[1, 0, 2],
                  [0, 5, 0],
                  [3, 0, 4]], dtype=np.double)
    R = radial_sum(x)
    pi = np.pi
    assert_array_equal(R[[135, 45, 225, 315]], [1, 2, 3, 4])

if __name__ == "__main__":
    run_module_suite()

