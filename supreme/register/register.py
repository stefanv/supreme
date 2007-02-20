"""Perform image registration."""

__all__ = ['logpolar','refine','sparse']

import numpy as N
import scipy as S
from scipy import ndimage as ndi
import scipy.optimize
import scipy.linalg
fft2 = S.fftpack.fft2
ifft2 = S.fftpack.ifft2

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
                 target_feat_rows, target_feat_cols):
        self.rx,self.ry,self.tx,self.ty = \
                map(N.asarray,[ref_feat_cols,ref_feat_rows,
                               target_feat_cols,target_feat_rows])

        assert len(self.rx) == len(self.ry) == len(self.tx) == len(self.ty), \
               "Equal number of coordinates expected."

    def estimate(self):
        """Estimate the homographic point correspondence.

        Output:
        -------

        A (3,3) array H, describing the point correspondence.

        Input point: x = [[c_0]
                          [c_1]
                          [c_2]]

        Output point: x' = [[c'_0]
                            [c'_1]
                            [c'_2]]

        Input and output points are related by

        x' = Hx

        Given errors in the measurement, H minimises

        |x' - Hx'|

        See Digital Image Warping by George Wolberg, p. 54.

        """

        rx,ry,tx,ty = self.rx,self.ry,self.tx,self.ty

        nr = len(self)

        U = N.zeros((2*nr,8),dtype=ftype)
        U[:nr,0] = tx
        U[:nr,1] = ty
        U[:nr,2] = 1.
        U[:nr,6] = -tx*rx
        U[:nr,7] = -ty*rx

        U[nr:,3] = tx
        U[nr:,4] = ty
        U[nr:,5] = 1.
        U[nr:,6] = -tx*ry
        U[nr:,7] = -ty*ry

        B = N.concatenate((rx,ry))[:,N.newaxis]

        M,res,rank,s = scipy.linalg.lstsq(U,B)

        return N.append(M,1).reshape((3,3))

    def transform(self,M):
        pass

    def reject(self,off_mean=0.8):
        pass

    def __len__(self):
        return len(self.rx)

def sparse(ref_feat_rows,ref_feat_cols,
           target_feat_rows,target_feat_cols):
    p = PointCorrespondence(ref_feat_rows,ref_feat_cols,
                            target_feat_rows,target_feat_cols)

    M = p.estimate()
    return M

def rectangle_inside(shape,percent=10):
    """Return a path inside the border defined by shape."""
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

def logpolar(ref_img,img_list,window_shape=None,angles=180,
             variance_threshold=0.75,peak_thresh=5):
    """Register the given images using log polar transforms.

    The output is a list of 3x3 arrays.

    """
    assert ref_img.ndim == 2, "Images must be 2-dimensional arrays"

    for img in img_list:
        assert ref_img.shape == img.shape

    if window_shape is None:
        window_shape = N.array(img.shape,dtype=int)/5 + 1
        window_shape[window_shape < 21] = 21
    else:
        window_shape = N.asarray(window_shape,dtype=int)

    # Pre-calculate coordinates for log-polar transforms
    angle_samples = N.linspace(0,2*N.pi,angles)
    w = max(window_shape[:2])
    cr,cc = sr.transform.transform._lpcoords(N.append(window_shape,1),
                                             w,angles=angle_samples)

    def lpt_on_path(image,path,shape):
        """Calculate log polar transforms along a given path."""
        path = list(path)
        cutouts = sr.geometry.cut.along_path(path,image,shape=shape)
        for pos,cut in izip(path,cutouts):
            lpt = sr.transform.logpolar(cut,_coords_r=cr,_coords_c=cc,mode='W')
            yield (pos,cut,lpt - lpt.mean())

    def lpt_corr(reference_frames,frame,descr,path,window_shape,fft_shape):
        try:
            max_corr_sofar = descr['source'].info['variance']
        except:
            max_corr_sofar = 0
        corr_vals = []
        for pos,cut,lpt in lpt_on_path(frame,path,window_shape):
            # prepare correlation FFT
            X = fft2(lpt,fft_shape)

            for rf in reference_frames:
                corr = abs(ifft2(X*rf['fft']))
                corr /= (N.sqrt((lpt**2).sum()*(rf['lpt']**2).sum()))
                corr_max_arg = corr.argmax()
                corr_max = corr.flat[corr_max_arg]
                corr_vals.append(corr_max)

                if corr_max > max_corr_sofar:
                    print corr_max
                    rotation,scale = N.unravel_index(corr_max_arg,fft_shape)
                    rotation = angle_samples[rotation]
                    scale -= fft_shape[1]/2
                    max_corr_sofar = corr_max
                    if max_corr_sofar < 0.6:
                        quality = 'rejected'
                    elif max_corr_sofar < 0.7:
                        quality = 'bad'
                    elif max_corr_sofar < 0.8:
                        quality = 'good'
                    elif max_corr_sofar < 0.85:
                        quality = 'stable'
                    else:
                        quality = 'trusted'

                    descr.update({'source': ImageInfo(cut,
                                                    {'variance': max_corr_sofar,
                                                     'position': pos,
                                                     'rotation': rotation,
                                                     'scale': scale,
                                                     'reference': rf,
                                                     'quality': quality}),
                                'lpt': lpt,
                                'fft': X,
                                'frame': frame})
        return corr_vals

    # Divide reference frame into 4 quadrants and calculate log-polar
    # transforms at points of maximum variance.

    # High-pass filter

    def _prepare_varmap(ref_img):
        vm_filter_mask = [[0,  1, 0],
                          [1, -2, 1],
                          [0,  1, 0]]

        vmsource = ndi.correlate(ref_img,vm_filter_mask)
        vm = sr.ext.variance_map(vmsource,shape=window_shape/4)
        vm = vm/N.prod(window_shape/4)
        vm = _clearborder(vm,window_shape/2)
        return vm

    vm = _prepare_varmap(ref_img)

    import pylab as P
    P.subplot(121)
    P.imshow(ref_img,cmap=P.cm.gray)
    P.axis('off')
    P.subplot(122)
    P.imshow(vm)
    P.rcParams['figure.figsize'] = (6.67,3.335)
    P.axis('off')
    P.savefig('varmap.eps')
    P.show()

    # 'reference' stores image sequences.  Each sequence contains
    # original slice, slice log polar transform and DFT of slice LPT
    reference_frames = []
    ref_pos = _peaks(vm,12,peak_thresh)
    assert len(ref_pos) > 0, "Could not find suitable reference position."
    ref_var = [vm[tuple(p)] for p in ref_pos]
    for pos,original,lpt in lpt_on_path(ref_img,ref_pos,window_shape):
        reference_frames.append({'source':ImageInfo(original,{'position':pos,
                                                              'maxcor':0}),
                                 'lpt': lpt})

    # Calculate Fourier transforms of reference log-polar transforms.
    fft_shape = (angles,w*2-1)
    for frame in reference_frames:
        frame['fft'] = fft2(frame['lpt'][::-1,::-1],fft_shape)

    best_matched_frame = [{} for i in xrange(len(img_list))]
    for fnum,frame in enumerate(img_list):
        print "Matching frame ", fnum
        tic = timeit.time.time()
        bmf = best_matched_frame[fnum]

        vm = _prepare_varmap(frame)

        print "Performing log polar transforms and correlations..."
        path = _peaks(vm,40,0.95*min(ref_var))
        lpt_corr(reference_frames,frame,bmf,path,window_shape,fft_shape)

        toc = timeit.time.time()
        print "Peak correlation was", best_matched_frame[fnum]['source'].info['variance']
        print "Registration completed in %.2f seconds.\n" % (toc-tic)

    def _lpt_peak(pos,frame,bmf,window_shape,fft_shape):
        corr = lpt_corr([bmf['source'].info['reference']],frame,bmf,[pos],window_shape,fft_shape)
        return corr[0]

    for fnum,frame in enumerate(img_list):
        print "Refining frame %d..." % fnum
        bmf = best_matched_frame[fnum]
#        pos = list(bmf['source'].info['position'])
#        scipy.optimize.fmin_cg(_lpt_peak,bmf['source'].info['position'],
#                               args=(frame,bmf,window_shape,fft_shape))
        path = (N.mgrid[-4:5,-4:5].T + bmf['source'].info['position']).reshape((-1,2))
        lpt_corr([bmf['source'].info['reference']],frame,bmf,path,window_shape,fft_shape)

    for fnum,f in enumerate(best_matched_frame):
        info = f['source'].info
        print "Frame #%d" % fnum
        print "Rotation:", info['rotation']/N.pi*180
        print "Scale:", info['scale']
        print "Quality:", info['quality']

        # experiment: show matches
        import pylab as P
        ref = f['source'].info['reference']
        panel = N.hstack((ref_img,f['frame']))
        ref_pos = ref['source'].info['position'].copy()
        target_pos = f['source'].info['position'].copy()
        target_pos[0] = ref_img.shape[0] - target_pos[0]
        ref_pos[0] = ref_img.shape[0] - ref_pos[0]
        target_pos += [0,ref_img.shape[1]]
        P.imshow(panel,interpolation='nearest',cmap=P.cm.gray)
        P.plot([ref_pos[1],target_pos[1]],[ref_pos[0],target_pos[0]],'r-o')
        for rf in reference_frames:
            ref_pos = rf['source'].info['position']
            P.plot([ref_pos[1]],[ref_img.shape[0] - ref_pos[0]],'-wo')
        P.rcParams['figure.figsize'] = (3.24,3.24)
        P.axis('off')
        P.box('off')
        P.savefig('features_%d.eps' % fnum)
        P.show()

    accepted_frames = []
    tf_matrices = []
    for fnum,f in enumerate(best_matched_frame):
        info = f['source'].info
        if info['variance'] >= variance_threshold:
            accepted_frames.append(fnum)
        else:
            continue

        theta = -info['rotation']
        M = N.array([[N.cos(theta),-N.sin(theta),0],
                     [N.sin(theta),N.cos(theta),0],
                     [0,0,1]])

        ref_p = N.append(info['reference']['source'].info['position'][::-1],1)
        p = N.append(info['position'][::-1],1)

        delta = ref_p - N.dot(p,M.T)
        M[:2,2] += delta[:2]
        tf_matrices.append(M)

    return accepted_frames,tf_matrices

def _tf_difference(M_target,M_ref,target,reference):
    """Calculate difference between reference and transformed target."""
    M_target[[6,7]] = 0
    M_target[8] = 1
    M_ref[[6,7]] = 0
    M_ref[8] = 1
    im1 = sr.transform.matrix(reference,M_ref.reshape((3,3)))
    im2 = sr.transform.matrix(target,M_target.reshape((3,3)))
    diff = ((im1 - im2)**2)[20:-20,20:-20]
    # TODO: do polygon overlap check
    return diff.sum()

def _build_tf(p):
    if N.sum(N.isnan(p) + N.isinf(p)) != 0:
        return N.eye(3)
    else:
        theta,a,b,tx,ty = p
        C = N.cos(theta)
        S = N.sin(theta)
        return N.array([[a*C, -a*S, tx],
                        [a*b*S, a*C, ty],
                        [0,0,1.]])

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
