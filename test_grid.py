import numpy as N
from numpy.testing import *
from grid import *

class test_grid(ScipyTestCase):
    def check_init(self, level=1):
        g = Grid(2,2)
        assert_array_almost_equal(g['x'], N.array([[0,1],[0,1]]))
        assert_array_almost_equal(g['y'], N.array([[0,0],[1,1]]))
        assert_array_almost_equal(g['z'], N.array([[1,1],[1,1]]))

if __name__ == "__main__":
    ScipyTest().run()
