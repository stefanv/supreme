import numpy as N
import pylab as P
from numpy.testing import *

set_local_path('../../..')
from supreme import transform
from supreme.transform.transform import stackcopy
import supreme.config as SC
restore_path()

class test_transform(NumpyTestCase):
    def check_logpolar(self,level=1):
        x = N.zeros((3,3))
        z = transform.logpolar(x)
        assert_equal(z.shape,(359,3))

        x = N.zeros((3,3,3))
        z = transform.logpolar(x)
        assert_equal(z.shape,(359,3,3))

        x = N.zeros((3,3,4))
        z = transform.logpolar(x)
        assert_equal(z.shape,(359,3,4))
        z = transform.logpolar(x,angles=400)        
        assert_equal(z.shape,(400,3,4))

        x = N.zeros((3))
        self.failUnlessRaises(ValueError, transform.logpolar, x)

    def test_stackcopy(self,level=1):
        layers = 4
        x = N.empty((3,3,layers))
        y = N.eye(3,3)
        stackcopy(x,y)
        for i in range(layers):
            assert_array_almost_equal(x[...,i],y)

    def test_matrix(self,level=1):
        x = N.arange(9).reshape((3,3))+1
        theta = -N.pi/2
        M = N.array([[N.cos(theta),-N.sin(theta),0],
                     [N.sin(theta), N.cos(theta),2],
                     [0,            0,           1]])
        x90 = transform.matrix(x,M,order=1)
        assert_array_almost_equal(x90,N.rot90(x))        

if __name__ == "__main__":
    NumpyTest().run()
