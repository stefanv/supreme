"""Perform image registration."""

__all__ = ['PointCorrespondence','refine','sparse']

import numpy as N
import scipy as S
import scipy.optimize
import scipy.linalg

from numpy.testing import set_local_path, restore_path

import sys
from itertools import izip
import timeit
import warnings

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

def rectangle_inside(shape,percent=10):
    """Return a path inside the border as defined by shape."""
    shape = N.asarray(shape)
    rtop = N.round_(shape*percent/100.)
    rbottom = shape - rtop

    cp = sr.geometry.coord_path
    return cp.build(cp.rectangle(rtop,rbottom))

def _rects(shape,divide_rows,divide_cols):
    class Rect:
        def __init__(self,top_r,top_c,height,width):
            self.top_r = top_r
            self.top_c = top_c
            self.width = width
            self.height = height

        @property
        def origin(self):
            return (self.top_r,self.top_c)

        @property
        def shape(self):
            return (int(self.height),int(self.width))

        @property
        def coords(self):
            """x- and y-coordinates, rather than row/column"""
            return (self.top_c,self.top_c,
                    self.top_c+self.width,self.top_c+self.width),\
                    (self.top_r,self.top_r+self.height,
                     self.top_r+self.height,self.top_r)

        def as_slice(self):
            return [slice(self.top_r,self.top_r+self.height),
                    slice(self.top_c,self.top_c+self.width)]

        def __str__(self):
            return "Rectangle: (%d,%d), height: %d, width: %d" % \
                   (self.top_r,self.top_c,self.height,self.width)

    rows,cols = shape
    rows = N.linspace(0,rows,divide_rows+1).astype(int)
    cols = N.linspace(0,cols,divide_cols+1).astype(int)

    rects = []
    for r0,r1 in zip(rows[:-1],rows[1:]):
        for c0,c1 in zip(cols[:-1],cols[1:]):
            rects.append(Rect(r0,c0,r1-r0,c1-c0))

    return rects

def _peaks(image,nr,minvar=0):
    """Divide image into nr quadrants and return peak value positions."""
    n = N.ceil(N.sqrt(nr))
    quadrants = _rects(image.shape,n,n)
    peaks = []
    for q in quadrants:
        q_image = image[q.as_slice()]
        q_argmax = q_image.argmax()
        q_maxpos = N.unravel_index(q_argmax,q.shape)
        if q_image.flat[q_argmax] > minvar:
            peaks.append(N.array(q_maxpos) + q.origin)
    return peaks

def _clearborder(image,border_shape):
    rows,cols = image.shape
    br,bc = border_shape
    image[:br,:] = 0
    image[rows-br:,:] = 0
    image[:,:bc] = 0
    image[:,cols-bc:] = 0
    return image

class ImageInfo(N.ndarray):
    """Description wrapper around ndarray"""
    def __new__(image_cls,arr,info={}):
        x = N.array(arr).view(image_cls)
        x.info = info
        return x
    def __array_finalize__(self, obj):
        if hasattr(obj,'info'):
            self.info = obj.info
        return

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
