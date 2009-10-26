"""Register two rotated images using the log polar transform."""

import numpy as np
import matplotlib.pyplot as plt

import os.path

import supreme
import supreme.misc
from supreme.config import data_path,ftype
from supreme import transform

img1 = supreme.misc.imread(os.path.join(data_path,'NASA/hubble_crop.jpg'),flatten=True)
img2 = supreme.misc.imread(os.path.join(data_path,'NASA/hubble_crop_rot25_centre.jpg'),flatten=True)

img1_tf = transform.logpolar(img1)
img2_tf = transform.logpolar(img2)

plt.subplot(221)
plt.imshow(img1,cmap=plt.cm.gray)
plt.subplot(222)
plt.imshow(img2,cmap=plt.cm.gray)
plt.subplot(223)
plt.imshow(img1_tf,cmap=plt.cm.gray)
plt.subplot(224)
plt.imshow(img2_tf,cmap=plt.cm.gray)

cv = supreme.register.fft_correlate(img1_tf,img2_tf)
plt.figure()
plt.imshow(cv)
plt.colorbar()

print "Dims:", cv.shape
mi = np.unravel_index(cv.argmax(),cv.shape)
print "Max idx:", mi
print "Diff:", np.array(mi,ftype) - (np.array(cv.shape)-1)/2.

plt.show()
plt.close()
