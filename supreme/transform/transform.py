import numpy as N
from scipy.ndimage import interpolation as ndii

__all__ = ['logpolar','matrix']

import supreme
import supreme.config as SC

def stackcopy(a,b):
    """a[:,:,0] = a[:,:,1] = ... = b"""
    if a.ndim == 3:
        a.transpose().swapaxes(1,2)[:] = b
    else:
        a[:] = b

def _lpcoords(ishape,angles,w):
    """Calculate the reverse coordinates for the log-polar transform."""

    ishape = N.array(ishape)
    bands = ishape[2]
    
    oshape = ishape.copy()
    centre = (ishape[:2]-1)/2.
    
    oshape[0] = angles
    oshape[1] = w
    d = N.hypot(*(ishape[:2]-centre))
    log_base = N.log(d/2)/w

    coords = N.empty(N.r_[3,oshape],dtype=SC.ftype)

    theta = N.empty((angles,w),dtype=SC.ftype)
    # Use broadcasting to replicate angles
    theta.transpose()[:] = -N.linspace(0,2*N.pi,angles+1)[:-1]
    
    L = N.empty((angles,w),dtype=SC.ftype)
    # Use broadcasting to replicate distances
    L[:] = N.arange(w).astype(SC.ftype)

    r = N.exp(L*log_base)

    # y-coordinate mapping
    stackcopy(coords[0,...], r*N.sin(theta) + centre[0])

    # x-coordinate mapping
    stackcopy(coords[1,...], r*N.cos(theta) + centre[1])
    
    # colour-coordinate mapping
    coords[2,...] = range(bands)

    return coords

def logpolar(image,angles=359,order=1,_coords=None):
    """Perform the log polar transform on an image.

    angles - Number of angles at which to evaluate.
    order - Order of splines used in interpolation.
    
    _coords - Pre-calculated coords, as given by _lpcoords.
    """

    if image.ndim < 2:
        raise ValueError("Input must have more than 1 dimension.")

    image = N.atleast_3d(image)

    w = max(image.shape[:2])

    if _coords is None:
        _coords = _lpcoords(image.shape,angles,w)
    
    # Prefilter not necessary for order 1 interpolation
    prefilter = order > 1
    mapped = ndii.map_coordinates(image,_coords,order=order,prefilter=prefilter,
                                  mode='reflect')

    return mapped.squeeze()

def matrix(image,matrix,output_shape=None,order=1,mode='constant',
           cval=0.):
    """Perform a matrix transform on an image.

    Each coordinate (x,y,1) is multiplied by matrix to find its
    new position.  E.g., to rotate by theta degrees clockwise,
    the matrix should be

    [[cos(theta) -sin(theta) 0]
     [sin(theta)  cos(theta) 0]
     [0            0         1]]

    or to translate x by 10 and y by 20,

    [[1 0 10]
     [0 1 20]
     [0 0 1 ]].

    reshape - whether or not to reshape the output to contain
              the whole transformed image
    order - order of splines used in interpolation.
    """

    if image.ndim < 2:
        raise ValueError("Input must have more than 1 dimension.")

    image = N.atleast_3d(image)
    ishape = N.array(image.shape)
    if image.ndim > 2:
        bands = ishape[2]
    else:
        bands = 1
        
    if output_shape is None:
        output_shape = ishape

    coords = N.empty(N.r_[3,output_shape],dtype=SC.ftype)
    tf_coords = supreme.geometry.Grid(*output_shape[:2]).coords
    tf_coords = N.dot(tf_coords,N.linalg.inv(matrix).transpose())
    tf_coords[N.absolute(tf_coords) < SC.eps] = 0.

    # y-coordinate mapping
    stackcopy(coords[0,...], tf_coords[...,1])

    # x-coordinate mapping
    stackcopy(coords[1,...], tf_coords[...,0])

    # colour-coordinate mapping
    coords[2,...] = range(bands)
    
    # Prefilter not necessary for order 1 interpolation
    prefilter = order > 1
    mapped = ndii.map_coordinates(image,coords,prefilter=prefilter,
                                  mode=mode,order=order,cval=cval)

    return mapped.squeeze()
