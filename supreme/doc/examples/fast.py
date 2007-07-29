import os
import numpy as N

from numpy.testing import set_local_path, restore_path
set_local_path('../../..')
from supreme.lib import fast
from supreme.config import data_path
from supreme.misc.io import ImageCollection
restore_path()

import scipy as S
imread = S.misc.pilutil.imread
imsave = S.misc.pilutil.imsave

ic = ImageCollection(os.path.join(data_path,'toystory/toystory00*.png'),
                     grey=True)

xy0 = fast.corner_detect(ic[0],barrier=10)
xy1 = fast.corner_detect(ic[1])

def mark_feature(img,xy):
    shape = list(img.shape) + [3]
    rgb = N.zeros(shape,N.uint8)
    for band in range(3):
        rgb[:,:,band].flat = img
    for x,y in xy:
        rgb[y,x] = [255,0,0]
    return rgb

img0 = mark_feature(ic[0],xy0)
img1 = mark_feature(ic[1],xy1)

import pylab as P
P.subplot(121)
P.imshow(img0)
P.subplot(122)
P.imshow(img1)
P.show()
P.close()
