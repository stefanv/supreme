"""Perform image registration."""

__all__ = ['PointCorrespondence', 'refine', 'sparse', 'dense_MI']

import numpy as np
import scipy as sp
import scipy.optimize
import scipy.linalg

import sys

import supreme as sr
from supreme.config import ftype
from supreme.feature import RANSAC
from supreme import transform
from parzen import joint_hist, mutual_info

_log = sr.config.get_log(__name__)

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
        error = np.sum((rcoord - tc)**2, axis=1)

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

                ``||x' - Hx'||^2``

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

        M = np.append(M,1).reshape((3,3))
        return M, True

    def _build_transform_from_params(self,p):
            theta,tx,ty,s = p
            return np.array([[s*np.cos(theta), -s*np.sin(theta), tx],
                             [s*np.sin(theta),  s*np.cos(theta), ty],
                             [0,                0,               1.]])

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
        self.RANSAC_mode = args.get('RANSAC_mode', 'direct')

    def estimate(self):
        if self.mode == 'direct':
            return Homography().estimate_direct(self.data)
        elif self.mode == 'iterative':
            return Homography().estimate_iterative(self.data)
        else:
            return self.RANSAC(self.RANSAC_mode)

    def RANSAC(self, mode='direct'):
        """Mode can be 'direct' or 'iterative'.

        """
        M = Homography()
        if mode == 'iterative':
            M.estimate = M.estimate_iterative
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
    RANSAC_mode : {'direct', 'iterative'}, optional
        Whether RANSAC should estimates homographies directly
        or iteratively.

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

def _build_tf(p, translation_only=False, fixed_scale=False):
    if np.sum(np.isnan(p) + np.isinf(p)) != 0:
        H = np.eye(3)
    else:
        theta,a,b,tx,ty = p
        if translation_only:
            theta = 0
            a = b = 1
        if fixed_scale:
            a = b = 1

        C = np.cos(theta)
        S = np.sin(theta)

        H = np.array([[a*C,  -b*S, tx],
                      [a*S,   b*C, ty],
                      [0,     0,   1.]])
        if translation_only:
            H[:2, :2] = np.eye(2)

    return H

def dense_MI(A, B, p=None, levels=3, fast=False, std=1, win_size=5,
             translation_only=False, fixed_scale=False):
    """Register image B to A, using mutual information and an image pyramid.

    Parameters
    ----------
    A, B : ndarray of uint
        Images to register.
    levels : int
        Number of levels in the image pyramid.  Each level is downsampled
        by 2.
    p : list of floats, optional
        The five initial parameters passed to the optimiser.  These are
        rotation angle, skew in the X direction, skew in the Y direction,
        translation in x and translation in y.
    fast : bool
        If true, the histogram is not smoothed.
    std : float
        Standard deviation used by the smoothing window.
    win_size : int (odd)
        Window size of the smoother.
    translation_only : bool
        Whether to use a translation-only motion model.  By default,
        a full homography is estimated.
    fixed_scale : bool
        Limit the scale of the motion model to 1.

    Returns
    -------
    M : (3,3) ndarray of float
        Transformation matrix that transforms B to A.

    """
    def cost(p, A, B):
        M = _build_tf(p, translation_only=translation_only,
                         fixed_scale=fixed_scale)
        try:
            T = transform.homography(B, M, order=2)
        except np.linalg.LinAlgError:
            raise RuntimeError('Could not invert transformation matrix. '
                               'This may be because too many levels of '
                               'downscaling was requested (%d).' % levels)
        H = joint_hist(A, T, win_size=win_size, std=std, fast=fast)
        S = mutual_info(H)
        return -S

    if p is None:
        p = [0, 1, 1, 0, 0]
    for z in range(levels - 1, -2, -1):
        p = [p[0], p[1], p[2], 2*p[3], 2*p[4]]
        _log.info("Zoom factor: %f" % (1/2.**z))
        A_ = scipy.ndimage.zoom(A, 1/2.**z, order=2)
        B_ = scipy.ndimage.zoom(B, 1/2.**z, order=2)

        p, fopt, direc, iter, funcalls, warnflag = \
          scipy.optimize.fmin_powell(cost, p, args=(A_, B_), full_output=True)

    p = [p[0], p[1], p[2], p[3]/2, p[4]/2]

    return _build_tf(p, translation_only=translation_only), -fopt
