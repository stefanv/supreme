import numpy as N
from scipy.ndimage import interpolation as ndii

__all__ = ['logpolar']

import supreme
import supreme.config as SC
import numpy as N

def stackcopy(a,b):
    """a[:,:,0] = a[:,:,1] = ... = b"""
    if a.ndim == 3:
        a.transpose().swapaxes(1,2)[:] = b
    else:
        a.transpose()[:] = b

def logpolar(image,angles=359,order=1):
    """Perform the log polar transform on an image.

    angles - Number of angles at which to evaluate.
    order - Order of splines used in interpolation.
    """

    image = N.atleast_3d(image)

    if image.ndim < 2:
        raise ValueError("Input must have more than 1 dimension.")

    ishape = N.array(image.shape)
    if image.ndim > 2:
        bands = ishape[2]
    else:
        bands = 1

    oshape = ishape
    w = max(ishape[:2])
    centre = ishape[:2]/2.
    
    oshape[0] = angles
    oshape[1] = w
    log_base = N.log(w/2)/w

    from math import sin, cos, e
    coords = N.empty(N.r_[3,oshape],dtype=SC.ftype)

    theta = N.empty((angles,w),dtype=SC.ftype)
    # Use broadcasting to replicate angles
    theta.transpose()[:] = -N.linspace(0,2*N.pi,angles+1)[:-1]
    
    L = N.empty((angles,w),dtype=SC.ftype)
    # Use broadcasting to replicate distances
    L[:] = N.arange(w).astype(SC.ftype)

    r = N.exp(L*log_base)

    # x-coordinate mapping
    stackcopy(coords[0,...], r*N.sin(theta) + centre[0])

    # y-coordinate mapping
    stackcopy(coords[1,...], r*N.cos(theta) + centre[1])
    
    # colour-coordinate mapping
    coords[2,...] = range(bands)
    
    # Prefilter not necessary for order 1 interpolation
    prefilter = order > 1
    mapped = ndii.map_coordinates(image,coords,order=order,prefilter=prefilter)

    return mapped.squeeze()
