import numpy as np
import unittest
from nose.tools import *
from numpy.testing import assert_array_equal, assert_array_almost_equal, assert_equal
from supreme import transform
import supreme.config as SC

class TestChirpz(unittest.TestCase):
    def test_fft(self,level=1):
        sz = 20
        x = np.arange(sz)
        print transform.chirpz
        a = transform.chirpz(x,1,np.exp(-1j*2*np.pi/sz),sz)
        b = np.fft.fft(x)

        x = np.random.random(sz) + 1j*np.random.random(sz)
        a = transform.chirpz(x,1,np.exp(-1j*2*np.pi/sz),sz)
        b = np.fft.fft(x)

        assert_array_almost_equal(a,b)

    def test_fft2(self,level=1):
        sz = 5
        x = np.arange(sz**2).reshape((sz,sz))
        A = 1
        W = np.exp(-1j*2*np.pi/sz)
        a = transform.chirpz2(x,1,W,sz,1,W,sz)
        assert_array_almost_equal(a,np.fft.fft2(x))

if __name__ == "__main__":
    NumpyTest().run()
