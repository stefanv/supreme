"""Construct super-resolution reconstruction of a registered data-set.

"""
SCALE = 3
std = None # Auto-detect
#std = 1.19 #1.19121431622 # text
std = 1.25156 # text
#std = 1.23123012741 # library

import numpy as np
import scipy.optimize as opt

from supreme.resolve import solve, initial_guess_avg
from supreme.config import data_path
from supreme.io import load_vgg
from supreme.transform import homography
from supreme.resolve.operators import convolve

import matplotlib.pyplot as plt

import sys, os

if len(sys.argv) > 1:
    vgg_dir = sys.argv[1]
else:
    vgg_dir = os.path.join(data_path, 'text_small')

ic = load_vgg(vgg_dir)

images = []

# Perform crude photometric registration
ref = ic[0].copy()
for i in range(len(ic)):
    img_warp = homography(ic[i], ic[i].info['H'])
    mask = (img_warp != 0) & (ref != 0)
    scale = np.mean(ref[mask].astype(float) / img_warp[mask])

    images.append(ic[i] * scale)

HH = [i.info['H'] for i in images]
oshape = np.floor(np.array(images[0].shape) * SCALE)
avg = initial_guess_avg(images, HH, SCALE, oshape)


# Automatically determine best standard deviation parameter
C = convolve(oshape[0], oshape[1], np.array([[-1, -1, -1],
                                             [-1,  8, -1],
                                             [-1, -1, -1]]))

def std_func(std):
    out = solve(images, HH, scale=SCALE, tol=0, std=std,
                x0=avg, damp=0, iter_lim=5, lam=0, fast=True)
    out = C * out.flat
    return np.var(out)

if not std:
    print "Searching for optimal camera variance..."
    std = opt.fminbound(std_func, 1.05, 3)
    print "Std estimated to be:", std

#
# Solve by adding one frame at a time
#
out = avg.copy()
## for j in range(1):
##     print "SR iteration %d" % j
##     for i in range(len(images)):
##         print "Resolving frame %d" % i
##         out = solve([images[i]], [HH[i]], scale=SCALE, tol=0, std=std,
##                     x0=out, damp=6, iter_lim=10, lam=500)

#
# Solve all at once
#
out = solve(images, HH, scale=SCALE, tol=0, std=std,
            x0=out, damp=6, iter_lim=40, lam=1200)


import scipy.misc
scipy.misc.imsave('/tmp/avg.png', avg)
scipy.misc.imsave('/tmp/out.png', out)

out = out[20:-10, 10:-15]
avg = avg[20:-10, 10:-15]

plt.subplot(3, 1, 1)
plt.imshow(ic[0], interpolation='nearest', cmap=plt.cm.gray)

plt.subplot(3, 1, 2)
plt.imshow(avg, interpolation='lanczos', cmap=plt.cm.gray)

plt.subplot(3, 1, 3)
plt.imshow(out, interpolation='lanczos', cmap=plt.cm.gray)

plt.show()
