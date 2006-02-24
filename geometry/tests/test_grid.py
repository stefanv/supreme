import numpy as N
from numpy.testing import *

from supreme.geometry import Grid

class test_grid(NumpyTestCase):
    def check_init(self, level=1):
        g = Grid(2,2)
        assert_array_almost_equal(g['x'], N.array([[0,1],[0,1]]))
        assert_array_almost_equal(g['y'], N.array([[0,0],[1,1]]))
        assert_array_almost_equal(g['z'], N.array([[1,1],[1,1]]))

    def check_coords(self, level=1):
        g = Grid(1,3)
        assert_array_almost_equal(g.coords, N.array([[0,0,1], [1,0,1], [2,0,1]]))        
        g = Grid(2,2)
        assert_array_almost_equal(g.coords, N.array([[0,0,1], [1,0,1], [0,1,1], [1,1,1]]))
        

if __name__ == "__main__":
    NumpyTest().run()
