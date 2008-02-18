import numpy as N
import unittest
from nose.tools import *
from numpy.testing import assert_array_equal, assert_array_almost_equal, assert_equal
import os

import supreme
from supreme.photometry import hdr

class TestHdr(unittest.TestCase):
    data_path = os.path.join(os.path.dirname(__file__),'../../misc/tests')
    data_glob = os.path.join(data_path,'exif_tagged*.jpg')

    def test_naive(self):
        ic = supreme.misc.io.ImageCollection(self.data_glob)
        ps = hdr.PhotometrySampler(ic)
        dr = hdr.DeviceResponse(ps)
        out = hdr.HDRMapperNaive(dr)(ic)

if __name__ == "__main__":
    NumpyTest().run()
