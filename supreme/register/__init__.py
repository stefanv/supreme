# Registration module

import stack
from image import *
from register import *
from logpolar import patch_match as lp_patch_match
from logpolar import *
from correspond import *
from ncorr import *

def affine_tm(theta=0, tx=0, ty=0, scale=None, scale_x=None, scale_y=None):
    """Return the transformation matrix for an affine transformation.

    Parameters
    ----------
    theta : float
        Rotation angle in radians.
    tx, ty : float
        X and Y translations.
    scale : float
        Scaling in both the X and the Y directions.  Defaults to 1.
    scale_x : float
        Scaling in the X direction.  Cannot be used together with `scale`.
    scale_y : float
        Scaling in the Y direction.  Cannot be used with `scale`.

    Returns
    -------
    M : ndarray of float
        Transformation matrix with the supplied parameters.  Can be used to
        transform any homogeneous coordinate ``p = [[x, y, 1]].T`` by
        ``np.dot(M, p)``.

    """
    if scale is not None:
        if scale_x is not None or scale_y is not None:
            raise ValueError("Cannot use scale in combination with "
                             "`scale_x` or `scale_y`.")
        scale_x = scale
        scale_y = scale
    else:
        if scale_x is None:
            scale_x = 1
        if scale_y is None:
            scale_y = 1

    a = scale_x
    b = scale_y
    C = np.cos(theta)
    S = np.sin(theta)

    return np.array([[a*C,  -b*S, tx],
                     [a*S,   b*C, ty],
                     [0,     0,   1.]])
