# -*- python -*-

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
    double exp(double)
    double round(double)

cdef tf(double x, double y, M):
    cdef np.ndarray[np.double_t, ndim=2] H = M
    cdef double xx, yy, zz

    xx = H[0, 0] * x + H[0, 1] * y + H[0, 2]
    yy = H[1, 0] * x + H[1, 1] * y + H[1, 2]
    zz = H[2, 0] * x + H[2, 1] * y + H[2, 2]

    xx /= zz
    yy /= zz

    return xx, yy

cpdef bilinear(int MM, int NN, list HH, int M, int N,
               int boundary=0):
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
    boundary : {0, 1}
        Outside boundary use zero (0) or mirror (1).

    Returns
    -------
    A : (len(HH) * M * N, MM * NN) ndarray
        Linear-operator representing bilinear interpolation from
        the HR image to the different LR images.

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

                if boundary == 1:
                    yy = (yy % (MM - 1))
                    xx = (xx % (NN - 1))
                elif xx < 0 or yy < 0 or yy >= (MM - 1) or xx >= (NN - 1):
                    continue

                t = ii - yy
                u = jj - xx

                R = k*M*N + i * N + j

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

cpdef convolve(int M, int N, np.ndarray mask_arr):
    """A linear operator that represents a convolution operation.

    Parameters
    ----------
    M, N : int
        Shape of the output image.
    mask_arr : (K,K) ndarray where K is odd
        Mask to convolve with.

    Returns
    -------
    A : (M*N, M*N) sparse array
        Linear operator that performs a convolution.

    """
    cdef np.ndarray[np.double_t, ndim=2] mask = mask_arr.astype(np.double)
    cdef int m, n, mm, nn, i, j, hwin
    cdef list I = [], J = [], V = []

    hwin = (mask.shape[0] - 1) / 2

    for m in range(M):
        for n in range(N):
            for i in range(-hwin, hwin + 1):
                for j in range(-hwin, hwin + 1):
                    mm = m + i
                    nn = n + j

                    if mm < 0 or mm >= M or nn < 0 or nn >= N:
                        continue

                    I.append(m * N + n)
                    J.append(mm * N + nn)
                    V.append(mask[i + hwin, j + hwin])

    return sparse.coo_matrix((V, (I, J)), shape=(M*N, M*N)).tocsr()

cpdef block_diag(int M, int N, int MM, int NN):
    """Linear operator that represents diagonal block stacking.

    Repeats an (M, N) matrix diagonally to fit into
    and (MM, NN)-shaped matrix.

    """
    cdef int m, n, p, P
    cdef list I = [], J = [], V = []

    P = min(MM / M, NN / N)

    for p in range(P):
        for m in range(M):
            for n in range(N):
                I.append((p * M + m) * NN + p * N + n)
                J.append(m*N + n)
                V.append(1)

    return sparse.coo_matrix((V, (I, J)), shape=(MM*NN, M*N)).tocsr()

def op_repeat(op, N):
    """Apply the given operator to N identically sized images.

    """
    D = sparse.dia_matrix((np.ones(N), 0), shape=(N, N))
    return sparse.kron(D, op)
