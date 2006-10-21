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
restore_path()

images = [supreme.imread(fn,flatten=True) for fn in glob.glob(os.path.join(data_path,'toystory/*.png'))]
#images = [supreme.imread(fn,flatten=True) for fn in glob.glob(os.path.join(data_path,'test/flower*.jpg'))]

frames = images[:5]
accepted_frames,tf_matrices = register.logpolar(frames[0],frames[1:])
tf_matrices = [N.eye(3)] + tf_matrices
usedframes = [frames[0]] + [frames[i+1] for i in accepted_frames]

print "Refining frames (this may take a while)..."
tf_matrices = [tf_matrices[0]] + \
              [register.refine(usedframes[0],F,M)
               for F,M in zip(usedframes[1:],tf_matrices[1:])]

print "Reconstructing..."

for m in tf_matrices:
    print m
    print

out = register.stack.with_transform(usedframes, tf_matrices)

P.imshow(out,cmap=P.cm.gray)
P.show()

