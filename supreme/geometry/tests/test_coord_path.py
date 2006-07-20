import numpy as N
from numpy.testing import *

set_local_path('../../..')
from supreme.geometry import coord_path
from supreme.config import ftype,itype
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

    def check_build_multi(self,level=1):
        line = coord_path.line
        l1 = coord_path.build(line((0,0),(0,2)))
        l2 = coord_path.build(line((0,2),(0,4)))
        l = coord_path.build(l1,l2)
        assert_almost_equal(l,N.array([[0,0],[0,1],[0,2],[0,3],[0,4]]))

    def check_ftype(self,level=1):
        line = coord_path.line
        l = coord_path.build(line((0,0),(0,3)))
        assert_equal(N.dtype(type(l[0][0])),N.dtype(itype))

    def check_nodupes(self,level=1):
        line = coord_path.line
        l = coord_path.build(line((0,0),(5,5)))
        lr = N.round_(l)
        for i,coord in enumerate(l[:-1]):
            assert(N.any(coord != l[i+1]))

    def check_return_indexable(self,level=1):
        line = coord_path.line
        l = coord_path.build(line((0,0),(5,5)))
        assert_equal(len(l[1]),2)

    def check_rectangle(self,level=1):
        rect = coord_path.rectangle((0,0),(1,1))
        r = coord_path.build(rect)
        assert_array_almost_equal(r,[[0,0],[1,0],[1,1],[0,1],[0,0]])

    def check_circle(self,level=1):
        circ = coord_path.circle((0,0),-1)
        self.failUnlessRaises(ValueError,circ.next)

        circ = coord_path.circle((0,0),1)
        coords = [c for c in circ]
        assert_array_almost_equal(coords[0],[1.,0.])
        assert_array_almost_equal(coords[-1],[1.,0.])
        assert len(coords) > 6

        circ = coord_path.circle((1,1),1)
        assert not N.allclose(circ.next(),[1.,0.])

    def check_spline(self,level=2):
        spl = coord_path.spline(((0,0),(3,5)))
        self.failUnlessRaises(ValueError,spl.next)
        
        spl = coord_path.spline(((0,0),(3,5),(1,1)))
        coords = [c for c in spl]
        assert(len(coords) > 10)
        assert_array_almost_equal(coords[0], (0,0))
        assert_array_almost_equal(coords[-1], (1,1))
    
if __name__ == "__main__":
    NumpyTest().run()
