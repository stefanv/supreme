import numpy as np
import scipy.optimize
import scipy.ndimage

from demo_data import chelsea
from supreme.register.parzen import joint_hist, mutual_info
from supreme.transform import homography
import supreme.register as register

import sys
if len(sys.argv) == 3:
    from supreme.io import imread
    A = imread(sys.argv[1], flatten=True).astype(np.uint8)
    Ac = imread(sys.argv[1], flatten=False).astype(np.uint8)
    B = imread(sys.argv[2], flatten=True).astype(np.uint8)
    Bc = imread(sys.argv[2], flatten=False).astype(np.uint8)


A = chelsea(grey=True).astype(np.uint8)
t = 20/180. * np.pi
x = 3
y = 6
B = homography(A, [[np.cos(t), -np.sin(t), x],
                   [np.sin(t),  np.cos(t), y],
                   [0,            0,       1]])

def _build_tf(p):
    if np.sum(np.isnan(p) + np.isinf(p)) != 0:
        return np.eye(3)
    else:
        theta,a,b,tx,ty = p
        C = np.cos(theta)
        S = np.sin(theta)
        return np.array([[a*C, -b*S, tx],
                         [a*S,  b*C, ty],
                         [0,    0,   1.]])

def cost(p, A, B):
    T = homography(B, _build_tf(p), order=2)
    S = mutual_info(joint_hist(A, T, win_size=5, std=1))
    return S

p = [0, 1, 1, 0, 0],
for z in range(3, -1, -1):
    print "Downsampling by", 2**z
    A_ = scipy.ndimage.zoom(A, 1/2.**z)
    B_ = scipy.ndimage.zoom(B, 1/2.**z)
    p = scipy.optimize.fmin_powell(cost, p, args=(A_, B_))

M = _build_tf(p)
print "Transformation matrix:"
print np.array2string(M, separator=', ')

X = register.stack.with_transform([Ac, Bc], [np.eye(3), M], save_tiff=True)

if len(sys.argv) != 3:
    import matplotlib.pyplot as plt
    plt.imshow(X)
    plt.show()
