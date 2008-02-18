import numpy as N
import unittest
from nose.tools import *
from numpy.testing import assert_array_equal, assert_array_almost_equal, assert_equal
from supreme.register import image

class TestImage(unittest.TestCase):
    def test_fft_correlate(self):
        x = N.random.random((15,15))
        z = image.fft_correlate(x,x)
        assert_equal(N.array(z.shape)/2,
                     N.unravel_index(z.argmax(),z.shape))
    
if __name__ == "__main__":
    NumpyTest().run()
