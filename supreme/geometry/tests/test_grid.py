import numpy as N
from numpy.testing import *

set_local_path('../../..')
from supreme.geometry import Grid
restore_path()
    
class test_grid(NumpyTestCase):
    def check_init(self, level=1):
        g0 = Grid([0,1],[0,1])
        g1 = Grid(2,2)
        g2 = Grid([[0,0],[1,1]],[[0,1],[0,1]])
        for g in [g0,g1,g2]:
            assert_array_almost_equal(g['cols'], N.array([[0,1],[0,1]]))
            assert_array_almost_equal(g['rows'], N.array([[0,0],[1,1]]))
            assert_array_almost_equal(g['z'], N.array([[1,1],[1,1]]))

    def check_coords(self, level=1):
        g = Grid([0],[0,1,2])
        assert_array_almost_equal(g.coords, N.array([[[0,0,1], [1,0,1], [2,0,1]]]))        
        g = Grid([0,1],[0,1])
        assert_array_almost_equal(g.coords, N.array([[[0,0,1], [1,0,1]], [[0,1,1], [1,1,1]]]))

    def check_coords_readonly(self, level=2):
        g = Grid([0],[0])
        try:
            g.coords = []
        except AttributeError:
            pass
        else:
            fail("should not be able to set coords")

    def check_getitem(self, level=1):
        g = Grid([0],[0])
        assert_array_almost_equal(g['cols'], N.array([[0]]))

    def check_fields(self, level=1):
        g = Grid([0],[0])
        assert_equal(g['cols'], g.cols)

if __name__ == "__main__":
    NumpyTest().run()
