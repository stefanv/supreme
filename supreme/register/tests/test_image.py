from numpy.testing import *
import numpy as np

from supreme.register import image

class TestImage:
    def test_fft_corr(self):
        x = np.random.random((15, 15))
        z = image.fft_corr(x, x)
        assert_equal(np.array(z.shape) / 2,
                     np.unravel_index(z.argmax(), z.shape))

def phase_corr_wrap(x, y):
    out = image.phase_corr(x, y)
    m, n = np.unravel_index(np.argmax(out), out.shape)
    return m, n, out[m, n]

class TestPhaseCorr:
    def test_basic(self):
        x = np.random.random((50, 50))
        y = x + np.random.random((50, 50)) * 0.1

        m, n, p = phase_corr_wrap(x, x)
        assert_almost_equal((m, n, p), (0, 0, 1))

    def test_basic_with_noise(self):
        x = np.random.random((50, 50))
        y = x + np.random.random((50, 50)) * 0.1

        m, n, p = phase_corr_wrap(x, y)
        assert_almost_equal((m, n, p), (0, 0, 0.98), decimal=1)

    def test_shift(self):
        x = np.random.random((50, 50))
        y = np.zeros_like(x)
        y[10:, 10:] = x[0:-10, 0:-10]

        m, n, p = phase_corr_wrap(y, x)
        assert_almost_equal((m, n), (10, 10))


if __name__ == "__main__":
    run_module_suite()

