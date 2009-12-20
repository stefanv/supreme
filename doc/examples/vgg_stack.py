"""Load a VGG data-set and stack the images.

"""

import numpy as np

from supreme.io import load_vgg
from supreme.config import data_path
from supreme.register import stack

import matplotlib.pyplot as plt
from scipy.misc import imsave

import os, sys

scale = 1.5

if len(sys.argv) > 1:
    vgg_dir = sys.argv[1]
else:
    vgg_dir = os.path.join(data_path, 'vgg/sr_sequences/text')

ic = load_vgg(vgg_dir)

HH = [img.info['H'] for img in ic]
for H in HH:
    H[:2, :] *= scale
S = stack.with_transform(ic, HH, order=2)

imsave('vgg_stack.png', S)

plt.imshow(S, cmap=plt.cm.gray)
plt.show()
