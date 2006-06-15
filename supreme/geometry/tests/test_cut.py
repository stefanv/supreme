import numpy as N
from numpy.testing import *

set_local_path('../../..')
from supreme.geometry import cut,coord_path
from supreme.config import ftype,itype
restore_path()

class test_cut(NumpyTestCase):
    def check_centre_cut(self):
        p = coord_path.build(coord_path.line((1,1),(1,1)))
        image = N.arange(12).reshape((4,3))
        cp = cut.along_path(p,image,shape=(3,3))
        
        cut_img = cp.next()
        assert_equal(cut_img.shape,(3,3))
        assert_array_almost_equal(cut_img,[[0,1,2],[3,4,5],[6,7,8]])

    def check_corner_cut(self):
        p = coord_path.build(coord_path.line((0,0),(1,0)))
        image = N.arange(12).reshape((4,3))
        cp = cut.along_path(p,image,shape=(3,3),centre=(0,0))

        cut_img = cp.next()
        assert_equal(cut_img.shape,(3,3))
        assert_array_almost_equal(cut_img,[[0,1,2],[3,4,5],[6,7,8]])

        cut_img = cp.next()
        assert_equal(cut_img.shape,(3,3))
        assert_array_almost_equal(cut_img,[[3,4,5],[6,7,8],[9,10,11]])
        
if __name__ == "__main__":
    NumpyTest().run()
