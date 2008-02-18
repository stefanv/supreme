import numpy as N
import unittest
from nose.tools import *
from numpy.testing import assert_array_equal, assert_array_almost_equal, assert_equal
from supreme.lib import klt
import supreme.config as SC

class TestLibklt(unittest.TestCase):
    def test_basic(self):
        img1 = N.zeros((128,128),dtype=N.uint8)
        img2 = N.zeros((128,128),dtype=N.uint8)

        rand = lambda x: (N.random.random(x)*x).astype(N.uint8)

        img1[rand(128),rand(128)] = 255
        img2[rand(128),rand(128)] = 255

        tc = klt.TrackingContext()
        fl = klt.FeatureList(100)
        klt.select_good_features(tc, img1, fl)
        klt.track_features(tc, img1, img2, fl)
        fl.to_image(img2)

        assert_equal(len(fl),100)

        fa = fl.as_array()
        values = fa['val']
        assert 0 <= len(values[values != -1]) <= 100

if __name__ == "__main__":
    NumpyTest().run()
