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

if __name__ == "__main__":
    NumpyTest().run()
