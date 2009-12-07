__all__ = ['ncc', 'sat', 'sat_sum', 'window_wrap']

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

cpdef np.ndarray sat(np.ndarray X):
    """Summed area table / integral image.

    The integral image contains the sum of all elements above and to the
    left of it, i.e.:

    .. math::

       S[m, n] = \sum_{i \leq m} \sum_{j \leq n} X[i, j]

    Parameters
    ----------
    X : ndarray of uint8
        Input image.

    Returns
    -------
    S : ndarray
        Summed area table.

    References
    ----------
    .. [1] F.C. Crow, "Summed-area tables for texture mapping,"
           ACM SIGGRAPH Computer Graphics, vol. 18, 1984, pp. 207-212.

    """
    cdef int s_rows, s_cols
    s_rows = X.shape[0]
    s_cols = X.shape[1]

    cdef np.ndarray[np.uint64_t, ndim=2] S = np.zeros((s_rows, s_cols),
                                                      dtype=np.uint64)

    # First column
    S[0, 0] = X[0, 0]
    for m in range(1, s_rows):
        S[m, 0] = X[m, 0] + S[m - 1, 0]

    # First row
    for n in range(1, s_cols):
        S[0, n] = X[0, n] + S[0, n - 1]

    for m in range(1, s_rows):
        for n in range(1, s_cols):
                S[m, n] = S[m - 1, n] + S[m, n - 1] \
                              - S[m - 1, n - 1] + X[m, n]

    return S

cpdef np.uint64_t sat_sum(np.ndarray sat, int r0, int c0, int r1, int c1):
    """Using a summed area table / integral image, calculate the sum
    over a given window.

    Parameters
    ----------
    sat : ndarray of uint64
        Summed area table / integral image.
    r0, c0 : int
        Top-left corner of block to be summed.
    r1, c1 : int
        Bottom-right corner of block to be summed.

    Returns
    -------
    S : int
        Sum over the given window.

    """
    cdef np.uint64_t S = 0

    S += sat[r1, c1]

    if (r0 - 1 >= 0) and (c0 - 1 >= 0):
        S += sat[r0 - 1, c0 - 1]

    if (r0 - 1 >= 0):
        S -= sat[r0 - 1, c1]

    if (c0 - 1 >= 0):
        S -= sat[r1, c0 - 1]

    return S

cpdef np.ndarray window_wrap(int m0, int n0, int m1, int n1,
                             int rows, int cols):
    """Calculate the corner-coordinates of the sub-windows resulting
    when wrapping one window around another.

    ::


      No wrapping:

      .________.
      |  ___   |
      | |   |  |
      | |___|  |
      |________|

      Column wrapping:

      .________.
      |_      _|
      | |    | |
      |_|    |_|
      |________|

      Row wrapping:

      .________.
      |  |___| |
      |        |
      |  .___. |
      |__|___|_|

      Diagonal wrapping:

      .________.
      |__|  |__|
      |        |
      |__.  .__|
      |__|__|__|


    Notes
    -----
    The algorithm works as follows:

    - Assume that all wrappings take place
    - Calculate the corners for each resulting window
    - Remove windows with negative coordinates
    - Clip all coordinates to the clipping window boundary

    """
    cdef int w, v

    cdef np.ndarray[np.int_t, ndim=2] windows = \
         np.zeros((4, 4), dtype=np.int)

    # main, column_wrap, row_wrap, diagonal_wrap

    windows[0, :] = [m0, n0, m1, n1]
    windows[1, :] = [m0, 0, m1, n1 - cols]
    windows[2, :] = [0, n0, m1 - rows, n1]
    windows[3, :] = [0, 0, m1 - rows, n1 - cols]

    for w in range(4):
        for v in range(4):
            if windows[w, v] < 0:
                windows[w, :] = [-1, -1, -1, -1]
                break

        for v in (0, 2):
            if windows[w, v] >= rows:
                windows[w, v] = rows - 1

        for v in (1, 3):
            if windows[w, v] >= cols:
                windows[w, v] = cols - 1

    return windows


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

    Notes
    -----
    While integral images are used, not all the suggestions made in
    [2] have been investigated.

    References
    ----------
    .. [1] J.P. Lewis, Fast Normalized Cross-Correlation, 1995,
           http://www.idiom.com/~zilla/.
    .. [2] D. Tsai and C. Lin, "Fast normalized cross correlation for
           defect detection," Pattern Recognition Letters, vol. 24, 2003.
    .. [3] F.C. Crow, "Summed-area tables for texture mapping,"
           ACM SIGGRAPH Computer Graphics, vol. 18, 1984, pp. 207-212.

    """
    cdef np.ndarray[np.uint8_t, ndim=2] S = imgS
    cdef np.ndarray[np.uint8_t, ndim=2] T = imgT
    cdef np.ndarray[np.double_t, ndim=2] out
    cdef np.ndarray[np.uint64_t, ndim=2] SAT = sat(S)
    cdef np.ndarray[np.uint64_t, ndim=2] SAT_var = sat(S.astype(np.uint64) ** 2)

    cdef int s_rows, s_cols, t_rows, t_cols, ta
    cdef double var_S, var_T, u_S, u_T, var_norm
    cdef np.uint8_t xS, xT

    s_rows = S.shape[0]
    s_cols = S.shape[1]
    t_rows = T.shape[0]
    t_cols = T.shape[1]
    ta = t_rows * t_cols # template area

    cdef int i, j, m, n, mm, nn
    cdef int row_start_S, row_end_S, col_start_S, col_end_S, \
             row_start_T, row_end_T, col_start_T, col_end_T, \
             row_range, col_range
    cdef np.ndarray[np.int_t, ndim=2] windows

    cdef double val

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

    # S is standing still.  The template, T, moves over S
    for i in range(s_rows):
        for j in range(s_cols):
            windows = window_wrap(i, j, i + t_rows - 1, j + t_cols - 1,
                                  s_rows, s_cols)

            u_S = 0
            var_S = 0

            for m in range(4):
                if windows[m, 0] != -1:
                    u_S += sat_sum(SAT, windows[m, 0], windows[m, 1],
                                        windows[m, 2], windows[m, 3])
                    var_S += sat_sum(SAT_var, windows[m, 0], windows[m, 1],
                                              windows[m, 2], windows[m, 3])

##             # Without the above optimisation. Approx factor 100 slow-down.
##             for m in range(t_rows):
##                 for n in range(t_cols):
##                     sm, sn = (i + m) % s_rows, (j + n) % s_cols
##                     u_S += S[sm, sn]
##                     var_S += S[sm, sn] ** 2

            u_S /= ta
            var_S /= ta
            var_S -= u_S ** 2

            val = 0
            for m in range(t_rows):
                for n in range(t_cols):
                    sm = (i + m) % s_rows
                    sn = (j + n) % s_cols

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
