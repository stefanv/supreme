import numpy as np
from numpy.testing import *

from supreme.noise import *
from supreme.io import imread

import os

class TestDenoise:
    def setup(self):
        self.X = imread(os.path.join(os.path.dirname(__file__),
                                     '../../lib/pywt/demo/data/aero.png'))

    def test_basic(self):
        noise = np.random.normal(loc=0, scale=30, size=self.X.shape)
        Y = dwt_denoise(self.X + noise, alpha=2350)
        assert np.sum((self.X - Y)**2) / np.prod(Y.shape) < 200

if __name__ == "__main__":
    run_module_suite()
