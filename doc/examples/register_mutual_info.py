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
else:
    A = chelsea(grey=True).astype(np.uint8)
    Ac = A
    t = 20/180. * np.pi
    x = 3
    y = 6
    B = homography(A, [[np.cos(t), -np.sin(t), x],
                       [np.sin(t),  np.cos(t), y],
                       [0,            0,       1]])
    Bc = B

M, S = register.dense_MI(A, B, levels=3)
print "Mutual information: ", S
if S < 1.5:
    print "Warning: registration probably failed."

print "Transformation matrix:"
print np.array2string(M, separator=', ')

X = register.stack.with_transform([Ac, Bc], [np.eye(3), M], save_tiff=True)

if len(sys.argv) != 3:
    import matplotlib.pyplot as plt
    plt.imshow(X)
    plt.show()
