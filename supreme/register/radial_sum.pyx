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
