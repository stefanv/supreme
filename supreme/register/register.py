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

def logpolar(ref_img,img_list,window_shape=(51,51)):
    """Register the given images using log polar transforms.

    The output is a list of 3x3 arrays.
    
    """

    for img in img_list:
        assert ref_img.shape == img.shape

    def lp_frame(img,shape=window_shape):
        path = rectangle_inside(ref_img.shape[:2],30)
        coords = None
        for cut in geometry.cut.along_path(path,img,shape):
            if coords is None:
                # Pre-calculate coordinates
                coords = transform.transform._lpcoords(cut.shape,359,max(cut.shape[:2]))
                
            yield transform.logpolar(cut,_coords=coords)

    print "Calculating log polar transforms for reference frame..."
    ref_lpt = list(lp_frame(ref_img))

    for img in img_list:
        for tf in lp_frame(img):
            print "Correlating"
