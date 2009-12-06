"""Register two rotated images using the log polar transform."""

from __future__ import division

import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid import Grid, ImageGrid, make_axes_locatable
from mpl_toolkits.mplot3d import axes3d

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

angles = np.linspace(0, np.pi * 2, 360)
Rs = 500
img1_tf, angles, log_base = \
         sr.transform.logpolar(img1, angles=angles, Rs=Rs, extra_info=True)

img2_tf = sr.transform.logpolar(img2, angles=angles, Rs=Rs)

cv = sr.register.phase_corr(img2_tf, img1_tf)
m, n = np.unravel_index(np.argmax(cv), cv.shape)

if n > Rs/2:
    n = n - Rs # correlation matched, but from the other side

theta = angles[m]
scale = np.exp(n * log_base)
print "Estimation:   rotation of %.2f degrees and scaling of %s." % \
      ((theta / np.pi * 180) % 360, scale)
print "Ground truth: rotation of %.2f degrees and scaling of %s." % \
      (r / np.pi * 180, s)
print "Peak correlation was %.2f." % cv[m, n]

fig = plt.figure(0)

grid1 = Grid(fig, 211, nrows_ncols=(2, 2), share_x=False, share_y=False)

grid1[0].imshow(img1, cmap=plt.cm.gray)
grid1[0].set_title('Source image')

grid1[1].imshow(img2, cmap=plt.cm.gray)
grid1[1].set_title('Rotated $%.2f^\\circ$\nScaled $\\times %.2f$' % \
                   (r/np.pi * 180, s))

grid1[2].set_title('Log polar transform')
grid1[2].imshow(img1_tf, cmap=plt.cm.gray)
grid1[3].imshow(img2_tf, cmap=plt.cm.gray)

fig = plt.figure(1)

cv_cut = cv[max(0, m - 30):min(cv.shape[1], m + 30),
            max(0, n - 30):min(cv.shape[0], n + 30)]

coords = sr.geometry.Grid(*cv_cut.shape)

ax3d = axes3d.Axes3D(fig)
ax3d.plot_wireframe(coords['cols'], coords['rows'], cv_cut)
ax3d.set_title('Phase correlation around peak\n$\\log(100 + x)$')
fig = plt.figure(0)

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
