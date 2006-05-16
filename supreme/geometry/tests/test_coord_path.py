import numpy as N
from numpy.testing import *

set_local_path('../../..')
from supreme.geometry import coord_path
from supreme.config import ftype
restore_path()

class test_coord_path(NumpyTestCase):
    def check_line(self,level=1):
        l = coord_path.line((0,0),(0,1))
        c = [coord for coord in l]
        assert_array_equal(c[0], [0,0])
        assert_array_equal(c[-1], [0,1])
        assert(len(c) >= 2)

    def check_build(self,level=1):
        line = coord_path.line
        l = coord_path.build(line((0,0),(0,3)))
        assert_almost_equal(l,N.array([[0,0],[0,1],[0,2],[0,3]]))
        l = coord_path.build(line((3,0),(0,0)))
        assert_almost_equal(l,N.array([[3,0],[2,0],[1,0],[0,0]]))

    def check_ftype(self,level=1):
        line = coord_path.line
        l = coord_path.build(line((0,0),(0,3)))
        assert_equal(N.dtype(type(l[0][0])),N.dtype(ftype))

    def check_nodupes(self,level=1):
        line = coord_path.line
        l = coord_path.build(line((0,0),(5,5)))
        lr = N.round_(l)
        for i,coord in enumerate(l[:-1]):
            assert(N.any(coord != l[i+1]))

    def check_return_list(self,level=1):
        line = coord_path.line
        l = coord_path.build(line((0,0),(5,5)))
        assert_equal(type(l), type(list()))
            
if __name__ == "__main__":
    NumpyTest().run()
