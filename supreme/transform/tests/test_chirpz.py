import numpy as N
import unittest
from nose.tools import *
from numpy.testing import assert_array_equal, assert_array_almost_equal, assert_equal
from supreme import transform
import supreme.config as SC

class TestChirpz(unittest.TestCase):
    def test_fft(self,level=1):
        sz = 20
        x = N.arange(sz)
        a = transform.chirpz(x,1,N.exp(-1j*2*N.pi/sz),sz)
        b = N.fft.fft(x)

        x = N.random.random(sz) + 1j*N.random.random(sz)
        a = transform.chirpz(x,1,N.exp(-1j*2*N.pi/sz),sz)
        b = N.fft.fft(x)        

        assert_array_almost_equal(a,b)

    def test_fft2(self,level=1):
        sz = 5
        x = N.arange(sz**2).reshape((sz,sz))
        A = 1
        W = N.exp(-1j*2*N.pi/sz)
        a = transform.chirpz2(x,1,W,sz,1,W,sz)
        assert_array_almost_equal(a,N.fft.fft2(x))

if __name__ == "__main__":
    NumpyTest().run()
