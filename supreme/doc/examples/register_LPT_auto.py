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

frames = images[:13]
tf_matrices = register.logpolar(frames[0],frames[1:])
tf_matrices = [N.eye(3)] + tf_matrices

print "Reconstructing..."
out = register.stack.with_transform(frames,tf_matrices)

P.imshow(out,cmap=P.cm.gray)
P.show()

