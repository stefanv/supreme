"""Demonstrate HDR (High Dynamic Range) tone mapping."""

from numpy.testing import set_local_path, restore_path
import numpy as N
import pylab as P

import os.path

set_local_path('../../..')
import supreme
from supreme.config import data_path,ftype
from supreme.photometry import hdr
restore_path()

ic = supreme.misc.io.ImageCollection(os.path.join(data_path,
                                                  'hdr00/*_scaled.jpg'),
                                     grey=False)

ps = hdr.PhotometrySampler(ic)
dr = hdr.DeviceResponse(ps)
out = hdr.HDRMapperNaive(dr)(ic)

P.imshow(out)
P.show()
P.close()
