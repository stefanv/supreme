"""Register a collection of images, using the log polar transform."""

import numpy as np
import matplotlib.pyplot as plt
import scipy as sp

import os.path
import glob

import supreme
from supreme.config import data_path
from supreme import register
import supreme as SR
import supreme.io

def getframes(path):
    return [supreme.io.imread(fn,flatten=True) for fn in
            sorted(glob.glob(os.path.join(data_path,path)))]

images = getframes('toystory/*.png')[:5]
#images = getframes('test/flower*.jpg')
#images = getframes('test/olie*.jpg')
#images = getframes('reflectometer/*.png')
#images = getframes('chris/Q*.png')
#images = getframes('ooskus/dscf172*cropped.jpg')

#images = getframes('sec/*scaled*.jpg')
#images = getframes('hanno/*crop*.png')

print "Input image size:", images[0].shape

frames = images
accepted_frames,tf_matrices = \
                          register.logpolar(frames[0],frames[1:],
                                            variance_threshold=0.1,
                                            angles=180,
                                            peak_thresh=5, window_shape=(131,131))

tf_matrices = [np.eye(3)] + list(tf_matrices)
usedframes = [frames[0]] + list(frames[i+1] for i in accepted_frames)

#print "Iteratively refining frames (this may take a while)..."
#tf_matrices = [tf_matrices[0]] + \
#              [register.refine(usedframes[0],F,tf_matrices[0],M)
#               for F,M in zip(usedframes[1:],tf_matrices[1:])]

print "Reconstructing..."
scale = 1
for m in tf_matrices:
    m[:2,:] *= scale

for u in usedframes:
    u -= u.min()
out = register.stack.with_transform(usedframes, tf_matrices)

interp = 'nearest'
plt.imshow(out,cmap=plt.cm.gray,interpolation=interp)
plt.xticks([])
plt.yticks([])
plt.show()

#sp.misc.pilutil.imsave('/tmp/data.eps',out)
