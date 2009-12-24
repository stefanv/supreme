import numpy as np
from numpy.testing import *

import scipy.ndimage as ndi

from supreme.resolve.operators import bilinear
from supreme.io import imread

import os

HR = imread(os.path.join(os.path.dirname(__file__), 'peppers_40.png'),
            flatten=True)

def test_basic():
    H = np.array([[1/2., 0,    0],
                  [0,    1/2., 0],
                  [0,    0,    1]])
    A = bilinear(HR.shape[0], HR.shape[1],
                 [H, H],
                 HR.shape[0] / 2, HR.shape[1]/2)

    p = np.prod(HR.shape)
    assert_equal(A.shape, (2 * p/4, np.prod(HR.shape)))

    HR_small = (A[p/4:, :] * HR.flat).reshape(np.array(HR.shape) / 2)
    err_norm = np.linalg.norm(ndi.zoom(HR, 0.5) - HR_small)
    err_norm /= np.prod(HR_small.shape)

    assert err_norm < 2


if __name__ == "__main__":
    scale = 2

    theta = 5 / 180. * np.pi
    C = np.cos(theta)
    S = np.sin(theta)
    tx, ty = 0, 0

    A = bilinear(HR.shape[0], HR.shape[1],
                 [np.array([[C/scale, -S,        tx],
                            [S,        C/scale,  ty],
                            [0,        0,        1.]])],
                  HR.shape[0] / scale, HR.shape[1] / scale)

    import matplotlib.pyplot as plt
    plt.spy(A.todense())

    plt.figure()
    fwd = (A * HR.flat)
    rev = A.T * fwd

    plt.subplot(1, 2, 1)
    plt.imshow(fwd.reshape(np.array(HR.shape) / scale),
               interpolation='nearest', cmap=plt.cm.gray)
    plt.subplot(1, 2, 2)
    plt.imshow(rev.reshape(HR.shape),
               interpolation='nearest', cmap=plt.cm.gray)
    plt.show()
