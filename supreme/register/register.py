"""Perform image registration."""

__all__ = ['logpolar','sparse','refine']

import numpy as N
import scipy as S
import scipy.optimize
from numpy.testing import set_local_path, restore_path
import sys
import warnings

set_local_path('../../..')
import supreme as sr
from supreme.config import ftype,itype
from supreme import geometry
from supreme import transform
restore_path()

def sparse(ref_feat_rows,ref_feat_cols,
           target_feat_rows,target_feat_cols):
    rx,ry,tx,ty = map(N.asarray,[ref_feat_cols,ref_feat_rows,
                                 target_feat_cols,target_feat_rows])
    one = N.ones(len(rx))
    rcoord = N.vstack((rx,ry,one)).T
    tcoord = N.vstack((tx,ty,one)).T

    def _buildmat(p):
        theta,a,b,tx,ty = p
        return N.array([[a*N.cos(theta),-a*N.sin(theta),tx],
                        [a*N.sin(theta),a*N.cos(theta),ty],
                        [0,0,1]])

    def tf_model(p):
        M = _buildmat(p)
        tc = N.dot(tcoord,M.T)
        return N.sqrt(N.sum((rcoord - tc)**2,axis=1))

    p_default = N.array([0,1,1,0,0])
    p = p_default.copy()

    for i in range(3):
        try:
            p,ier = S.optimize.leastsq(tf_model,p,maxfev=500000)
        except:
            p,ier = p_default, -1

        print "Number of features: ", len(tcoord)

        # trivial outlier rejection
        d = tf_model(p)
        mask = (d <= 0.8*d.mean()) | (d <= .25)
        tcoord = tcoord[mask]
        rcoord = rcoord[mask]

        if len(tcoord) < 10:
            return N.eye(3), -1

    if ier != 1:
        warnings.warn("Sparse registration did not converge.")
    else:
        print "P = ", p
    return p, ier

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

def _build_tf(p):
    if N.sum(N.isnan(p) + N.isinf(p)) != 0:
        return N.eye(3)
    else:
        theta,a,b,tx,ty = p
        C = N.cos(theta)
        S = N.sin(theta)
        return N.array([[a*C, -a*S, tx],
                        [a*b*S, a*C, ty],
                        [0,0,1]])

def _tf_difference(p,p_ref,reference,target):
    """Calculate difference between reference and transformed target."""
    tf_target = _build_tf(p)
    tf_ref = _build_tf(p_ref)
    im1 = sr.transform.matrix(reference,tf_ref)
    im2 = sr.transform.matrix(target,tf_target)
    diff = ((im1 - im2)**2)
    # TODO: do polygon overlap check
    return diff.sum()

def refine(reference,target,p_ref,p_target):
    """Refine registration parameters iteratively."""

    p = scipy.optimize.fmin_cg(_tf_difference,p_target,
                               args=(p_ref,reference,target))
    return p

