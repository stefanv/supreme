from numpy.testing import *

from supreme import geometry as G

class TestPolygon:
    def test_area(self, level=1):
        p = G.Polygon([1,0,1], [1,0,0])
        assert_equal(p.area(), 0.5)

        p = G.Polygon([0,1,1], [0,1,0])
        assert_equal(p.area(), 0.5)

    def test_centroid(self, level=1):
        p = G.Polygon([0,1,1,0], [0,0,1,1])
        assert_equal(p.centroid(), [0.5,0.5])

    def test_inside(self, level=1):
        p = G.Polygon([0,1,1,0], [0,0,1,1])
        assert_equal(p.inside(0.5,0.5), True)

        x = [-0.5, 0.5, 1.5]
        y = [0.5, 0.5, 0.5]
        assert_equal(p.inside(x,y), [False, True, False])

if __name__ == "__main__":
    run_module_suite()
