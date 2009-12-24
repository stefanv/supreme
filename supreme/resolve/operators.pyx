"""Construct linear operators that represents the camera process.

Ax = b where A is the operator, x is the high-resolution image and b
is a stacked column of all low resolution images, unravelled in raster
scan (lexicographic) order.

"""

import scipy.sparse as sparse

import numpy as np
cimport numpy as np

cdef extern from "math.h":
    double floor(double)

cdef tf(int x, int y, M):
    cdef np.ndarray[np.double_t, ndim=2] H = M
    cdef double xx, yy, zz

    xx = H[0, 0] * x + H[0, 1] * y + H[0, 2]
    yy = H[1, 0] * x + H[1, 1] * y + H[1, 2]
    zz = H[2, 0] * x + H[2, 1] * y + H[2, 2]

    xx /= zz
    yy /= zz

    return xx, yy

cpdef bilinear(int MM, int NN, list HH, int M, int N):
    """Represent the camera process as a simple bilinear interpolation.

    Parameters
    ----------
    MM, NN : int
        Shape of the high-resolution image.
    HH : list of (3,3) ndarray
        Transformation matrices that warp the high-resolution frame
        to the individual low-resolution frames.
    M, N : int
        Dimensions of a single low-resolution output frame.

    """
    cdef int out_M, out_N

    out_M = len(HH) * M * N
    out_N = MM * NN

    cdef list I = [], J = [], V = []

    cdef np.ndarray[np.double_t, ndim=2] H

    cdef int i, j, p, q, xx, yy, R
    cdef double ii, jj, t, u

    for k in range(len(HH)):
        H = np.linalg.inv(HH[k])

        for i in range(M):
            for j in range(N):
                jj, ii = tf(j, i, H)

                xx = (int)(floor(jj))
                yy = (int)(floor(ii))

                if xx < 0 or yy < 0 or yy >= (MM - 1) or xx >= (NN - 1):
                    continue


                t = ii - yy
                u = jj - xx

                R = k*M*N + i * M + j

                I.extend([R, R, R, R])
                J.extend([yy*NN + xx,
                          (yy + 1)*NN + xx,
                          (yy + 1)*NN + xx + 1,
                          yy*NN + xx + 1])
                V.extend([(1 - t) * (1 - u),
                          t * (1 - u),
                          t * u,
                          (1 - t) * u])

    return sparse.coo_matrix((V, (I, J)), shape=(out_M, out_N)).tocsr()
