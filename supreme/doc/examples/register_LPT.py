"""Register two rotated images using the log polar transform."""

from numpy.testing import set_local_path, restore_path
import numpy as N
import pylab as P
import scipy as S
S.pkgload('signal')

import os.path

set_local_path('../../..')
import supreme
from supreme.config import data_path
from supreme import transform
restore_path()

img1 = supreme.imread(os.path.join(data_path,'NASA/hubble_crop.jpg'),flatten=True)
img2 = supreme.imread(os.path.join(data_path,'NASA/hubble_crop_rot25.jpg'),flatten=True)

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

cv = S.signal.fftconvolve(img1,img1)
#cv = cv/cv.max()
P.figure()
P.imshow(cv)
P.colorbar()

print "Dims:", cv.shape
print "Max idx:", N.unravel_index(cv.argmax(),cv.shape)

P.show()
P.close()
