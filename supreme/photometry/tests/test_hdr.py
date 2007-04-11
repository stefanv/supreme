import numpy as N
from numpy.testing import *

import os

set_local_path('../../..')
import supreme
from supreme.photometry import hdr
restore_path()

class test_hdr(NumpyTestCase):
    data_path = os.path.join(os.path.dirname(__file__),'../../misc/tests')
    data_glob = os.path.join(data_path,'exif_tagged*.jpg')

    def test_naive(self):
        ic = supreme.misc.io.ImageCollection(self.data_glob)
        ps = hdr.PhotometrySampler(ic)
        dr = hdr.DeviceResponse(ps)
        out = hdr.HDRMapperNaive(dr)(ic)

if __name__ == "__main__":
    NumpyTest().run()
