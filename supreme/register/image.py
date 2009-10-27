"""Image analysis routines."""

import scipy.signal as ss

__all__ = ['fft_correlate']

def fft_correlate(A, B, *args, **kwargs):
    return ss.fftconvolve(A, B[::-1, ::-1, ...], *args, **kwargs)
