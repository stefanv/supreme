from numpy.testing import *
import numpy as np

from supreme.register import image

class TestImage:
    def test_fft_correlate(self):
        x = np.random.random((15, 15))
        z = image.fft_correlate(x, x)
        assert_equal(np.array(z.shape) / 2,
                     np.unravel_index(z.argmax(), z.shape))

if __name__ == "__main__":
    run_module_suite()

