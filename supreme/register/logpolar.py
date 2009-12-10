__all__ = ['logpolar', 'patch_match']

import supreme as sr
import supreme.geometry
import supreme.config

_log = supreme.config.get_log(__name__)

from supreme.config import ftype,itype
from supreme.io import Image

import numpy as np
import scipy.fftpack as fftpack
from itertools import izip
from scipy import ndimage as ndi

import timeit

fft2 = fftpack.fft2
ifft2 = fftpack.ifft2

def patch_match(a, b, angles=360, Rs=None, plot_corr=False):
    """Align two patches, using the log polar transform.

    Parameters
    ----------
    a : ndarray of uint8
        Reference image.
    b : ndarray of uint8
        Target image.
    angles : int
        Number of angles to use in log-polar transform.
    Rs : int
        Number of radial samples used in the log-polar transform.
    plot_corr : bool, optional
        Whether to plot the phase correlation coefficients.

    Returns
    -------
    c : float
        Peak correlation value.
    theta : float
        Estimated rotation angle from `a` to `b`.
    scale : float
        Estimated scaling from `a` to `b`.

    """
    from image import phase_corr
    import supreme.transform as tr

    angles = np.linspace(0, np.pi * 2, angles)
    if Rs is None:
        Rs = max(a.shape[:2])
    A, angles, log_base = tr.logpolar(a, angles=angles, Rs=Rs, extra_info=True)
    B = tr.logpolar(b, angles=angles, Rs=Rs)

    cv = phase_corr(B, A)
    m, n = np.unravel_index(np.argmax(cv), cv.shape)

    if n > Rs/2:
        n = n - Rs # correlation matched, but from the other side

    if plot_corr:
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import axes3d

        fig = plt.figure()

        cv_cut = cv[max(0, m - 30):min(cv.shape[1], m + 30),
                    max(0, n - 30):min(cv.shape[0], n + 30)]

        coords = sr.geometry.Grid(*cv_cut.shape)

        ax3d = axes3d.Axes3D(fig)
        ax3d.plot_wireframe(coords['cols'], coords['rows'], cv_cut)
        ax3d.set_title('Phase correlation around peak\n$\\log(100 + x)$')
        plt.show()

    return cv[m, n], angles[m], np.exp(n * log_base)


def _clearborder(image,border_shape):
    rows,cols = image.shape
    br,bc = border_shape
    image[:br,:] = 0
    image[rows-br:,:] = 0
    image[:,:bc] = 0
    image[:,cols-bc:] = 0
    return image

def _peaks(image,nr,minvar=0):
    """Divide image into nr quadrants and return peak value positions."""
    n = np.ceil(np.sqrt(nr))
    quadrants = _rects(image.shape,n,n)
    peaks = []
    for q in quadrants:
        q_image = image[q.as_slice()]
        q_argmax = q_image.argmax()
        q_maxpos = np.unravel_index(q_argmax,q.shape)
        if q_image.flat[q_argmax] > minvar:
            peaks.append(np.array(q_maxpos) + q.origin)
    return peaks

def rectangle_inside(shape,percent=10):
    """Return a path inside the border as defined by shape."""
    shape = np.asarray(shape)
    rtop = np.round_(shape*percent/100.)
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
    rows = np.linspace(0,rows,divide_rows+1).astype(int)
    cols = np.linspace(0,cols,divide_cols+1).astype(int)

    rects = []
    for r0,r1 in zip(rows[:-1],rows[1:]):
        for c0,c1 in zip(cols[:-1],cols[1:]):
            rects.append(Rect(r0,c0,r1-r0,c1-c0))

    return rects

def _lpt_on_path(image,path,shape, **lp_args):
    """Calculate log polar transforms along a given path."""
    path = list(path)
    cutouts = sr.geometry.cut.along_path(path,image,shape=shape)
    for pos,cut in izip(path,cutouts):
        lpt = sr.transform.logpolar(cut, **lp_args)
        yield (pos,cut,lpt - lpt.mean())

def _lpt_corr(reference_frames,
              frame, descr, path, window_shape, fft_shape,
              angles, log_base,
              **lpt_args):
    try:
        max_corr_sofar = descr['source'].info['variance']
    except:
        max_corr_sofar = 0
    corr_vals = []
    for pos,cut,lpt in _lpt_on_path(frame,path,window_shape,
                                    **lpt_args):
        # prepare correlation FFT
        X = fft2(lpt)

        for rf in reference_frames:
            # Phase correlation
            corr = rf['fft'] * X.conj()
            corr /= np.abs(corr)
            corr = np.abs(ifft2(corr))

            corr_max_arg = corr.argmax()
            corr_max = corr.flat[corr_max_arg]
            corr_vals.append(corr_max)

            if corr_max_arg != 0 and corr_max > max_corr_sofar:
                rotation, scale = np.unravel_index(corr_max_arg, fft_shape)
                if scale > X.shape[1]/2:
                    scale = scale - X.shape[1]/2 # correlation matched,
                                                 # but from the other side

                rotation = angles[rotation]
                scale = np.exp(scale * log_base)

                max_corr_sofar = corr_max

                descr.update({'source': Image(cut,
                                              info={'variance': max_corr_sofar,
                                                    'position': pos,
                                                    'rotation': rotation,
                                                    'scale': scale,
                                                    'reference': rf}),
                            'lpt': lpt,
                            'fft': X,
                            'frame': frame})
    return corr_vals


def logpolar(ref_img,img_list,window_shape=None,angles=181,
             variance_threshold=0.09,peak_thresh=5):
    """Register the given images using log polar transforms.

    Output:
    -------
    accepted : bool array
        For each of the input frames, return whether the image could be used.

    Hs : list of (3,3) floating point arrays
        For each of the input frames, the homography H that maps
        the frame to the reference image.

    """
    assert ref_img.ndim == 2, "Images must be 2-dimensional arrays"

    for img in img_list:
        assert ref_img.shape == img.shape

    if window_shape is None:
        window_shape = np.array(img.shape,dtype=int)/5 + 1
        window_shape[window_shape < 21] = 21
    else:
        window_shape = np.asarray(window_shape,dtype=int)

    # Pre-calculate coordinates for log-polar transforms
    angle_samples = np.linspace(0, 2*np.pi, angles)
    w = max(window_shape[:2])/2
    cr, cc, angle_samples, log_base = \
                          sr.transform.transform._lpcoords(
        np.append(window_shape, 1), w, angles=angle_samples)

    lpt_args = {'_coords_r': cr,
                '_coords_c': cc,
                'mode': 'W'}

    # Divide reference frame into 4 quadrants and calculate log-polar
    # transforms at points of maximum variance.

    # High-pass filter

    def _prepare_varmap(ref_img):
        vm_filter_mask = [[0,  1, 0],
                          [1, -2, 1],
                          [0,  1, 0]]

        #vmsource = ndi.correlate(ref_img,vm_filter_mask)
        vmsource = ref_img - ndi.sobel(ref_img)
#        vm = ndi.gaussian_filter(ref_img, 2) - ndi.gaussian_filter(ref_img, 1)
        vm = sr.ext.variance_map(vmsource,shape=window_shape/8)
        vm = vm/np.prod(window_shape/4)
        vm = _clearborder(vm,window_shape/2)
        return vm

    vm = _prepare_varmap(ref_img)

##     import pylab as P
##     P.subplot(121)
##     P.imshow(ref_img,cmap=P.cm.gray)
##     P.axis('off')
##     P.subplot(122)
##     P.imshow(vm)
##     P.rcParams['figure.figsize'] = (6.67,3.335)
##     P.axis('off')
##     P.savefig('varmap.eps')
##     P.show()

    # 'reference' stores image sequences.  Each sequence contains
    # original slice, slice log polar transform and DFT of slice LPT
    reference_frames = []
    ref_pos = _peaks(vm,12,peak_thresh)
    assert len(ref_pos) > 0, "Could not find suitable reference position."
    ref_var = [vm[tuple(p)] for p in ref_pos]
    for pos,original,lpt in _lpt_on_path(ref_img,ref_pos,window_shape,**lpt_args):
        reference_frames.append({'source':Image(original,info={'position':pos,
                                                               'maxcor':0}),
                                 'lpt': lpt})

    # Calculate Fourier transforms of reference log-polar transforms.
    fft_shape = (angles,w)
    for frame in reference_frames:
        frame['fft'] = fft2(frame['lpt'])

    best_matched_frame = [{} for i in xrange(len(img_list))]
    _log.info("Performing log polar transforms and correlations...")
    for fnum,frame in enumerate(img_list):
        _log.info("Matching frame %d..." % fnum)
        tic = timeit.time.time()
        bmf = best_matched_frame[fnum]

        vm = _prepare_varmap(frame)

        path = _peaks(vm,40,0.95*min(ref_var))
        _lpt_corr(reference_frames,frame,bmf,path,window_shape,fft_shape,
                  angle_samples, log_base, **lpt_args)

        toc = timeit.time.time()
        _log.info("Frame registration completed in %.2f seconds." % (toc-tic))

    def _lpt_peak(pos,frame,bmf,window_shape,fft_shape):
        corr = _lpt_corr([bmf['source'].info['reference']],
                         frame, bmf, [pos], window_shape,
                         fft_shape, angle_samples, log_base, **lpt_args)
        return corr[0]

    for fnum,frame in enumerate(img_list):
        _log.info("Refining frame %d..." % fnum)
        bmf = best_matched_frame[fnum]
        pos = list(bmf['source'].info['position'])
        path = (np.mgrid[-4:5,-4:5].T + bmf['source'].info['position']).reshape((-1,2))
        _lpt_corr([bmf['source'].info['reference']],frame,bmf,path,window_shape,fft_shape,angle_samples, log_base, **lpt_args)
##        import scipy.optimize
##         scipy.optimize.fmin(_lpt_peak,bmf['source'].info['position'],
##                                args=(frame,bmf,window_shape,fft_shape))


    for fnum,f in enumerate(best_matched_frame):
        info = f['source'].info
        _log.info("[%d] Rotation: %.2f" % (fnum, info['rotation']/np.pi*180))
        _log.info("[%d] Scale: %.2f" % (fnum, info['scale']))

        # experiment: show matches
        ref = f['source'].info['reference']
        panel = np.hstack((ref_img,f['frame']))
        ref_pos = ref['source'].info['position'].copy()
        target_pos = f['source'].info['position'].copy()
        target_pos[0] = ref_img.shape[0] - target_pos[0]
        ref_pos[0] = ref_img.shape[0] - ref_pos[0]
        target_pos += [0,ref_img.shape[1]]

        ## import pylab as P
        ## P.imshow(panel,interpolation='nearest',cmap=P.cm.gray)
        ## P.plot([ref_pos[1],target_pos[1]],[ref_pos[0],target_pos[0]],'r-o')
        ## for rf in reference_frames:
        ##     ref_pos = rf['source'].info['position']
        ##     P.plot([ref_pos[1]],[ref_img.shape[0] - ref_pos[0]],'-wo')
        ## P.rcParams['figure.figsize'] = (3.24,3.24)
        ## P.axis('off')
        ## P.box('off')
        ## P.savefig('features_%d.eps' % fnum)
        ## P.show()
        ## P.close()

    accepted_frames = []
    tf_matrices = []
    for fnum, f in enumerate(best_matched_frame):
        info = f['source'].info
        theta = info['rotation']
        s = info['scale']

        if info['variance'] >= variance_threshold and \
           (s < 1.5 and s > 0.8) and (theta > -np.pi/2 and theta < np.pi/2):
            accepted_frames.append(fnum)
        else:
            continue

        M = np.array([[s*np.cos(theta), -s*np.sin(theta),0],
                     [s*np.sin(theta), s*np.cos(theta),0],
                     [0, 0, 1]])

        ref_p = np.append(info['reference']['source'].info['position'][::-1],1)
        xt, yt = info['position'][::-1]
        M_shift = np.array([[1, 0, -xt],
                            [0, 1, -yt],
                            [0, 0,  1]])

        M = np.dot(np.linalg.inv(M_shift), np.dot(M, M_shift))

        tf_matrices.append(M)

    _log.info('%s frames returned' % len(accepted_frames))

    return accepted_frames,tf_matrices
