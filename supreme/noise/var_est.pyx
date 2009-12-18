# -*- python -*-

"""Calculate variance over a shifting window.

"""

# cython: cdivision(True)

__all__ = ['variance']

import numpy as np
cimport numpy as np

def variance(np.ndarray[np.double_t, ndim=2] X, int win_size):
    cdef int i, j, rows, cols, hwin, p, q, ii, jj
    cdef double N, SS, S, mu

    rows = X.shape[0]
    cols = X.shape[1]

    cdef np.ndarray[np.double_t, ndim=2] out = \
         np.zeros((rows, cols), dtype=np.double)

    if win_size % 2 != 1:
        raise ValueError("Window size must be uneven")

    hwin = (win_size - 1) / 2

    # http://en.wikipedia.org/wiki/Algorithms_for_calculating_variance
    for i in range(rows):
        for j in range(cols):
            # Could also consider compensation summation / Kahan summation
            # http://en.wikipedia.org/wiki/Compensated_summation
            # to reduce cancellation error

            # First pass
            N = 0
            S = 0
            for p in range(-hwin, hwin + 1):
                for q in range(-hwin, hwin + 1):
                    ii = i + p
                    jj = j + q

                    if ii < 0 or jj < 0 or ii >= rows or jj >= cols:
                        continue


                    N += 1
                    S += X[ii, jj]

            mu = S / N

            # Second pass
            SS = 0
            for p in range(-hwin, hwin + 1):
                for q in range(-hwin, hwin + 1):
                    ii = i + p
                    jj = j + q

                    if ii < 0 or jj < 0 or ii >= rows or jj >= cols:
                        continue

                    SS += (X[ii, jj] - mu) ** 2

            out[i, j] = SS / N

    return out
