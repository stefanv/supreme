"""Register two rotated images using the log polar transform."""

from numpy.testing import set_local_path, restore_path
import numpy as N
import pylab as P
import scipy as S

import os.path

set_local_path('../../..')
import supreme
from supreme.config import data_path,ftype
from supreme import transform
restore_path()

img1 = supreme.imread(os.path.join(data_path,'NASA/hubble_crop.jpg'),flatten=True)
img2 = supreme.imread(os.path.join(data_path,'NASA/hubble_crop_rot25_centre.jpg'),flatten=True)

img1_tf = transform.logpolar(img1)
img2_tf = transform.logpolar(img2)

P.subplot(221)
P.imshow(img1,cmap=P.cm.gray)
P.subplot(222)
P.imshow(img2,cmap=P.cm.gray)
P.subplot(223)
P.imshow(img1_tf,cmap=P.cm.gray)
P.subplot(224)
P.imshow(img2_tf,cmap=P.cm.gray)

cv = supreme.register.fft_correlate(img1_tf,img2_tf)
P.figure()
P.imshow(cv)
P.colorbar()

print "Dims:", cv.shape
mi = N.unravel_index(cv.argmax(),cv.shape)
print "Max idx:", mi
print "Diff:", N.array(mi,ftype) - (N.array(cv.shape)-1)/2.

P.show()
P.close()
