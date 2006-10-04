"""Chirp z-Transform.

As described in

Rabiner, L.R., R.W. Schafer and C.M. Rader.
The Chirp z-Transform Algorithm.
IEEE Transactions on Audio and Electroacoustics, AU-17(2):86--92, 1969
"""

import numpy as np

import supreme.config as SC

def chirpz(x,A,W,M):
    """Compute the chirp z-transform.

    The discrete z-transform,

    X(z) = \sum_{n=0}^{N-1} x_n z^{-n}

    is calculated at M points,

    z_k = AW^-k, k = 0,1,...,M-1

    for A and W complex, which gives

    X(z_k) = \sum_{n=0}^{N-1} x_n z_k^{-n}    

    """
    A = np.complex(A)
    W = np.complex(W)
    x = np.asarray(x,dtype=SC.ftype)
    
    N = x.size
    L = int(2**np.ceil(np.log2(M+N-1)))

    n = np.arange(N,dtype=SC.ftype)
    y = np.power(A,-n) * np.power(W,n**2 / 2.) * x 
    Y = np.fft.fft(y,L)

    n = np.arange(L)    
    v = np.power(W,-n**2/2.)
    V = np.fft.fft(v,L)
    
    g = np.fft.ifft(V*Y)[N:N+M]
    k = np.arange(M)
    g *= np.power(W,k**2 / 2.)

    return g