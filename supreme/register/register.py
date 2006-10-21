"""Perform image registration."""

__all__ = ['logpolar','phase_correlation','refine']

import numpy as N
import scipy as S
from scipy import ndimage as ndi
import scipy.optimize
fft2 = S.fftpack.fft2
ifft2 = S.fftpack.ifft2

from numpy.testing import set_local_path, restore_path

import sys
from itertools import izip
import timeit

set_local_path('../../..')
from supreme.config import ftype,itype
import supreme as SR
restore_path()

def rectangle_inside(shape,percent=10):
    """Return a path inside the border defined by shape."""
    shape = N.asarray(shape)
    rtop = N.round_(shape*percent/100.)
    rbottom = shape - rtop

    cp = SR.geometry.coord_path
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
            
def logpolar(ref_img,img_list,window_shape=None,angles=180):
    """Register the given images using log polar transforms.

    The output is a list of 3x3 arrays.
    
    """
    assert ref_img.ndim == 2, "Images must be 2-dimensional arrays"

    for img in img_list:
        assert ref_img.shape == img.shape

    window_shape = N.array(img.shape,dtype=int)/5 + 1

    # Pre-calculate coordinates for log-polar transforms
    angle_samples = N.linspace(-N.pi/2,N.pi/2,angles)
    cr,cc = SR.transform.transform._lpcoords(N.append(window_shape,1),
                                             max(window_shape[:2]),
                                             angles=angle_samples)

    def lpt_on_path(image,path,shape):
        """Calculate log polar transforms along a given path."""
        path = list(path)
        cutouts = SR.geometry.cut.along_path(path,image,shape=shape)
        for pos,cut in izip(path,cutouts):
            lpt = SR.transform.logpolar(cut,_coords_r=cr,_coords_c=cc)
            yield (pos,cut,lpt - lpt.mean())

    def lpt_corr(reference_frames,frame,descr,path,window_shape,fft_shape):
        try:
            print descr['source'].info['variance'], "<<<"
            max_corr_sofar = descr['source'].info['variance']
        except:
            max_corr_sofar = 0
        for pos,cut,lpt in lpt_on_path(frame,path,window_shape):
            # prepare correlation FFT
            X = fft2(lpt,fft_shape)
            
            for rf in reference_frames:
                corr = abs(ifft2(X*rf['fft']))
                corr /= (N.sqrt((lpt**2).sum()*(rf['lpt']**2).sum()))
                corr_max_arg = corr.argmax()

                if corr.flat[corr_max_arg] > max_corr_sofar:
                    print corr.flat[corr_max_arg]
                    rotation,scale = N.unravel_index(corr_max_arg,fft_shape)
                    rotation = angle_samples[rotation-1] - N.pi/2
                    scale -= fft_shape[1]/2
                    max_corr_sofar = corr.flat[corr_max_arg]
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
                                'fft': X})

    # Divide reference frame into 4 quadrants and calculate log-polar
    # transforms at points of maximum variance.

    # High-pass filter
    vmsource = ndi.correlate(ref_img,[[0,1,0],[1,-1,1],[0,1,0]])
    vm = SR.ext.variance_map(vmsource,shape=window_shape/4)
    vm = vm/vm.max()
    vm = _clearborder(vm,window_shape/2)

    # 'reference' stores image sequences.  Each sequence contains
    # original slice, slice log polar transform and DFT of slice LPT
    reference_frames = []
    ref_pos = _peaks(vm,4,0.2)
    ref_var = [vm[tuple(p)] for p in ref_pos]
    for pos,original,lpt in lpt_on_path(ref_img,ref_pos,window_shape):
        reference_frames.append({'source':ImageInfo(original,{'pos':pos}),
                                 'lpt': lpt})

    # Calculate Fourier transforms of reference log-polar transforms.
    fft_shape = (angles,window_shape[1]*2-1)
    for frame in reference_frames:
        frame['fft'] = fft2(frame['lpt'][::-1,::-1],fft_shape)

    best_matched_frame = [{} for i in xrange(len(img_list))]
    for fnum,frame in enumerate(img_list):
        tic = timeit.time.time()
        bmf = best_matched_frame[fnum]
        
        vmframe = ndi.correlate(frame,[[0,1,0],[1,-1,1],[0,1,0]])        
        vm = SR.ext.variance_map(vmframe,shape=window_shape/4)
        vm = vm/vm.max()
        vm = _clearborder(vm,window_shape/2)

        print "Performing log polar transforms and correlations..."
        path = _peaks(vm,40,0.95*min(ref_var))
        lpt_corr(reference_frames,frame,bmf,path,window_shape,fft_shape)

        toc = timeit.time.time()
        print "Peak correlation was", best_matched_frame[fnum]['source'].info['variance']        
        print "Registration completed in %.2f seconds.\n" % (toc-tic)

    for fnum,frame in enumerate(img_list):
        print "Refining frame %d..." % fnum
        bmf = best_matched_frame[fnum]        
        path = (N.mgrid[-4:5,-4:5].T + bmf['source'].info['position']).reshape((-1,2))
        lpt_corr([bmf['source'].info['reference']],frame,bmf,path,window_shape,fft_shape)

    for fnum,f in enumerate(best_matched_frame):
        info = f['source'].info
        print "Frame #%d" % fnum
        print "Rotation:", info['rotation']/N.pi*180
        print "Scale:", info['scale']
        print "Quality:", info['quality']        
        
##         import pylab as P
##         P.subplot(121)
##         P.imshow(f['source'].info['reference']['source'])
##         ws = [[c] for c in window_shape[::-1]/2]
##         P.plot(ws[0],ws[1],'o')
##         P.subplot(122)
##         P.imshow(f['source'])
##         P.plot(ws[0],ws[1],'o')        
##         P.show()

    accepted_frames = []
    tf_matrices = []
    for fnum,f in enumerate(best_matched_frame):
        info = f['source'].info
        if info['quality'] in ['trusted']:
            accepted_frames.append(fnum)
        else:
            continue
            
        theta = -info['rotation']
        M = N.array([[N.cos(theta),-N.sin(theta),0],
                     [N.sin(theta),N.cos(theta),0],
                     [0,0,1]])

        ref_p = N.append(info['reference']['source'].info['pos'][::-1],1)
        p = N.append(info['position'][::-1],1)

        delta = ref_p - N.dot(p,M.T)
        M[:2,2] += delta[:2]
        tf_matrices.append(M)

    return accepted_frames,tf_matrices

def phase_correlation(img,img_list):
    """Register offset by phase correlation.

    """
    F0 = N.angle(N.fft.fftshift(N.fft.fft2(img)))
    for frame in img_list:
        F1 = N.angle(N.fft.fftshift(N.fft.fft2(frame)))
        Z = N.fft.fft2(F1)*N.fft.fft2(F0)
        ind = N.unravel_index(Z.argmax(),Z.shape)
        print ind
    import pylab as P
    P.subplot(131)
    P.imshow(img)
    P.subplot(132)
    P.imshow(frame)
    P.subplot(133)
    P.imshow(Z/Z.max()*255,cmap=P.cm.gray)
    P.show()
    P.close()
    
def refine(reference,target,tf_matrix):
    """Refine registration parameters iteratively."""
    def _build_tf(p):
        C = N.cos(p[0])
        S = N.sin(p[0])        
        return N.array([[C,-S,p[1]],
                        [S,C,p[1]],
                        [0,0,1]])
    
    def _tf_difference(p,reference,target):
        """Calculate difference between reference and transformed target."""
        tf_matrix = _build_tf(p)
        diff = reference - SR.transform.matrix(target,tf_matrix)
        # TODO: do polygon overlap check
        _clearborder(diff,N.array(diff.shape)/4)
        return N.square(diff).sum()

    theta = N.arccos(tf_matrix[0,0])
    tx = tf_matrix[0,2]
    ty = tf_matrix[1,2]

    p = [theta,tx,ty]
    p = scipy.optimize.fmin_cg(_tf_difference,p,
                               args=(reference,target))
    return _build_tf(p)

