import numpy as np
from numpy.testing import *

from supreme.noise import *

class TestVarianceEstimate:
    def test_basic(self):
        x = np.arange(12).astype(np.double).reshape((4, 3))
        v = variance(x, 3)
        assert v.shape == (4, 3)
        assert v[0, 2] == 2.5

if __name__ == "__main__":
    run_module_suite()
