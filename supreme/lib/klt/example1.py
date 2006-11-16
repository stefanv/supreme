import numpy as N

from numpy.testing import set_local_path, restore_path
set_local_path('../../..')
from supreme.lib import klt
restore_path()

import scipy as S
imread = S.misc.pilutil.imread

img1 = imread('img0.pgm')
img2 = imread('img1.pgm')

tc = klt.TrackingContext()
print tc

fl = klt.FeatureList(100)
klt.select_good_features(tc, img1, fl)

print '\nIn first image:'
print fl
