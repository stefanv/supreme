from numpy.testing import *
import numpy as np

from supreme import ext
from supreme.geometry import Polygon

class TestLibsupreme:
    def test_variance_map(self):
        x = np.arange(12).reshape((3, 4))

        vm = ext.variance_map(x)
        assert_almost_equal(vm[1, 1], np.var(x[:3,:3]))
        assert_almost_equal(vm[1, 2], np.var(x[:3,1:4]))

    @raises(AssertionError)
    def test_empty(self):
        ext.variance_map(np.empty((1, 1, 1)))

    def test_line_intersect(self,):
        assert_equal(((0.5, 0.5), 0),
                     ext.line_intersect(0.5, 0, 0.5, 1, 0, 0.5, 1, 0.5))
        assert_equal(((2, 2), 1), ext.line_intersect(0, 0, 1, 1, 0, 4, 4, 0))
        assert_equal(((0, 0), 2), ext.line_intersect(0, 0, 1, 0, 0, 1, 1, 1))
        assert_equal(((0, 0), 3), ext.line_intersect(0, 0, 1, 0, 2, 0, 4, 0))

    @raises(AssertionError)
    def fail_poly_clip(self, *args):
        ext.poly_clip(*args)

    def test_poly_clip(self):
        x = [0,  1, 2, 1]
        y = [0, -1, 0, 1]

        xc, yc = ext.poly_clip(x, y, 0, 1, 1, 0)
        assert_equal(Polygon(xc, yc).area(), 0.5)

        x = [-1, 1.5, 1.5, -1]
        y = [.5, 0.5, 1.5, 1.5]
        xc,yc = ext.poly_clip(x, y, 0, 1, 1, 0)
        assert_equal(Polygon(xc, yc).area(), 0.5)

        fail_poly_clip = raises(AssertionError)(ext.poly_clip)
        yield(fail_poly_clip, [1], [1, 2], 0, 0, 0, 0)
        yield(fail_poly_clip, [1, 2], [1, 2], 0, 10, -1, 10)
        yield(fail_poly_clip, [1, 2], [1, 2], 10, 0, 10, 0)

    def test_correlate(self):
        assert_equal(ext.correlate([[0, 1, 2]], [[0, 1, 2]]),
                     [[5, 2, 0]])

        x = [[1, 1, 2],
             [3, 2, 1]]
        y = [[1, 5, 3],
             [3, 7, 9]]

        assert_equal(ext.correlate(x, y),
                     [[44, 24, 5],
                      [16, 7,  1]])

        assert_equal(ext.correlate(x, y, mode_column='mirror'),
                                   [[44, 54, 52],
                                    [16, 16, 22]])

        assert_equal(ext.correlate(x, y, mode_row='mirror'),
                     [[44, 24, 5],
                      [44, 24, 7]])

        assert_equal(ext.correlate(x, y, mode_row='mirror',
                                   mode_column='mirror'),
                     [[44, 54, 52],
                      [44, 42, 44]])

    def test_interp_bilinear(self):
        x = np.mgrid[:10, :10].sum(axis=0)
        out = ext.interp_bilinear(x, [[1, 2], [1.5, 1.5]],
                                     [[2, 1], [1.5, 1.5]])
        assert_equal(out, [[3, 3], [3, 3]])

if __name__ == "__main__":
    run_module_suite()

