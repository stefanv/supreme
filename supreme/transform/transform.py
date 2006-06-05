import numpy as N
from scipy.ndimage import interpolation as ndii

__all__ = ['logpolar']

import supreme
import supreme.config as SC
import numpy as N

def stackcopy(a,b):
    """a[:,:,0] = a[:,:,1] = ... = b"""
    a.transpose().swapaxes(1,2)[:] = b

def logpolar(image,angles=359,order=1):
    """Perform log polar transform on image."""

    ishape = N.array(image.shape)
    if len(ishape) < 2:
        raise ValueError("Input must have more than 1 dimension.")

    oshape = ishape
    w = max(ishape[:2])
    centre = ishape[:2]/2.
    
    oshape[0] = angles
    oshape[1] = w
    log_base = N.log(w/2)/w

    from math import sin, cos, e
    coords = N.empty(N.r_[3,angles,w,3],dtype=SC.ftype)
    theta = N.empty((angles,w),dtype=SC.ftype)
    theta.transpose()[:] = N.linspace(0,2*N.pi,angles+1)[:-1] 
    L = N.empty((angles,w),dtype=SC.ftype)
    L[:] = N.arange(w).astype(SC.ftype)

#    print g.coords[...,0].shape
#    coords[0,...,0] = g.coords[...,0]
#    coords[0,...,1] = g.coords[...,0]
#    coords[0,...,2] = g.coords[...,0]

    r = N.exp(L*log_base)
    print r*N.sin(theta)

    # x-coordinate mapping
    stackcopy(coords[0,...], r*N.sin(theta) + centre[0])

    # y-coordinate mapping
    stackcopy(coords[1,...], r*N.cos(theta) + centre[1])
    
    # colour-coordinate mapping
    coords[2,...] = [0,1,2]
    
#        theta = angles[theta]
#        r = e**(L*log_base)
#        return (r*sin(theta) + centre[0],
#                r*cos(theta) + centre[1],col)

    # Prefilter not necessary for order 1 interpolation
    prefilter = order > 1
    return ndii.map_coordinates(image,coords,order=order,prefilter=prefilter)
