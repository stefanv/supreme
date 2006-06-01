import numpy as N
from scipy.ndimage import interpolation as ndii

__all__ = ['logpolar']

import supreme
import numpy as N

def logpolar(image,angles=N.linspace(0,2*N.pi,360)[:-1]):
    """Perform log polar transform on image."""

    ishape = N.array(image.shape)
    if len(ishape) < 2:
        raise ValueError("Input must have more than 1 dimension.")

    oshape = ishape
    w = max(ishape[:2])
    centre = ishape[:2]/2.
    
    oshape[0] = len(angles)
    oshape[1] = w
    log_base = N.log(w/2)/w

    from math import sin, cos, e
    
    def lp_coord(coord,log_base=log_base,angles=angles,centre=centre):
        theta,L,col = coord
        theta = angles[theta]
        r = e**(L*log_base)
        return (r*sin(theta) + centre[0],
                r*cos(theta) + centre[1],col)

    return ndii.geometric_transform(image,lp_coord,output_shape=oshape,
                                    prefilter=False)
