__all__ = ['dwt_denoise']

import numpy as np

from supreme.lib import pywt

def _denoise_band(X, wavelet, levels, alpha):
    from var_est import variance

    if alpha is None:
        alpha = 2

    decomp = pywt.wavedec2(X, wavelet, level=levels)
    for i, all_coeff in enumerate(decomp[1:]):
        minvar = np.empty(all_coeff[0].shape, dtype=float)
        minvar.fill(np.inf)
        # Handle horizontal, vertical and diagonal coefficients
        for coeff in all_coeff:
            for win_size in (3, 5, 7, 9):
                var = variance(coeff, win_size)
                mask = (var < minvar)
                minvar[mask] = var[mask]

            # Wiener estimator
            coeff *= (minvar / (minvar + alpha))

    rec = pywt.waverec2(decomp, wavelet)
    rows, cols = X.shape
    if X.shape != rec.shape:
        rows_mod = rows % 2
        cols_mod = cols % 2
        return rec[rows_mod:, cols_mod:]
    else:
        return rec

def dwt_denoise(X, wavelet='db8', levels=4, alpha=2):
    """Denoise an image using the Discrete Wavelet Transform.

    Parameters
    ----------
    X : ndarray of uint8
        Image to denoise.
    wavelet : str
        Wavlet family to use.  See `supreme.lib.pywt.wavelist()` for a
        complete list.
    levels : int
        Number of levels to use in the decomposition.
    alpha : float
        Parameter used to tweak the Wiener estimator.  A larger
        value of `alpha` results in a smoother output.

    Returns
    -------
    Y : ndarray of float64
        Denoised image.

    Notes
    -----
    Implemented according to the overview of [2]_ given in [1]_.

    References
    ----------
    .. [1] J. Fridrich, "Digital Image Forensics," IEEE Signal Processing
           Magazine, vol. 26, 2009, pp. 26-37.
    .. [2] M. Mihcak, I. Kozintsev, K. Ramchandran, and P. Moulin,
           "Low-complexity image denoising based on statistical
           modeling of wavelet coefficients," IEEE Signal Processing
           Letters, vol. 6, 1999, pp. 300-303.

    """
    out = np.zeros(X.shape, dtype=float)
    if X.ndim == 3:
        bands = X.shape[2]

        for b in range(bands):
            out[:, :, b] = _denoise_band(X[..., b], wavelet, levels, alpha)
    else:
        out[:] = _denoise_band(X, wavelet, levels, alpha)

    return out
