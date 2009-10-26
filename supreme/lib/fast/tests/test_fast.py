from numpy.testing import *
import numpy as np

from supreme.lib import fast

class TestLibfast:
    def setUp(self):
        self.img0 = (np.random.random((80, 50)) * 255)
        self.img1 = self.img0.astype(np.uint8)

    def test_basic(self):
        for n in range(9, 13):
            xy = fast.corner_detect(self.img0, size=n)
            height, width = self.img0.shape
            assert len(xy) > 0
            for x, y in xy:
                assert((x >= 0) and (x < width))
                assert((y >= 0) and (y < height))

    def test_barrier(self):
        xy0 = fast.corner_detect(self.img0, barrier=10)
        xy1 = fast.corner_detect(self.img0, barrier=20)
        assert(len(xy0) > len(xy1))

    def test_input_image(self):
        xy0 = fast.corner_detect(self.img0, size=9)
        xy1 = fast.corner_detect(self.img1, size=9)
        assert_array_equal(xy0, xy1)

    def test_size_fail(self):
        for sz in (8, 13):
            try:
                fast.corner_detect(self.img0, size=sz)
            except ValueError:
                pass
            else:
                raise Exception("Expected ValueError")

if __name__ == "__main__":
    run_module_suite()

