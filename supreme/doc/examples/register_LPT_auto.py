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

images = [supreme.imread(fn,flatten=True) for fn in glob.glob(os.path.join(data_path,'toystory/*.png'))]
#images = [supreme.imread(fn,flatten=True) for fn in glob.glob(os.path.join(data_path,'test/flower*.jpg'))]
#images = [supreme.imread(fn,flatten=True) for fn in glob.glob(os.path.join(data_path,'test/olie*.jpg'))]
images = [supreme.imread(fn,flatten=True) for fn in glob.glob(os.path.join(data_path,'chris/*.jpg'))]

# frames that work well: 1,2,(4),(8),(9),11,
#frames = [images[i] for i in [0,1,2,11]] # don't say a word, it's late
frames = images
accepted_frames,tf_matrices = register.logpolar(frames[0],frames[1:],window_shape=(31,31))
tf_matrices = [N.eye(3)] + tf_matrices
usedframes = [frames[0]] + [frames[i+1] for i in accepted_frames]



print "Iteratively refining frames (this may take a while)..."
#tf_matrices = [tf_matrices[0]] + \
#              [register.refine(usedframes[0],F,M)
#               for F,M in zip(usedframes[1:],tf_matrices[1:])]

print "Reconstructing..."

for m in tf_matrices:
    print m

out = register.stack.with_transform(usedframes, tf_matrices)

interp = 'lanczos'
P.subplot(121)
P.imshow(images[0],cmap=P.cm.gray,interpolation=interp)
#P.subplot(223)
#P.imshow(images[1],cmap=P.cm.gray,interpolation=interp)
P.subplot(122)
P.imshow(out,vmin=0,vmax=255,cmap=P.cm.gray,interpolation=interp)
P.show()
