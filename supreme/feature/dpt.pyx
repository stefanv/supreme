# -*- python -*-

"""Extract image features, using the discrete pulse transform.

"""

# cython: cdivision(True)

__all__ = ['features']

import numpy as np
cimport numpy as np
cimport cython

from supreme.lib.dpt.connected_region cimport ConnectedRegion
cimport supreme.lib.dpt.connected_region_handler as crh

import supreme.config
_log = supreme.config.get_log(__name__)

cdef extern from "math.h":
    double pow(double, double)

cdef add_f_array(np.ndarray a, np.float64_t value, ConnectedRegion cr):
    """Add 'value' to the array over the connected region.

    """
    cdef np.ndarray[np.float64_t, ndim=2] arr = a
    cdef int rows = arr.shape[0]
    cdef int cols = arr.shape[1]

    cdef int* rowptr = cr.rowptr.buf
    cdef int* colptr = cr.colptr.buf

    cdef int r, c, start, end, k, start_row = cr._start_row

    for r in range(cr.rowptr.size - 1):
        for c in range((rowptr[r + 1] - rowptr[r]) / 2):
            start = colptr[rowptr[r] + 2*c]
            end = colptr[rowptr[r] + 2*c + 1]

            for k in range(start, end):
                if r >= 0 and r < rows and \
                   start >= 0 and start < cols and \
                   end >= 0 and end <= cols:
                    arr[r + start_row, k] += value

cdef int iabs(int x):
    if x >= 0:
        return x
    else:
        return -x

cdef np.double_t dabs(np.double_t x):
    if x >= 0:
        return x
    else:
        return -x

cpdef features(dict pulses, shape, win_size=0):
    """Find feature points.

    Parameters
    ----------
    pulses : dict
        The pulses dictionary returned by the discrete pulse
        transform.
    shape : tuple of ints
        Shape of the image on which the DPT was performed.
    win_size : int
        Do not return more than one feature from any ``win_size x win_size``
        shaped area.

    Returns
    -------
    weight : ndarray of float
        An array of the same shape as the image, with values indicating
        the likelihood of any pixel being a feature.
    area : ndarray of float
        The estimated area of the feature at each pixel.

    See Also
    --------
    supreme.lib.dpt

    """
    cdef ConnectedRegion cr
    cdef int nnz, i, j, ii, jj
    cdef double T, mean_A, mean_B, beta, lamb
    cdef double mean, stdev
    cdef int total_A, total_B
    cdef int hwin
    cdef np.ndarray[np.double_t, ndim=2] weight = np.zeros(shape, dtype=float)
    cdef np.ndarray[np.int_t, ndim=2] area = np.zeros(shape, dtype=np.int)

    for nnz in sorted(pulses):
        for cr in pulses[nnz]:
            add_f_array(weight, iabs(cr._value) / pow(<double>cr._nnz, 0.5),
                        cr)
            crh._set_array(<np.int_t*>area.data,
                           shape[0], shape[1], cr,
                           cr._nnz, 1)

    weight -= weight.min()
    beta = weight.mean()
    lamb = 1/beta
    stdev = weight.std()

    hwin = (win_size - 1) / 2
    for i in range(shape[0]):
        for j in range(shape[1]):
            # Filter peak, based on surrounding values
            for ii in range(i - hwin, i + hwin + 1):
                for jj in range(j - hwin, j + hwin + 1):
                    if (ii <= 0) or (ii >= shape[0]) or \
                       (jj <= 0) or (jj >= shape[1]):
                        continue

                    if weight[ii, jj] > weight[i, j]:
                        weight[i, j] = 0

    _log.info('Features found: %s' % np.sum(weight != 0))

    return weight, area
