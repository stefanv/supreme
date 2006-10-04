import numpy as N
from numpy.testing import *

set_local_path('../../..')
from supreme import ext
import supreme.config as SC
restore_path()

class test_libsupreme(NumpyTestCase):
    def test_variance_map(self,level=1):
        x = N.arange(12).reshape((3,4))
        
        vm = ext.variance_map(x)
        assert_almost_equal(vm[1,1], N.var(x[:3,:3]))
        assert_almost_equal(vm[1,2], N.var(x[:3,1:4]))

        self.failUnlessRaises(AssertionError, ext.variance_map,
                              N.empty((1,1,1)))

    def test_line_intersect(self,level=1):
        assert_equal(((0.5,0.5),0), ext.line_intersect(0.5,0,0.5,1, 0,0.5,1,0.5))
        assert_equal(((2,2),1), ext.line_intersect(0,0,1,1, 0,4,4,0))
        assert_equal(((0,0),2), ext.line_intersect(0,0,1,0, 0,1,1,1))
        assert_equal(((0,0),3), ext.line_intersect(0,0,1,0, 2,0,4,0))

if __name__ == "__main__":
    NumpyTest().run()
