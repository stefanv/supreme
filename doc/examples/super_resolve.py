"""Construct super-resolution reconstruction of a registered data-set.

"""
SCALE = 2

from supreme.resolve import iresolve
from supreme.config import data_path
from supreme.io import load_vgg

import matplotlib.pyplot as plt

import sys, os

if len(sys.argv) > 1:
    vgg_dir = sys.argv[1]
else:
    vgg_dir = os.path.join(data_path, 'text_small')

ic = load_vgg(vgg_dir)

HH = [ic[i].info['H'] for i in range(5)]
images = [ic[i] for i in range(5)]
out = iresolve(images, HH, scale=SCALE)

plt.subplot(1, 2, 1)
plt.imshow(ic[0])

plt.subplot(1, 2, 2)
plt.imshow(out)

plt.show()
