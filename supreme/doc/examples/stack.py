"""Stack two transformed images."""

from numpy.testing import set_local_path, restore_path
import numpy as N
import pylab as P
import scipy as S

import os
from math import sin,cos

set_local_path('../../..')
import supreme
from supreme.config import data_path
from supreme import register
restore_path()

images = ['NASA/hubble_crop.jpg','NASA/hubble_crop_rot5.jpg']
images = [supreme.imread(os.path.join(data_path,fn),flatten=True) for fn in images]

theta = 5/180.*N.pi
tf_matrices = [N.array([[1,0,0],
                        [0,1,0],
                        [0,0,1]]),
               N.array([[cos(theta),-sin(theta),0],
                        [sin(theta),cos(theta),0],
                        [0,0,1]])]

out = register.stack.with_transform(images,tf_matrices)

P.figure()
P.imshow(out)
P.show()
P.close()
