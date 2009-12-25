"""Construct super-resolution reconstruction of a registered data-set.

"""
SCALE = 2

import numpy as np

from supreme.resolve import solve, initial_guess_avg
from supreme.config import data_path
from supreme.io import load_vgg
from supreme.transform import homography

import matplotlib.pyplot as plt

import sys, os

if len(sys.argv) > 1:
    vgg_dir = sys.argv[1]
else:
    vgg_dir = os.path.join(data_path, 'text_small')

ic = load_vgg(vgg_dir)

images = []
# Perform photometric registration
ref = ic[0].copy()
for i in range(len(ic)):
    img_warp = homography(ic[i], ic[i].info['H'])
    mask = (img_warp != 0) & (ref != 0)
    scale = np.mean(ref[mask].astype(float) / img_warp[mask])

    images.append(ic[i] * scale)

##HH = [ic[i].info['H'] for i in range(10)]
#images = [ic[i] for i in range(10)]
HH = [i.info['H'] for i in ic]
oshape = np.floor(np.array(images[0].shape) * SCALE)
avg = initial_guess_avg(images, HH, SCALE, oshape)

out = solve(images, HH, scale=SCALE, tol=0, std=1.1,
            x0=avg, damp=2, iter_lim=300)

#out = np.clip(out, 0, 255)
#out = iresolve(images, HH, scale=SCALE,
#               cost_measure=cost_prior_xsq,
#               cost_args={'lam': 0.3})

plt.subplot(3, 1, 1)
plt.imshow(ic[0], interpolation='nearest', cmap=plt.cm.gray)

plt.subplot(3, 1, 2)
plt.imshow(avg, interpolation='nearest', cmap=plt.cm.gray)

plt.subplot(3, 1, 3)
plt.imshow(out, interpolation='nearest', cmap=plt.cm.gray)

plt.show()
