from numpy.testing import *
import numpy as np

from supreme.register.correspond import correspond

def test_basic():
    x = np.zeros((100, 100))
    y = x.copy()

    x[10, 10] = 50
    y[60, 60] = 50

    matches = correspond([(10, 10)], x, [(60, 60)], y)

    assert_equal(matches[0], ((10, 10), (60, 60)))

if __name__ == "__main__":
    run_module_suite()

