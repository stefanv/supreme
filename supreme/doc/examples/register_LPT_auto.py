"""Register a collection of images, using the log polar transform."""

from numpy.testing import set_local_path, restore_path
import numpy as N
import pylab as P
import scipy as S

import os.path
import glob

set_local_path('../../..')
import supreme
from supreme.config import data_path,ftype
from supreme import register
import supreme as SR
restore_path()

def getframes(path):
    return [supreme.imread(fn,flatten=True) for fn in
            glob.glob(os.path.join(data_path,path))]

#images = getframes('toystory/*.png')
#images = getframes('test/flower*.jpg')
#images = getframes('test/olie*.jpg') # beta 1.9, window_shape=(30,30)
images = getframes('chris/Q*.png') # angles=80,alpha=0,beta=-1,
#                                   # window_shape=(71,71))

#images = getframes('sec/*scaled*.jpg')
#images = getframes('hanno/*crop*.png')

# frames that work well: 1,2,(4),(8),(9),11,
#frames = [images[i] for i in [0,1,2,11]] # don't say a word, it's late
#frames = [images[1],images[0]] + images[2:]

frames = images
accepted_frames,tf_matrices = register.logpolar(frames[0],frames[1:],
                                                variance_threshold=0.7,
                                                angles=80,alpha=1,beta=1,window_shape=(71,71))

tf_matrices = [N.eye(3)] + list(tf_matrices)
usedframes = [frames[0]] + list(frames[i+1] for i in accepted_frames)

print "Iteratively refining frames (this may take a while)..."
#tf_matrices = [tf_matrices[0]] + \
#              [register.refine(usedframes[0],F,M)
#               for F,M in zip(usedframes[1:],tf_matrices[1:])]

print "Reconstructing..."
scale = 1
for m in tf_matrices:
    m[:2,:] *= scale

#for u in usedframes:
#    u -= u.min()
out = register.stack.with_transform(usedframes, tf_matrices)

# Astronomy
#out = register.stack.with_transform(usedframes, tf_matrices, weights=N.ones(len(usedframes)))
#T = 400
#out[out > T] = T

interp = 'nearest'
#P.subplot(121)
#P.imshow(images[0],cmap=P.cm.gray,interpolation=interp)
#P.subplot(223)
#P.imshow(images[1],cmap=P.cm.gray,interpolation=interp)
#P.subplot(122)
P.imshow(out,cmap=P.cm.gray,interpolation=interp)
P.xticks([])
P.yticks([])
P.show()

S.misc.pilutil.imsave('/tmp/data.eps',out)
