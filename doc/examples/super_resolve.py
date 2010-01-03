"""Construct super-resolution reconstruction of a registered data-set.

"""
SCALE = 4.
UPDATE = 1 # if False, do a single pass calculation instead of
           # adding one frame at a time
DAMP = 1e-2
PHOTOMETRIC_ADJUSTMENT = True
METHOD = 'LSQR' # 'CG' or 'LSQR' or 'descent'
OPERATOR = 'polygon' # 'polygon' # bilinear or polygon

import numpy as np

from supreme.resolve import solve, initial_guess_avg
from supreme.config import data_path
from supreme.io import load_vgg
from supreme.transform import homography
from supreme.noise import dwt_denoise

import matplotlib.pyplot as plt

import sys, os

if len(sys.argv) > 1:
    vgg_dir = sys.argv[1]
else:
    vgg_dir = os.path.join(data_path, 'vgg/library_very_small')

ic = load_vgg(vgg_dir)

# Perform crude photometric registration
ref = ic[0].copy()
images = []
scales = []
for i in range(len(ic)):
    scale = 1

    if PHOTOMETRIC_ADJUSTMENT:
        img = ic[i]
        img_warp = homography(ic[i], ic[i].info['H'])
        mask = (img_warp > 20) & (img_warp < 220) & \
               (ref > 20) & (ref < 220)
        scale = np.mean(ref[mask].astype(float) / img_warp[mask])

    scales.append(scale)
    images.append(ic[i] * scale)

print "Images scaled by: %s" % str(['%.2f' % f for f in scales])

HH = [i.info['H'] for i in images]
oshape = np.floor(np.array(images[0].shape) * SCALE)
avg = initial_guess_avg(images, HH, SCALE, oshape)

#
# Solve by adding one frame at a time
#

if UPDATE:
    #
    # Update solution one frame at a time
    #
    out = avg.copy()
    for j in range(1):
        print "SR iteration %d" % j
        for i in range(len(images)):
            print "Resolving frame %d" % i
            out = solve([images[i]], [HH[i]], scale=SCALE, tol=0,
                        x0=out, damp=DAMP, iter_lim=200,
                        method=METHOD, operator=OPERATOR)

else:
    #
    # Solve all at once
    #
    out = avg.copy()
    out = solve(images, HH, scale=SCALE, tol=0,
                x0=out, damp=DAMP, iter_lim=200,
                method=METHOD)

import scipy.misc
scipy.misc.imsave('/tmp/avg.png', avg)
scipy.misc.imsave('/tmp/out.png', out)

plt.subplot(3, 1, 1)
plt.imshow(ic[0], interpolation='nearest', cmap=plt.cm.gray)

plt.subplot(3, 1, 2)
plt.imshow(avg, interpolation='lanczos', cmap=plt.cm.gray)

plt.subplot(3, 1, 3)
plt.imshow(out, interpolation='lanczos', cmap=plt.cm.gray)

plt.show()
