"""Stack two transformed images."""

import numpy as np
import matplotlib.pyplot as plt

import os, sys
from math import sin, cos

import supreme
from supreme.config import data_path
from supreme import register
import supreme.io

if len(sys.argv) > 1:
    images = [supreme.io.imread(f) for f in sys.argv[1:]]
    tf_matrices = [np.eye(3) for n in range(len(images))]
else:
    images = ['NASA/hubble_crop.jpg','NASA/hubble_crop_rot5.jpg']
    images = [supreme.io.imread(os.path.join(data_path,fn), flatten=True)
              for fn in images]

    theta = 5/180.*np.pi
    tf_matrices = [np.array([[1,0,0],
                             [0,1,0],
                             [0,0,1]]),
                   np.array([[cos(theta),-sin(theta),0],
                             [sin(theta),cos(theta),0],
                             [0,0,1]])]

out = register.stack.with_transform(images, tf_matrices)
if out.ndim == 3 and out.shape[2] == 4:
    mask = out[..., 3]
    out = out[..., :3]
    out[mask == 0] = 0


plt.figure()
plt.imshow(out.astype(np.uint8))
plt.show()
plt.close()
