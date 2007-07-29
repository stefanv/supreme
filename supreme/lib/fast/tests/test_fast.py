import numpy as N
from numpy.testing import *

set_local_path('../../../..')
from supreme.lib import fast
import supreme.config as SC
restore_path()

class test_libfast(NumpyTestCase):
    def setUp(self):
        self.img0 = (N.random.random((80,50))*255)
        self.img1 = self.img0.astype(N.uint8)

    def test_basic(self):
        for n in range(9,13):
            xy = fast.corner_detect(self.img0,size=n)
            height,width = self.img0.shape
            assert len(xy) > 0
            for x,y in xy:
                assert((x >= 0) and (x < width))
                assert((y >= 0) and (y < height))

    def test_barrier(self):
        xy0 = fast.corner_detect(self.img0,barrier=10)
        xy1 = fast.corner_detect(self.img0,barrier=20)
        assert(len(xy0) > len(xy1))

    def test_input_image(self):
        xy0 = fast.corner_detect(self.img0,size=9)
        xy1 = fast.corner_detect(self.img1,size=9)
        assert_array_equal(xy0,xy1)

    def test_size_fail(self):
        self.failUnlessRaises(ValueError,fast.corner_detect,self.img0,size=8)
        self.failUnlessRaises(ValueError,fast.corner_detect,self.img0,size=13)

if __name__ == "__main__":
    NumpyTest().run()
