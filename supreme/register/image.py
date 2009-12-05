"""Image analysis routines."""

import numpy as np
import scipy.signal as ss
from numpy.fft import fft2, ifft2

__all__ = ['fft_correlate']

def fft_correlate(A, B, *args, **kwargs):
    return ss.fftconvolve(A, B[::-1, ::-1, ...], *args, **kwargs)

def phase_corr(A, B):
    """Phase correlation of two images.

    Parameters
    ----------
    A, B : (M,N) ndarray
        Input images.

    Returns
    -------
    m : int
        Row-position of the maximum correlation.
    n : int
        Column-position of the maximum correlation.
    p : int
        Peak value of the correlation.

    """
    out = fft2(A) * fft2(B).conj()
    out /= np.abs(out)
    out = np.abs(ifft2(out))

    m, n = np.unravel_index(np.argmax(out), out.shape)
    p = out.max()

    return m, n, p
