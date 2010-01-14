import numpy as np

def photometric_adjust(source, target):
    """Adjust the intensity of source to look like target.

    Parameters
    ----------
    source, target : ndarray
        Source and target images.

    Returns
    -------
    a, b : float
        Adjustment factors so that ``source * a + b`` approximates
        target.

    """
    mask = (source > 0) & (target > 0) & (source < 210) & (target < 210)

    mu_s = np.mean(source[mask])
    std_s = np.std(source[mask])
    mu_t = np.mean(target[mask])
    std_t = np.std(target[mask])

    a = std_t / std_s
    b = (mu_t * std_s - mu_s * std_t)/std_s

    return a, b
