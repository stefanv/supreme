import numpy as np
from numpy.testing import *

from supreme.noise import *

class TestVarianceEstimate:
    def test_basic(self):
        x = np.arange(12).astype(np.uint8).reshape((4, 3))
        print variance(x, 3)

if __name__ == "__main__":
    run_module_suite()
