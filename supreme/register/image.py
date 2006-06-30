"""Image analysis routines."""

import scipy as S
S.pkgload('signal')

__all__ = ['fft_correlate']

def fft_correlate(A,B,*args,**kwargs):
    return S.signal.fftconvolve(A,B[::-1,::-1,...],*args,**kwargs)
