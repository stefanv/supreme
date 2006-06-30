import numpy as N
from numpy.testing import *

set_local_path('../../..')
from supreme.register import image
restore_path()

class test_image(NumpyTestCase):
    def check_fft_correlate(self):
        x = N.random.random((15,15))
        z = image.fft_correlate(x,x)
        assert_equal(N.array(z.shape)/2,
                     N.unravel_index(z.argmax(),z.shape))
    
if __name__ == "__main__":
    NumpyTest().run()
