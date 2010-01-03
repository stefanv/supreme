# -*- python -*-

"""Fast Parzen-Window-like estimator of the joint histogram between two
images.

"""
import numpy as np
cimport numpy as np
cimport cython

from supreme.geometry.window import gauss

cdef extern from "math.h":
    double logf(double)
    double round(double)

@cython.boundscheck(False)
cdef np.ndarray _add_window(np.ndarray out_arr, int m, int n,
                            np.ndarray win_arr):
    cdef np.ndarray[np.double_t, ndim=2] out = out_arr
    cdef np.ndarray[np.double_t, ndim=2] w = win_arr

    cdef int hwin = (win_arr.shape[0] - 1)/2
    cdef int i, j, ii, jj
    cdef int M, N
    M = out_arr.shape[0]
    N = out_arr.shape[1]

    for i in range(-hwin, hwin + 1):
        for j in range(-hwin, hwin + 1):
            ii = i + m
            jj = j + n

            if (ii < 0) or (ii >= M) or (jj < 0) or (jj >= N):
                continue

            out[ii, jj] += w[i + hwin, j + hwin]

    return out

@cython.boundscheck(False)
def joint_hist(np.ndarray[np.uint8_t, ndim=2] A,
               np.ndarray[np.uint8_t, ndim=2] B, L=255, win_size=5, std=1.0,
               int fast=0):
    """Estimate the joint histogram of A and B.

    Parameters
    ----------
    A, B : (M, N) ndarray of uint8
        Input images.
    L : int
        Number of grey-levels in histogram.
    win_size : int
        Width of Gaussian window used in the approximation.  A larger
        window can represent the Gaussian kernel somewhat more
        accurately.
    std : float
        Standard deviation of the Gaussian used in the Parzen estimation.
        The higher the standard deviation, the smoother the resulting
        histogram.  `win_size` must be made large enough to accommodate
        an increased standard deviation.
    fast : bool
        Calculate the classical histogram, instead of using a Parzen
        Window.  Fast, but does not estimate the PDF as accurately.

    Returns
    -------
    H : (256, 256) ndarray of float
        Estimation of the joint probability density function between A and B.

    """
    cdef np.ndarray[np.double_t, ndim=2] out

    if not (A.shape[0] == B.shape[0]) and (A.shape[1] == B.shape[1]):
        raise IndexError("Shapes of both input arrays must be equal.")

    # Approximation of Gaussian
    cdef np.ndarray[np.double_t, ndim=2] w

    if not fast:
        w = gauss(win_size, std)

    out = np.zeros((L, L), dtype=np.double)

    cdef int m, n, i, j, a, b
    m = A.shape[0]
    n = A.shape[1]

    for i in range(m):
        for j in range(n):
            a = A[i, j]
            b = B[i, j]

            if fast:
                out[(int)(round(a / 255. * (L - 1))),
                    (int)(round(b / 255. * (L - 1)))] += 1
            else:
                out = _add_window(out, a, b, w)

    # Normalisation not needed if the correct window is provided

    cdef double s = 0
    for i in range(255):
        for j in range(255):
            s += out[i, j]
    out /= s

    return out

@cython.boundscheck(False)
def mutual_info(np.ndarray[np.double_t, ndim=2] H):
    """Given the joint histogram of two images, calculate
    their mutual information.

    Parameters
    ----------
    H : (256, 256) ndarray of double

    Returns
    -------
    S : float
        Mutual information.

    """
    cdef int i, j
    cdef int M, N
    cdef double S
    cdef np.ndarray[np.double_t] hR, hC
    cdef double den

    M = H.shape[0]
    N = H.shape[1]

    hR = np.zeros(M, dtype=np.double)
    for i in range(M):
        for j in range(N):
            hR[i] += H[i, j]

    hC = np.zeros(N, dtype=np.double)
    for i in range(M):
        for j in range(N):
            hC[j] += H[i, j]

    S = 0
    for i in range(M):
        for j in range(N):
            if H[i, j] == 0 or hR[i] == 0 or hC[j] == 0:
                continue

            den = (hR[i] * hC[j])
            if den == 0:
                S += 100
                continue

            S += H[i, j] * logf(H[i, j] / den) / logf(2)

##     d = (H.sum(axis=0) * H.sum(axis=1).reshape(H.shape[0], -1))
##     mask = ((H != 0) & (d != 0))
##     h = H.copy()
##     h[mask] /= d[mask]
##     S = -np.sum(H[mask] * np.log(h[mask])) / np.log(2)

    return S
