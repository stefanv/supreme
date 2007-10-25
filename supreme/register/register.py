"""Perform image registration."""

__all__ = ['PointCorrespondence','refine','sparse']

import numpy as N
import scipy as S
import scipy.optimize
import scipy.linalg

from numpy.testing import set_local_path, restore_path

import sys

set_local_path('../..')
import supreme as sr
from supreme.config import ftype,itype
import supreme as sr
restore_path()

class PointCorrespondence(object):
    """Estimate point correspondence homographies."""

    def __init__(self, ref_feat_rows, ref_feat_cols,
                 target_feat_rows, target_feat_cols,
                 mode='direct'):
        self.rx,self.ry,self.tx,self.ty = \
                map(N.asarray,[ref_feat_cols,ref_feat_rows,
                               target_feat_cols,target_feat_rows])

        assert len(self.rx) == len(self.ry) == len(self.tx) == len(self.ty), \
               "Equal number of coordinates expected."

        if mode == 'direct':
            self.estimate = self._estimate_direct
        else:
            self.estimate = self._estimate_iterative

    def _estimate_direct(self):
        """Estimate the homographic point correspondence.

        Output:
        -------
        H : (3,3) array of floats

            Input point: x = [c_0, c_1, c_2]^T

            Output point: x' = [c'_0, c'_1, c'_2]^T

            Input and output points are related by

                ``x' = Hx``

            Given errors in the measurement, H minimises

                ``|x' - Hx'|``

        See Digital Image Warping by George Wolberg, p. 54.

        """

        rx,ry,tx,ty = self.rx,self.ry,self.tx,self.ty

        nr = len(self)

        U = N.zeros((2*nr,8),dtype=ftype)
        # x-coordinates
        U[:nr,0] = tx
        U[:nr,1] = ty
        U[:nr,2] = 1.
        U[:nr,6] = -tx*rx
        U[:nr,7] = -ty*rx

        # y-coordinates
        U[nr:,3] = tx
        U[nr:,4] = ty
        U[nr:,5] = 1.
        U[nr:,6] = -tx*ry
        U[nr:,7] = -ty*ry

        B = N.concatenate((rx,ry))[:,N.newaxis]

        M,res,rank,s = scipy.linalg.lstsq(U,B)

        return True,N.append(M,1).reshape((3,3))

    def _estimate_iterative(self):
        rx,ry,tx,ty = self.rx,self.ry,self.tx,self.ty

        rcoord = N.vstack((rx,ry,N.ones_like(rx))).T
        tcoord = N.vstack((tx,ty,N.ones_like(tx))).T

        def build_transform_from_params(p):
            theta,tx,ty,s = p
            return N.array([[s*N.cos(theta),-s*N.sin(theta),tx],
                            [s*N.sin(theta), s*N.cos(theta),ty],
                            [0,              0,             1.]])

        def model(p):
            tf_arr = build_transform_from_params(p)
            tc = N.dot(tcoord,tf_arr.T)
            return N.sum((rcoord - tc)**2,axis=1)

        pout,ignore,ignore,mesg,ier = S.optimize.leastsq(model,
                                                         [0,0,0,1],
                                                         maxfev=5000,
                                                         full_output=True)
        if ier != 1 and ier != 2:
            print "Warning: error status", ier
            print mesg
        return (ier==1),build_transform_from_params(pout)

    def transform(self,M):
        raise NotImplementedError

    def reject(self):
        raise NotImplementedError

    def __len__(self):
        """The number of points."""
        return len(self.rx)

def sparse(ref_feat_rows,ref_feat_cols,
        target_feat_rows,target_feat_cols,**kwargs):
    """Compatibility wrapper. Calculate the PointCorrespondence
    homography which maps reference features to target features.

    See also: PointCorrespondence

    """

    p = PointCorrespondence(ref_feat_rows,ref_feat_cols,
                            target_feat_rows,target_feat_cols,
                            **kwargs)

    M = p.estimate()
    return M

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
