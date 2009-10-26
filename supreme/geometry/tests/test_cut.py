from numpy.testing import *
import numpy as np

from supreme.geometry import cut, coord_path

class TestCut:
    def test_centre_cut(self):
        p = coord_path.build(coord_path.line((1, 1), (1, 1)))
        image = np.arange(12).reshape((4,3))
        cp = cut.along_path(p, image, shape=(3,3))

        cut_img = cp.next()
        assert_equal(cut_img.shape, (3,3))
        assert_array_almost_equal(cut_img, [[0, 1, 2],
                                            [3, 4, 5],
                                            [6, 7, 8]])

    def test_corner_cut(self):
        p = coord_path.build(coord_path.line((0, 0), (1, 0)))
        image = np.arange(12).reshape((4, 3))
        cp = cut.along_path(p, image,shape=(3, 3), centre=(0, 0))

        cut_img = cp.next()
        assert_equal(cut_img.shape, (3, 3))
        assert_array_almost_equal(cut_img, [[0, 1, 2],
                                            [3, 4, 5],
                                            [6, 7, 8]])

        cut_img = cp.next()
        assert_equal(cut_img.shape, (3, 3))
        assert_array_almost_equal(cut_img, [[3, 4, 5],
                                            [6, 7, 8],
                                            [9, 10, 11]])

    def test_outside(self):
        p = coord_path.build(coord_path.line((4, 4), (4, 4)))
        image = np.arange(12).reshape((4, 3))
        cp = cut.along_path(p,image,shape=(5, 5),centre=(0, 0))
        list(cp)

    def test_completely_outside(self):
        p = (50, 50)
        image = np.arange(12).reshape((4, 3))
        cp = cut.along_path(p,image,shape=(5, 5),centre=(0, 0))
        list(cp)

    @raises(ValueError)
    def test_2D(self):
        cut.along_path(None, None, shape=(3, 3, 3)).next()

    def test_colour_cut(self):
        p = coord_path.build(coord_path.line((0, 0), (0, 0)))
        image = np.arange(27).reshape((3, 3, 3))
        cp = cut.along_path(p,image, shape=(3, 3), centre=(0, 0))
        cut_img = cp.next()
        assert_equal(cut_img.shape, (3, 3, 3))
        assert_equal(cut_img[:], image[:])

    def test_dtype(self):
        p = coord_path.build(coord_path.line((0, 0), (0, 0)))
        image = np.arange(12).reshape((4, 3)).astype(np.uint8)
        cut_img = cut.along_path(p, image).next()
        assert_equal(image.dtype, cut_img.dtype)

if __name__ == "__main__":
    run_module_suite()

