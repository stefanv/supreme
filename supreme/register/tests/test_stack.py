import numpy as N
from numpy.testing import *

set_local_path('../../..')
from supreme.register import stack
restore_path()

class test_stack(NumpyTestCase):
    def check_corners(self):
        corners = stack.corners((3,5))
        assert_array_almost_equal(corners, [[0,0],
                                            [0,4],
                                            [2,0],
                                            [2,4]])

    def test_affine(self):
        pass
    
if __name__ == "__main__":
    NumpyTest().run()
