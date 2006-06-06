import numpy as N
import pylab as P
from numpy.testing import *

set_local_path('../../..')
from supreme.transform import *
from supreme.transform.transform import stackcopy
import supreme.config as SC
restore_path()

class test_transform(NumpyTestCase):
    def check_logpolar(self,level=1):
        x = N.zeros((3,3))
        z = logpolar(x)
        assert_equal(z.shape,(359,3))

        x = N.zeros((3,3,3))
        z = logpolar(x)
        assert_equal(z.shape,(359,3,3))

        x = N.zeros((3,3,4))
        z = logpolar(x)
        assert_equal(z.shape,(359,3,4))
        z = logpolar(x,angles=400)        
        assert_equal(z.shape,(400,3,4))

        x = N.zeros((3))
        self.failUnlessRaises(ValueError, logpolar, x)

    def test_stackcopy(self,level=1):
        layers = 4
        x = N.empty((3,3,layers))
        y = N.eye(3,3)
        stackcopy(x,y)
        for i in range(layers):
            assert_array_almost_equal(x[...,i],y)
        

if __name__ == "__main__":
    NumpyTest().run()
