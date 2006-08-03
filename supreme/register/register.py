"""Perform image registration."""

__all__ = ['logpolar']

import numpy as N
from numpy.testing import set_local_path, restore_path
import sys

set_local_path('../../..')
from supreme.config import ftype,itype
from supreme import geometry
from supreme import transform
restore_path()

def rectangle_inside(shape,percent=10):
    """Return a path inside the border defined by shape."""
    shape = N.asarray(shape)
    rtop = N.round_(shape*percent/100.)
    rbottom = shape - rtop

    cp = geometry.coord_path
    return cp.build(cp.rectangle(rtop,rbottom))

def logpolar_along_path(image,path,shape):
    """Cut sub-images at each coordinate on the path and yield the log
    polar transform.

    """
    for cut in geometry.cut.along_path(path,image,shape):
        yield transform.logpolar(cut)

def logpolar(ref_img,img_list,window_shape=(50,50)):
    """Register the given images using log polar transforms.

    The output is a list of 3x3 arrays.
    
    """
    print "Calculating log polar transforms for reference frame..."

    for i in logpolar_along_path(ref_img,
                                 rectangle_inside(ref_img.shape[:2],20),
                                 (51,51)):
        sys.stdout.write('.')
        sys.stdout.flush()
        

