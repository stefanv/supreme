import numpy as np

def gauss(size=5, std=1.0):
    """Discretised Gaussian window.

    Parameters
    ----------
    size : int
        The generated window has dimensions ``(size, size)``.
    std : float
        Standard deviation.

    Returns
    -------
    w : (size, size) ndarray
        Discretised Gaussian window.

    """
    x, y = np.mgrid[:size, :size]
    hwin = (size - 1) / 2
    x -= hwin
    y -= hwin
    w = np.exp(-(x**2 + y**2)/(2 * std**2)) / (2 * np.pi * std**2)

    return w
