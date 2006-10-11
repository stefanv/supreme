import numpy as N
from numpy.testing import *

set_local_path('../../..')
from supreme import transform
import supreme.config as SC
restore_path()

class test_chirpz(NumpyTestCase):
    def test_fft(self,level=1):
        sz = 20
        x = N.arange(sz)
        a = transform.chirpz(x,1,N.exp(-1j*2*N.pi/sz),sz)
        b = N.fft.fft(x)

        assert_array_almost_equal(a,b)

if __name__ == "__main__":
    NumpyTest().run()
