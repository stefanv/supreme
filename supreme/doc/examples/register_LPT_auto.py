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

print register.logpolar(images[0],images[1:])
