import numpy as np
from numpy.testing import *

import supreme.register as sr
from supreme.register.ncorr import window_wrap

def test_sat():
    x = np.arange(12).reshape((4,3))

    x = (np.random.random((50, 50)) * 255).astype(np.uint8)
    assert_equal(sr.sat(x)[-1, -1],
                 x.sum())

def test_xcorr_basic():
    x = (np.random.random((10, 10)) * 255).astype(np.uint8)

    y = (np.random.random((30, 30)) * 255).astype(np.uint8)
    y[13:23, 7:17] = x

    c = sr.ncc(y, x)

    assert_equal(np.unravel_index(np.argmax(c), c.shape),
                 (13, 7))

    assert_almost_equal(c[13, 7], 1)

def plot_box(coords, mode='r-', **plot_args):
    import matplotlib.pyplot as plt
    y0, x0, y1, x1 = coords
    plt.plot([x0, x1, x1, x0, x0], [y0, y0, y1, y1, y0], mode, **plot_args)

class TestWindowWrap:
    def _check(self, coords, win_shape, expected):
        m0, n0, m1, n1 = coords
        result = window_wrap(m0, n0, m1, n1, *win_shape)
        assert_equal(result, expected)

    def test_basic(self):
        # main, column_wrap, row_wrap, diagonal_wrap
        yield self._check, (2, 2, 3, 3), (5, 5), \
                           [[2, 2, 3, 3],
                            [-1, -1, -1, -1],
                            [-1, -1, -1, -1],
                            [-1, -1, -1, -1]]

    def test_wrap_diagonal(self):
        yield self._check, (3, 3, 6, 6), (5, 5), \
                           [[3, 3, 4, 4],
                            [3, 0, 4, 1],
                            [0, 3, 1, 4],
                            [0, 0, 1, 1]]

    def test_wrap_horizontal(self):
        yield self._check, (3, 3, 4, 6), (5, 5), \
                           [[3, 3, 4, 4],
                            [3, 0, 4, 1],
                            [-1, -1, -1, -1],
                            [-1, -1, -1, -1]]

    def test_wrap_vertical(self):
        yield self._check, (3, 3, 6, 4), (5, 5), \
                           [[3, 3, 4, 4],
                            [-1, -1, -1, -1],
                            [0, 3, 1, 4],
                            [-1, -1, -1, -1]]

##     def test_plot(self):
##         import matplotlib.pyplot as plt
##         windows = window_wrap(50, 50, 150, 150, 100, 100)
##         print windows
##         for i in range(4):
##             plot_box(windows[i])
##         plt.show()


class TestSatSum:
    x = (np.random.random((50, 50)) * 255).astype(np.uint8)
    s = sr.sat(x)

    def test_basic(self):
        x, s = self.x, self.s

        assert_equal(x[12:24, 10:20].sum(), sr.sat_sum(s, 12, 10, 23, 19))
        assert_equal(x[:20, :20].sum(), sr.sat_sum(s, 0, 0, 19, 19))
        assert_equal(x[:20, 10:20].sum(), sr.sat_sum(s, 0, 10, 19, 19))
        assert_equal(x[10:20, :20].sum(), sr.sat_sum(s, 10, 0, 19, 19))

    def test_single(self):
        assert_equal(self.x[0, 0], sr.sat_sum(self.s, 0, 0, 0, 0))
        assert_equal(self.x[10, 10], sr.sat_sum(self.s, 10, 10, 10, 10))


if __name__ == '__main__':
    run_module_suite()
