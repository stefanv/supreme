"""Perform image registration."""

__all__ = ['logpolar','phase_correlation']

import numpy as N
import scipy as S
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

def _peaks(image,nr):
    n = N.ceil(N.sqrt(nr))
    quadrants = _rects(image.shape,n,n)
    peaks = []
    for q in quadrants:
        q_maxarg = N.unravel_index(image[q.as_slice()].argmax(),q.shape)
        peaks.append(N.array(q_maxarg) + q.origin)
    return peaks

class ImageInfo(N.ndarray):
    """Description wrapper around ndarray"""
    def __new__(image_cls,arr,info={}):
        image_cls.info = info
        return N.array(arr).view(image_cls)
            
def logpolar(ref_img,img_list,window_shape=(65,65),angles=180):
    """Register the given images using log polar transforms.

    The output is a list of 3x3 arrays.
    
    """
    assert ref_img.ndim == 2, "Images must be 2-dimensional arrays"

    for img in img_list:
        assert ref_img.shape == img.shape

    window_shape = N.array(window_shape)

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

    # Divide reference frame into 4 quadrants and calculate log-polar
    # transforms at points of maximum variance.
    vm = SR.ext.variance_map(ref_img,shape=window_shape/4)

    # 'reference' stores image sequences.  Each sequence contains
    # original slice, slice log polar transform and DFT of slice LPT
    reference_frames = []
    for pos,original,lpt in lpt_on_path(ref_img,_peaks(vm,4),window_shape):
        reference_frames.append({'source':ImageInfo(original,{'pos':pos}),
                                 'lpt': lpt})

    # Calculate Fourier transforms of reference log-polar transforms.
    fft_shape = (angles,window_shape[1]*2-1)
    for frame in reference_frames:
        frame['fft'] = fft2(frame['lpt'][::-1,::-1],fft_shape)

    best_matched_frame = [{}]*len(img_list)
    for fnum,frame in enumerate(img_list):
        tic = timeit.time.time()
        
        print "Calculate variance map for image #", fnum
        vm = SR.ext.variance_map(frame,shape=window_shape/4)

        print "Performing log polar transforms and correlations..."        

        for pos_x,cut,lpt_x in lpt_on_path(frame,_peaks(vm,40),window_shape):
            import pylab as P
            # prepare correlation FFT
            X = fft2(lpt_x,fft_shape)
            for rf in reference_frames:
                corr = abs(ifft2(X*rf['fft']))
                corr /= N.sqrt((lpt_x**2).sum()*(rf['lpt']**2).sum())
                corr_max_arg = corr.argmax()

                bmf = best_matched_frame[fnum]
                if bmf.has_key('source'):
                    max_corr_sofar = bmf['source'].info['variance']
                else:
                    max_corr_sofar = 0

                print max_corr_sofar
                if corr.flat[corr_max_arg] > max_corr_sofar:
                    rotation,scale = N.unravel_index(corr_max_arg,fft_shape)
                    bmf.update({'source': ImageInfo(cut,
                                          {'variance': corr.flat[corr_max_arg],
                                           'position': pos_x,
                                           'rotation': rotation,
                                           'scale': scale,
                                           'reference': rf}),
                                'lpt': lpt_x,
                                'fft': X})

        toc = timeit.time.time()
        print "Registration completed in %.2f seconds.\n" % (toc-tic)

    for f in best_matched_frame:
        import pylab as P
        P.subplot(121)
        P.imshow(f['source'].info['reference']['source'])
        ws = [[c] for c in window_shape[::-1]/2]
        P.plot(ws[0],ws[1],'o')
        P.subplot(122)
        P.imshow(f['source'])
        P.plot(ws[0],ws[1],'o')        
        P.show()

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
    
