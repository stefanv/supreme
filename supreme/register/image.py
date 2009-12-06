"""Image analysis routines."""

import numpy as np
import scipy.signal as ss
from numpy.fft import fft2, ifft2

__all__ = ['fft_corr', 'phase_corr']

def fft_corr(A, B, *args, **kwargs):
    return ss.fftconvolve(A, B[::-1, ::-1, ...], *args, **kwargs)

def phase_corr(A, B):
    """Phase correlation of two images.

    Parameters
    ----------
    A, B : (M,N) ndarray
        Input images.

    Returns
    -------
    out : (M,N) ndarray
        Correlation coefficients.

    Examples
    --------

    Set up test data.  One array is offset (10, 10) from the other.

    >>> x = np.random.random((50, 50))
    >>> y = np.zeros_like(x)
    >>> y[10:, 10:] = x[0:-10, 0:-10]

    Correlate the two arrays, and ensure the peak is at (10, 10).

    >>> out = phase_corr(y, x)
    >>> m, n = np.unravel_index(np.argmax(out), out.shape)
    >>> print m, n
    (10, 10)

    """
    out = fft2(A) * fft2(B).conj()
    out /= np.abs(out)
    out = np.abs(ifft2(out))

    return out
