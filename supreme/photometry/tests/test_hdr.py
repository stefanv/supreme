import os.path

from numpy.testing import *

import supreme
import supreme.io
from supreme.photometry import hdr

class TestHdr:
    data_path = os.path.join(os.path.dirname(__file__),'../../io/tests')
    data_glob = os.path.join(data_path,'exif_tagged*.jpg')

    def test_naive(self):
        ic = supreme.io.ImageCollection(self.data_glob)
        ps = hdr.PhotometrySampler(ic)
        dr = hdr.DeviceResponse(ps)
        out = hdr.HDRMapperNaive(dr)(ic)

if __name__ == "__main__":
    run_module_suite()

