# -*- python -*-

# cython: cdivide=True

import numpy as np
cimport numpy as np
cimport cython

cdef extern from "math.h":
    double atanf(double)
    int round(double)

@cython.boundscheck(False)
def radial_sum(np.ndarray[np.double_t, ndim=2] patch):
    """Sum the elements of an array outward along 360 directions
    (1-degree increments).

    Parameters
    ----------
    img : (M,N) ndarray of double
        Input image.

    Returns
    -------
    R : (360,) ndarray of double
        Summed elements of `img` along each of 360 directions.  The central
        element, which belongs to all directions, is discarded.

    Examples
    --------
    >>> x = np.array([[2, 0, 1],
    ...               [0, 5, 0],
    ...               [3, 0, 4]], dtype=np.double)
    >>> R = radial_sum(x)
    >>> R[[45, 135, 225, 315]] == [1, 2, 3, 4]

    """
    cdef np.ndarray[np.double_t, ndim=1] out = np.zeros((360,), dtype=np.double)
    cdef int i, j, M, N, ii, jj
    cdef double angle

    M = patch.shape[0]
    N = patch.shape[1]

    for i in range(M):
        for j in range(N):
            ii = i - (M - 1)/2
            jj = j - (N - 1)/2

            # Ignore middle pixel
            if ii == 0 and jj == 0:
                continue

            # Use -1 to mask transparency
            if patch[i, j] == -1:
                continue

            if jj == 0 and ii > 0:
                out[90] += patch[i, j]
            elif jj == 0 and ii < 0:
                out[270] += patch[i, j]
            else:
                angle = -atanf(ii / float(jj)) / np.pi * 180
                if jj < 0:
                    angle += 180
                out[round(angle % 360)] += patch[i, j]

    return out
