import numpy as np

def photometric_adjust(source, target):
    """Adjust the intensity of source to look like target.

    Parameters
    ----------
    source, target : ndarray
        Source and target images.

    Returns
    -------
    f : float
        Adjustment factor so that ``source * f`` approximates
        target.

    """
    # Ignore values close to saturation
    mask = (source > 20) & (source < 220) & \
           (target > 20) & (target < 220)

    return np.median(target[mask].astype(float) / source[mask])
