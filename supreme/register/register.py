"""Perform image registration."""

__all__ = ['PointCorrespondence','refine','sparse']

import numpy as np
import scipy as sp
import scipy.optimize
import scipy.linalg

import sys

import supreme as sr
from supreme.config import ftype
from supreme.feature import RANSAC

class Homography(object):
    """Model of a homography for use with RANSAC.

    """
    # Minimum number of points required to estimate.
    @property
    def ndp(self): return 4

    def __init__(self, H=np.eye(3)):
        self.parameters = H

    def set_parameters(self, H):
        assert H.ndim == 2
        assert H.shape == (3,3)
        self._H = H

    def get_parameters(self):
        return self._H

    parameters = property(fget=get_parameters, fset=set_parameters)

    def __call__(self, data, H=None, confidence=0.8):
        if H is None:
            H = self.parameters

        ones = np.ones_like(data[:, 0]).reshape(-1, 1)
        rcoord = np.hstack((data[:, :2], ones))
        tcoord = np.hstack((data[:, 2:], ones))

        tc = np.dot(tcoord, H.T)
        error = np.sqrt(np.sum((rcoord - tc)**2, axis=1))

        # TODO: Should customise this pixel threshold
        return error, error < (1 - confidence) * 50

    def estimate(self, data):
        H, ignored = self.estimate_direct(data)
        return H, True

    def _data_from_array(self,data):
        data = np.asarray(data)
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

        U = np.zeros((2*nr,8),dtype=ftype)
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

        B = np.concatenate((rx,ry))[:,np.newaxis]

        M,res,rank,s = scipy.linalg.lstsq(U,B)

        return np.append(M,1).reshape((3,3)),True

    def _build_transform_from_params(self,p):
            theta,tx,ty,s = p
            return np.array([[s*np.cos(theta),-s*np.sin(theta),tx],
                            [s*np.sin(theta), s*np.cos(theta),ty],
                            [0,              0,             1.]])

    def estimate_iterative(self,data):
        rx,ry,tx,ty = self._data_from_array(data)

        rcoord = np.vstack((rx,ry,np.ones_like(rx))).T
        tcoord = np.vstack((tx,ty,np.ones_like(tx))).T

        def err_func(p):
            err,inlier = self(data,
                              H=self._build_transform_from_params(p))
            return err

        pout,ignore,ignore,mesg,ier = sp.optimize.leastsq(err_func,
                                                          [0,0,0,1],
                                                          maxfev=5000,
                                                          full_output=True)
        if ier != 1 and ier != 2:
            print "Warning: error status", ier
            print mesg
        return self._build_transform_from_params(pout),(ier==1)


class PointCorrespondence(object):
    """Estimate point correspondence homographies."""

    def __init__(self, ref_feat_rows, ref_feat_cols,
                 target_feat_rows, target_feat_cols,
                 **args):

        self.data = np.dstack([ref_feat_cols,ref_feat_rows,
                               target_feat_cols,target_feat_rows]).squeeze()

        self.mode = args.get('mode', 'direct').lower()
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
        R = RANSAC.RANSAC(M, p_inlier=0.1) # conservatively low
        return R(self.data,
                 inliers_required=self.args.get('inliers_required',
                                                len(self.data)/2),
                 confidence=self.args.get('confidence', None))

def sparse(ref_feat_rows, ref_feat_cols,
           target_feat_rows, target_feat_cols, **kwargs):
    """Compatibility wrapper. Calculate the PointCorrespondence
    homography which maps reference features to target features.

    See also: PointCorrespondence

    Parameters
    ----------
    ref_feat_rows, ref_feat_cols : array of floats
        Coordinates in the reference image.
    target_feat_rows, target_feat_cols : array of floats
        Coordinates in the target image.
    mode : {'direct', 'iterative', 'RANSAC'}, optional
        Method used to estimate the correspondences.  See also
        ``PointCorrespondence``.

    Other Parameters
    ----------------
    confidence : float
        Passed to RANSAC.
    inliers_required : int
        Number of inliers required for convergence.

    """

    p = PointCorrespondence(ref_feat_rows,ref_feat_cols,
                            target_feat_rows,target_feat_cols,
                            **kwargs)

    M = p.estimate()
    return M

def refine(reference, target, M_ref, M_target):
    """Refine registration parameters iteratively."""
    p = M_target[(0, 0, 0, 1), (0, 1, 2, 2)]
    p = scipy.optimize.fmin_cg(_tf_difference, p,
                               args=(M_ref, reference, target))
    C, S, x, y  = p
    return np.array([[ C, S, x],
                     [-S, C, y],
                     [ 0, 0, 1]])

def _tf_difference(p, M_ref, target, reference):
    """Calculate difference between reference and transformed target."""
    C, S, x, y  = p
    M_target = np.array([[ C, S, x],
                         [-S, C, y],
                         [ 0, 0, 1]])

    im1 = sr.transform.matrix(reference, M_ref)
    im2 = sr.transform.matrix(target, M_target)
    mask = (im1 != 0) & (im2 != 0)
    diff = (im1[mask] - im2[mask])**2
    # TODO: do polygon overlap check

    return diff.sum() / np.sum(mask)

def _build_tf(p):
    if np.sum(np.isnan(p) + np.isinf(p)) != 0:
        return np.eye(3)
    else:
        theta,a,b,tx,ty = p
        C = np.cos(theta)
        S = np.sin(theta)
        return np.array([[a*C,  -a*S, tx],
                         [a*b*S, a*C, ty],
                         [0,     0,   1.]])
