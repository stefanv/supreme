"""Image warping algorithms, e.g. log-polar transform."""

import numpy as N
from scipy.ndimage import interpolation as ndii

__all__ = ['logpolar','matrix']

import supreme
import supreme.config as SC
from supreme.ext import interp_bilinear

def stackcopy(a,b):
    """a[:,:,0] = a[:,:,1] = ... = b"""
    if a.ndim == 3:
        a.transpose().swapaxes(1,2)[:] = b
    else:
        a[:] = b

def _lpcoords(ishape,w,angles=None):
    """Calculate the reverse coordinates for the log-polar transform.

    Return array is of shape (len(angles),w)

    """

    ishape = N.array(ishape)
    bands = ishape[2]
    
    oshape = ishape.copy()
    centre = (ishape[:2]-1)/2.

    d = N.hypot(*(ishape[:2]-centre))
    log_base = N.log(d)/w

    if angles is None:
        angles =  -N.linspace(0,2*N.pi,359+1)[:-1]
    theta = N.empty((len(angles),w),dtype=SC.ftype)
    # Use broadcasting to replicate angles
    theta.transpose()[:] = angles
    
    L = N.empty_like(theta)
    # Use broadcasting to replicate distances
    L[:] = N.arange(w).astype(SC.ftype)

    r = N.exp(L*log_base)

    return r*N.sin(theta) + centre[0], r*N.cos(theta) + centre[1]

def logpolar(image,angles=None,mode='M',cval=0,output=None,
             _coords_r=None,_coords_c=None):
    """Perform the log polar transform on an image.

    Input:
    ------
    image  -- MxNxC image
    angles -- Angles at which to evaluate. Defaults to 0..2*Pi in 359 steps.
    mode   -- Value outside border: 'C' for constant, 'M' for mirror and
              'W' for wrap.
    cval   -- Outside border value for mode 'C'.
    
    Optimisation parameters:
    ------------------------
    _coords_r, _coords_c -- Pre-calculated coords, as given by _lpcoords.
    
    """

    if image.ndim < 2 or image.ndim > 3:
        raise ValueError("Input image must be 2 or 3 dimensional.")

    image = N.atleast_3d(image)

    w = max(image.shape[:2])

    if _coords_r is None or _coords_c is None:
        _coords_r, _coords_c = _lpcoords(image.shape,w,angles)

    bands = image.shape[2]
    if output is None:
        output = N.empty(_coords_r.shape + (bands,),dtype=N.uint8)
    else:
        output = N.atleast_3d(N.ascontiguousarray(output))
    for band in range(bands):
        output[...,band] = interp_bilinear(image[...,band],
                                           _coords_r,_coords_c,mode=mode,
                                           cval=cval,output=output[...,band])
        
    return output.squeeze()

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

    Input:
    ------
    order   -- order of splines used in interpolation.
    mode    -- passed to ndimage -- what to do outside boundaries
    cval    -- value to return outside boundaries, if mode is 'constant'
    
    """

    if image.ndim < 2:
        raise ValueError("Input must have more than 1 dimension.")

    image = N.atleast_3d(image)
    ishape = N.array(image.shape)
    bands = ishape[2]
        
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
