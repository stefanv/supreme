"""Register two rotated images using the log polar transform."""

from __future__ import division

import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid import Grid, ImageGrid, make_axes_locatable

import os.path

import supreme.api as sr
from supreme.config import data_path, ftype

img1 = sr.io.imread(os.path.join(data_path,'NASA/hubble_crop.jpg'),flatten=True)

r = np.random.random() * np.pi / 2
s = 0.5 + np.random.random() * 2

M = np.array([[s*np.cos(r), -s*np.sin(r), 0],
              [s*np.sin(r),  s*np.cos(r), 0],
              [0,            0,           1]])
M_shift = np.array([[1, 0, -img1.shape[1]/2.],
                    [0, 1, -img1.shape[0]/2.],
                    [0, 0, 1]])

M_around_center = np.dot(np.linalg.inv(M_shift), np.dot(M, M_shift))

img2 = sr.transform.matrix(img1, M_around_center)
corr_peak, theta, scale = \
           sr.register.lp_patch_match(img1, img2, Rs=500, angles=360,
                                      plot_corr=True)
print "Estimation:   rotation of %.2f degrees and scaling of %s." % \
      ((theta / np.pi * 180) % 360, scale)
print "Ground truth: rotation of %.2f degrees and scaling of %s." % \
      (r / np.pi * 180, s)
print "Peak correlation was %.2f." % corr_peak

fig = plt.figure(0)

grid1 = Grid(fig, 211, nrows_ncols=(2, 2), share_x=False, share_y=False)

grid1[0].imshow(img1, cmap=plt.cm.gray)
grid1[0].set_title('Source image')

grid1[1].imshow(img2, cmap=plt.cm.gray)
grid1[1].set_title('Rotated $%.2f^\\circ$\nScaled $\\times %.2f$' % \
                   (r/np.pi * 180, s))

grid1[2].set_title('Log polar transform')
a = np.linspace(0, np.pi * 2, 180)
grid1[2].imshow(sr.transform.logpolar(img1, angles=a), cmap=plt.cm.gray)
grid1[3].imshow(sr.transform.logpolar(img2, angles=a), cmap=plt.cm.gray)

M1 = np.array([[scale*np.cos(theta), -scale*np.sin(theta), 0],
               [scale*np.sin(theta),  scale*np.cos(theta), 0],
               [0,                    0,                   1]])
# Rotate around the image centre
M1 = np.dot(np.linalg.inv(M_shift), np.dot(M1, M_shift))
M1_inv = np.linalg.inv(M1)

img_stack = sr.register.stack.with_transform(
                [img1, img2], [np.eye(3), M1_inv])

img_warp = sr.transform.matrix(img2, M1_inv)

img_patch = img1.copy()
mask = (img_warp != 0)
img_patch[mask] = img_warp[mask]

r, c = img_warp.shape
corners = np.array([[0, 0, 1],
                    [c, 0, 1],
                    [c, r, 1],
                    [0, r, 1],
                    [0, 0, 1]]).T

corners = np.dot(M1_inv, corners).T

grid3 = Grid(fig, 212, nrows_ncols=(1, 2), share_x=False, share_y=False)
grid3[0].imshow(img_warp)
grid3[1].imshow(img_patch)
plt.plot(corners[:, 0], corners[:, 1], 'r-', linewidth=3)
plt.axis("image")

plt.show()
