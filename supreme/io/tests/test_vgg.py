import numpy as np
from numpy.testing import *

import os

from supreme.io.vgg import *

class TestVGG:
    def setup(self):
        self.ic = load_vgg(os.path.join(os.path.dirname(__file__), 'vgg_test'))

    def test_basic(self):
        assert_array_equal(self.ic[0].info['H'], np.eye(3))

if __name__ == "__main__":
    run_module_suite()
