import numpy as np
from numpy.testing import *

import scipy.ndimage as ndi
import scipy.linalg
import scipy.sparse as sparse

from supreme.geometry.window import gauss
from supreme.resolve.operators import bilinear, convolve, block_diag
from supreme.io import imread

import os

HR = imread(os.path.join(os.path.dirname(__file__), 'peppers_40.png'),
            flatten=True)

def test_bilinear():
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

def test_convolve():
    w = np.array([[0, 1, 0],
                  [1, 2, 1],
                  [0, 1, 0]]) / 6.
    A = convolve(40, 40, w)

    p = np.prod(HR.shape)
    c1 = (A * HR.flat).reshape(HR.shape)
    c2 = ndi.convolve(HR, w)

    assert np.linalg.norm(c1 - c2) / np.prod(HR.shape) < 0.5

def test_block_diag():
    X = np.array([[1, 2, 3],
                  [4, 5, 6]])
    Y = scipy.linalg.block_diag(X, X, X)
    bd = block_diag(X.shape[0], X.shape[1],
                    X.shape[0] * 3, X.shape[1] * 3)
    assert_array_equal((bd * X.flat).reshape(np.array(X.shape) * 3), Y)

if __name__ == "__main__":
    scale = 3

    theta = 5 / 180. * np.pi
    C = np.cos(theta)
    S = np.sin(theta)
    tx, ty = 0, 0

    A = bilinear(HR.shape[0], HR.shape[1],
                 [np.array([[C/scale, -S,        tx],
                            [S,        C/scale,  ty],
                            [0,        0,        1.]])],
                  HR.shape[0] / scale, HR.shape[1] / scale)


    C = convolve(HR.shape[0], HR.shape[1], gauss(5, std=1))

    import matplotlib.pyplot as plt
    plt.spy((A * C).todense())

    plt.figure()
    fwd = (A * C * HR.flat)
    rev = C.T * A.T * fwd

    plt.subplot(1, 3, 1)
    plt.imshow(HR, cmap=plt.cm.gray, interpolation='nearest')

    plt.subplot(1, 3, 2)
    plt.imshow(fwd.reshape(np.array(HR.shape) / scale),
               interpolation='nearest', cmap=plt.cm.gray)
    plt.subplot(1, 3, 3)
    plt.imshow(rev.reshape(HR.shape),
               interpolation='nearest', cmap=plt.cm.gray)
    plt.show()
