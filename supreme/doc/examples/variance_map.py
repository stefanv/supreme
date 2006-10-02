"""Demonstrate variance maps."""

import os.path

from numpy.testing import set_local_path, restore_path
import numpy as N
import pylab as P
import scipy as S

set_local_path('../../..')
import supreme
from supreme.config import data_path
from supreme.ext import variance_map
restore_path()

fn = 'toystory/toystory001.png'
x = supreme.imread(os.path.join(data_path,fn),flatten=True)

P.subplot(121)
P.imshow(x,cmap=P.cm.gray)
P.xlabel('Input image')
P.subplot(122)
vm = variance_map(x,shape=(20,20))
vm /= vm.max()
P.imshow(vm)
P.xlabel('Variance map')
P.show()
