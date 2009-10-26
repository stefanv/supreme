"""Demonstrate HDR (High Dynamic Range) tone mapping."""

import matplotlib.pyplot as plt

import os.path

import supreme
from supreme.config import data_path,ftype
from supreme.photometry import hdr

ic = supreme.misc.io.ImageCollection(os.path.join(data_path,
                                                  'hdr00/*_scaled.jpg'),
                                     grey=False)

ps = hdr.PhotometrySampler(ic)
dr = hdr.DeviceResponse(ps)
out = hdr.HDRMapperNaive(dr)(ic)

plt.imshow(out)
plt.show()
plt.close()
