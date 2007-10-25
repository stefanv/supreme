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
from supreme.feature import RANSAC
from supreme.misc.inject import interface
restore_path()

class Homography(object):
    """Model of a homography for use with RANSAC.

    """
    # Minimum number of points required to estimate.
    @property
    def ndp(self): return 4

    def __init__(self,H=N.eye(3)):
        self.parameters = H

    def set_parameters(self,H):
        assert H.ndim == 2
        assert H.shape == (3,3)
        self._H = H

    def get_parameters(self):
        return self._H

    parameters = property(fget=get_parameters,fset=set_parameters)

    def __call__(self,data,H=None,confidence=0.8):
        if H is None: H = self.parameters
        ones = N.ones_like(data[:,0]).reshape(-1,1)
        rcoord = N.hstack((data[:,:2],ones))
        tcoord = N.hstack((data[:,2:],ones))

        tc = N.dot(tcoord,H.T)
        error = N.sqrt(N.sum((rcoord - tc)**2,axis=1))
        return error, error < (1-confidence)*5

    def estimate(self,data):
        H,ignored = self.estimate_direct(data)
        return H,True

    def _data_from_array(self,data):
        data = N.asarray(data)
        return data[:,0], data[:,1], data[:,2], data[:,3]

    def estimate_direct(self,data):
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

        success : bool
            Whether or not the calculation could be made.

        See Digital Image Warping by George Wolberg, p. 54.

        """
        rx,ry,tx,ty = self._data_from_array(data)

        nr = len(data)

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

        return N.append(M,1).reshape((3,3)),True

    def _build_transform_from_params(self,p):
            theta,tx,ty,s = p
            return N.array([[s*N.cos(theta),-s*N.sin(theta),tx],
                            [s*N.sin(theta), s*N.cos(theta),ty],
                            [0,              0,             1.]])

    def estimate_iterative(self,data):
        rx,ry,tx,ty = self._data_from_array(data)

        rcoord = N.vstack((rx,ry,N.ones_like(rx))).T
        tcoord = N.vstack((tx,ty,N.ones_like(tx))).T

        def err_func(p):
            err,inlier = self(data,
                              H=self._build_transform_from_params(p))
            return err

        pout,ignore,ignore,mesg,ier = S.optimize.leastsq(err_func,
                                                         [0,0,0,1],
                                                         maxfev=5000,
                                                         full_output=True)
        if ier != 1 and ier != 2:
            print "Warning: error status", ier
            print mesg
        return self._build_transform_from_params(pout),(ier==1)

interface(Homography,RANSAC.IModel)

class PointCorrespondence(object):
    """Estimate point correspondence homographies."""

    def __init__(self, ref_feat_rows, ref_feat_cols,
                 target_feat_rows, target_feat_cols,
                 **args):

        self.data = N.dstack([ref_feat_cols,ref_feat_rows,
                              target_feat_cols,target_feat_rows]).squeeze()

        self.mode = args.get('mode','direct').lower()
        self.args = args

    def estimate(self):
        if self.mode == 'direct':
            return Homography().estimate_direct(self.data)
        elif self.mode == 'iterative':
            return Homography().estimate_iterative(self.data)
        else:
            return self.RANSAC()

    def RANSAC(self):
        M = Homography()
        R = RANSAC.RANSAC(M,2/3.)
        return R(self.data,len(self.data)/2,self.args.get('confidence',None))

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

def refine(reference,target,p_ref,p_target):
    """Refine registration parameters iteratively."""

    def _tf_difference(p,p_ref,reference,target):
        """Calculate difference between reference and transformed target."""
        tf_target = _build_tf(p)
        tf_ref = _build_tf(p_ref)
        im1 = sr.transform.matrix(reference,tf_ref)
        im2 = sr.transform.matrix(target,tf_target)
        diff = ((im1 - im2)**2)
        # TODO: do polygon overlap check
        return diff.sum()

    p = scipy.optimize.fmin_cg(_tf_difference,p_target,
                               args=(p_ref,reference,target))
    return p
