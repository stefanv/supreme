# -*- python -*-

import numpy as np
cimport numpy as np
import scipy.sparse as sparse

cdef extern from "math.h":
    double floor(double)
    double round(double)

cdef extern from "polygon.h":
    int poly_clip(int N, double* x, double* y,
                  double xleft, double xright, double ytop, double ybottom,
                  double* workx, double* worky)
    double area(int N, double* px, double* py)

cdef tf(double x, double y, np.ndarray M):
    cdef np.ndarray[np.double_t, ndim=2] H = M
    cdef double xx, yy, zz

    xx = H[0, 0] * x + H[0, 1] * y + H[0, 2]
    yy = H[1, 0] * x + H[1, 1] * y + H[1, 2]
    zz = H[2, 0] * x + H[2, 1] * y + H[2, 2]

    xx /= zz
    yy /= zz

    return xx, yy

cdef tf_polygon(int N, double* xp, double* yp, np.ndarray H_arr):
    cdef int i
    for i in range(N):
        xp[i], yp[i] = tf(xp[i], yp[i], H_arr)

def poly_interp_op(int MM, int NN, np.ndarray[np.double_t, ndim=2] H,
                   int M, int N, search_win=7):
    """
    Construct a linear interpolation operator based on polygon overlap.

    Parameters
    ----------
    MM, NN : int
        Shape of the high-resolution source frame.
    M, N : int
        Shape of the low-resolution target frame.
    H : (3, 3) ndarray
        Transformation matrix that warps the high-resolution image to
        the low-resolution image.

    Returns
    -------
    op : (M*N, MM*NN) sparse array
        Interpolation operator.

    """
    cdef double rx[5]
    cdef double ry[5]
    cdef double xleft, xright, ytop, ybottom
    cdef double a, S
    cdef double workx[9], worky[9]

    cdef list I = [], J = [], V = []

    cdef int m, n, wr, wc
    cdef int K, k, verts, hwin

    cdef int out_M = M * N
    cdef int out_N = MM * NN

    cdef np.ndarray[np.double_t, ndim=2] inv_tf_M = np.linalg.inv(H)

    cdef double mt, nt, ridx, cidx

    # For each element in the low-resolution source
    for m in range(M):
        for n in range(N):
            # Create pixel polygon
            xleft = n - 0.5
            xright = xleft + 1
            ybottom = m - 0.5
            ytop = ybottom + 1

            # Find position in high-resolution frame
            nt, mt = tf(n, m, inv_tf_M)
            nt = round(nt)
            mt = round(mt)

            # For 25 pixels in target vicinity
            K = 0
            hwin = (search_win - 1)/2
            for wr in range(-hwin, hwin):
                for wc in range(-hwin, hwin):
                    rx[0] = nt + wc - 0.5
                    rx[1] = rx[0] + 1
                    rx[2] = rx[1]
                    rx[3] = rx[0]
                    rx[4] = rx[0]

                    ry[0] = mt + wr - 0.5
                    ry[1] = ry[0]
                    ry[2] = ry[0] + 1
                    ry[3] = ry[2]
                    ry[4] = ry[0]

                    ridx = round(mt + wr - 0.5)
                    cidx = round(nt + wc - 0.5)

                    if ridx < 0 or ridx > (MM - 1) or \
                       cidx < 0 or cidx > (NN - 1):
                        continue

                    # Project back to LR frame
                    tf_polygon(5, rx, ry, H)

                    verts = poly_clip(5, rx, ry,
                                      xleft, xright, ytop, ybottom,
                                      workx, worky)
                    a = area(verts, workx, worky)

                    I.append(m*N + n)
                    J.append((int)(ridx * NN + cidx))
                    V.append(a)

                    K += 1

            S = 0
            for k in range(K):
                S += V[-k]

            for k in range(K):
                if S > 1e-6:
                    V[-k] /= S

    return sparse.coo_matrix((V, (I, J)), shape=(out_M, out_N)).tocsr()
