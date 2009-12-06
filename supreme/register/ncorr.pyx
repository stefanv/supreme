__all__ = ['ncc']

# cython: cdivision(True)

import numpy as np
cimport cython
cimport numpy as np

cdef imin(int a, int b):
    if a < b:
        return a
    else:
        return b

cdef imax(int a, int b):
    if a > b:
        return a
    else:
        return b

cdef coord_wrap(int i, int j, int rows, int cols):
    return i % rows, j % cols

@cython.boundscheck(False)
cpdef ncc(np.ndarray imgS, np.ndarray imgT):
    """Circular normalised cross-correlation of source and
    template image.

    Parameters
    ----------
    imgS : ndarray of uint8
        Source image.
    imgT : ndarray of uint8
        Template image.  The dimensions of the template image must be
        smaller or equal to that of the source.

    Returns
    -------
    ncc : ndarray of float
        Normalised correlation coefficients, of the same shape as the
        source image.

    References
    ----------
    .. [1] J.P. Lewis, Fast Normalized Cross-Correlation, 1995,
           http://www.idiom.com/~zilla/.
    .. [2] D. Tsai and C. Lin, "Fast normalized cross correlation for
           defect detection," Pattern Recognition Letters, vol. 24, 2003.

    """
    cdef np.ndarray[np.uint8_t, ndim=2] S = imgS
    cdef np.ndarray[np.uint8_t, ndim=2] T = imgT
    cdef np.ndarray[np.double_t, ndim=2] out
    cdef int s_rows, s_cols, t_rows, t_cols, ta
    cdef double var_S, var_T, u_S, u_T, var_norm
    cdef np.uint8_t xS, xT

    s_rows = S.shape[0]
    s_cols = S.shape[1]
    t_rows = T.shape[0]
    t_cols = T.shape[1]
    ta = t_rows * t_cols # template area

    cdef int i, j, m, n
    cdef int row_start_S, row_end_S, col_start_S, col_end_S, \
             row_start_T, row_end_T, col_start_T, col_end_T, \
             row_range, col_range

    cdef double val

    # S is standing still
    # Moving T over S

    out = np.zeros((s_rows, s_cols), dtype=np.double)

    # Calculate template mean and variance
    var_T = 0
    u_T = 0
    for m in range(t_rows):
        for n in range(t_cols):
            u_T += T[m, n]
            var_T += T[m, n] ** 2

    u_T /= ta
    var_T /= ta

    # E[(X - mu)^2] = E[X^2] - mu^2
    var_T -= u_T ** 2

    for i in range(s_rows):
        for j in range(s_cols):
            u_S = 0
            var_S = 0

            for m in range(t_rows):
                for n in range(t_cols):
                    sm, sn = coord_wrap(i + m, j + n, s_rows, s_cols)
                    u_S += S[sm, sn]
                    var_S += S[sm, sn] ** 2

            u_S /= ta
            var_S /= ta
            var_S -= u_S ** 2

            val = 0
            for m in range(t_rows):
                for n in range(t_cols):
                    sm, sn = coord_wrap(i + m, j + n, s_rows, s_cols)

                    xS = S[sm, sn]
                    xT = T[m, n]

                    val += (xS - u_S) * (xT - u_T)

            # Divide by standard deviation of each
            var_norm = ta * (var_S * var_T) ** 0.5
            if var_norm > 0:
                out[i, j] = val / var_norm
            else:
                out[i, j] = 0

    return out
