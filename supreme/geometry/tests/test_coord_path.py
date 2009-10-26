from numpy.testing import *
import numpy as np

from supreme.geometry import coord_path
import supreme.config as SC

class TestCoordPath:
    def test_line(self):
        l = coord_path.line((0, 0), (0, 1))
        c = [coord for coord in l]
        assert_array_equal(c[0], [0, 0])
        assert_array_equal(c[-1], [0, 1])
        assert(len(c) >= 2)

    def test_build(self):
        line = coord_path.line
        l = coord_path.build(line((0, 0), (0, 3)))
        assert_array_almost_equal(l, np.array([[0, 0],
                                               [0, 1],
                                               [0, 2],
                                               [0, 3]]))
        l = coord_path.build(line((3, 0), (0, 0)))
        assert_array_almost_equal(l, np.array([[3, 0],
                                               [2, 0],
                                               [1, 0],
                                               [0, 0]]))

    def test_build_multi(self):
        line = coord_path.line
        l1 = coord_path.build(line((0, 0), (0, 2)))
        l2 = coord_path.build(line((0, 2), (0, 4)))
        l = coord_path.build(l1, l2)
        assert_array_almost_equal(l, np.array([[0, 0],
                                               [0, 1],
                                               [0, 2],
                                               [0, 3],
                                               [0, 4]]))

    def test_ftype(self):
        line = coord_path.line
        l = coord_path.build(line((0, 0), (0, 3)))
        assert_equal(np.dtype(type(l[0][0])), np.dtype(SC.itype))

    def test_nodupes(self):
        line = coord_path.line
        l = coord_path.build(line((0, 0), (5, 5)))
        lr = np.round_(l)
        for i,coord in enumerate(l[:-1]):
            assert(np.any(coord != l[i+1]))

    def test_return_indexable(self):
        line = coord_path.line
        l = coord_path.build(line((0, 0), (5, 5)))
        assert_equal(len(l[1]), 2)

    def test_rectangle(self):
        rect = coord_path.rectangle((0, 0), (1, 1))
        r = coord_path.build(rect)
        assert_array_almost_equal(r, [[0, 0],
                                      [1, 0],
                                      [1, 1],
                                      [0, 1],
                                      [0, 0]])

    def test_circle(self):
        circ = coord_path.circle((0, 0), -1)
        try:
            circ.next()
        except:
            pass
        else:
            raise Exception("Expected exception")

        circ = coord_path.circle((0, 0), 1)
        coords = [c for c in circ]
        assert_array_almost_equal(coords[0], [1., 0.])
        assert_array_almost_equal(coords[-1],[1., 0.])
        assert len(coords) > 6

        circ = coord_path.circle((1, 1), 1)
        assert not np.allclose(circ.next(), [1., 0.])

    def test_spline(self):
        try:
            import Nurbs
        except:
            return
        try:
            spl = coord_path.spline(((0, 0), (3, 5)))
        except ValueError:
            pass
        else:
            raise Exception("ValueError expected (%s)" % spl.next)

        spl = coord_path.spline(((0, 0), (3, 5), (1, 1)))
        coords = [c for c in spl]
        assert(len(coords) > 10)
        assert_array_almost_equal(coords[0], (0, 0))
        assert_array_almost_equal(coords[-1], (1, 1))

if __name__ == "__main__":
    run_module_suite()

