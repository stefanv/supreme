__all__ = ['solve', 'default_camera', 'cost_squared_error', 'iresolve',
           'initial_guess_avg', 'cost_prior_xsq']

import numpy as np
import scipy.optimize as opt
import scipy.ndimage as ndi
import scipy.sparse as sparse

from supreme.register import stack
from supreme.transform import homography
from supreme.transform.transform import _homography_coords
from supreme.geometry.window import gauss

import supreme.config
log = supreme.config.get_log(__name__)

from lsqr import lsqr
from operators import bilinear, convolve, op_stack
from supreme.ext import poly_interp_op

import time

def solve(images, tf_matrices, scale, x0=None,
          tol=1e-10, iter_lim=None, damp=1e-1,
          method='CG', operator='bilinear'):
    """Super-resolve a set of low-resolution images by solving
    a large, sparse set of linear equations.

    This method approximates the camera with a downsampling operator,
    using bilinear interpolation.  The LSQR method is used to solve
    the equation :math:`A\mathbf{x} = b` where :math:`A` is the
    downsampling operator, :math:`\mathbf{x}` is the high-resolution
    estimate (flattened in raster scan or lexicographic order), and
    :math:`\mathbf{b}` is a stacked vector of all the low-resolution
    images.

    Parameters
    ----------
    images : list of ndarrays
        Low-resolution input frames.
    tf_matrices : list of (3, 3) ndarrays
        Transformation matrices that relate all low-resolution frames
        to a reference low-resolution frame (usually ``images[0]``).
    scale : float
        The resolution of the output image is `scale` times the resolution
        of the input images.
    x0 : ndarray, optional
        Initial guess of HR image.
    damp : float, optional
        If an initial guess is provided, `damp` specifies how much that
        estimate is weighed in the entire process.  A larger value of
        `damp` results in a solution closer to `x0`, whereas a smaller
        version of `damp` yields a solution closer to the solution
        obtained without any initial estimate.
    method : {'CG', 'LSQR', 'descent'}
        Whether to use conjugate gradients, least-squares or gradient descent
        to determine the solution.
    operator : {'bilinear', 'polygon'}
        The camera model is approximated as an interpolation process.  The
        polygon interpolation operator works well for zoom ratios < 2.

    Returns
    -------
    HR : ndarray
        High-resolution estimate.

    """
    assert len(images) == len(tf_matrices)

    HH = [H.copy() for H in tf_matrices]
    HH_scaled = []
    scale = float(scale)
    for H in HH:
        HS = np.array([[scale, 0,         0],
                       [0,       scale,   0],
                       [0,       0,       1]])

        HH_scaled.append(np.linalg.inv(np.dot(HS, H)))

    HH = HH_scaled

    oshape = np.floor(np.array(images[0].shape) * scale)
    LR_shape = images[0].shape

    print "Constructing camera operator (%s)..." % operator
    if operator == 'bilinear':
        op = bilinear(oshape[0], oshape[1], HH, *LR_shape, boundary=0)
    elif operator == 'polygon':
        sub_ops = []
        for H in HH:
            sub_ops.append(poly_interp_op(oshape[0], oshape[1],
                                          H, *LR_shape,
                                          search_win=round(scale) * 2 + 1))
        op = sparse.vstack(sub_ops, format='csr')
    else:
        raise ValueError('Invalid operator requested (%s).' % operator)

##  Visualise mapping of frames
##
##     import matplotlib.pyplot as plt
##     P = np.prod(LR_shape)
##     img = (op * x0.flat).reshape(LR_shape)
##     plt.subplot(1, 4, 1)
##     plt.imshow(x0, cmap=plt.cm.gray)
##     plt.title('x0')
##     plt.subplot(1, 4, 2)
##     plt.imshow(images[0], cmap=plt.cm.gray)
##     plt.title('LR frame')
##     plt.subplot(1, 4, 3)
##     plt.imshow(img, cmap=plt.cm.gray)
##     plt.title('LR image Ax0')
##     plt.subplot(1, 4, 4)
##     plt.imshow(images[0] - img, cmap=plt.cm.gray)
##     plt.title('diff images[0] - Ax')
##     plt.show()

    def A(x, m, n):
        return op * x

    def AT(x, m, n):
        return op.T * x

    k = len(images)
    M = np.prod(LR_shape)
    b = np.empty(k * M)
    for i in range(k):
        b[i * M:(i + 1) * M] = images[i].flat

    atol = btol = conlim = tol
    show = True

    def sr_func(x):
        return np.linalg.norm(op * x - b) ** 2 + \
               damp * np.linalg.norm(x - x0.flat) ** 2

    def sr_gradient(x):
        # Careful! Mixture of sparse and dense operators.
        #Axb = op * x - b
        #nrm_sq = np.dot(Axb, Axb) # Dense
        #Axbop = (op.T * Axb).T # Sparse
        #return nrm_sq * Axbop
        Axb = op * x - b
        return 2 * ((Axb.T * op) + damp * (x - x0.flat))

    print "Super resolving..."

## Conjugate Gradient Optimisation
    if method == 'CG':

        x, fopt, f_calls, gcalls, warnflag = \
           opt.fmin_cg(sr_func, x0, fprime=sr_gradient, gtol=0,
                       disp=True, maxiter=iter_lim, full_output=True)

    elif method == 'LSQR':

## LSQR Optimisation
##
        x0 = x0.flat
        b = b - op * x0
        x, istop, itn, r1norm, r2norm, anorm, acond, arnorm, xnorm, var = \
          lsqr(A, AT, np.prod(oshape), b, atol=atol, btol=btol,
               conlim=conlim, damp=damp, show=show, iter_lim=iter_lim)
        x = x0 + x

    elif method == 'descent':

## Steepest Descent Optimisation
##
        x = np.array(x0, copy=True).reshape(np.prod(x0.shape))
        for i in range(50):
            print "Gradient descent step %d" % i
            x += damp * (op.T * (b - (op * x)))

    else:
        raise ValueError('Invalid method (%s) specified.' % method)

    return x.reshape(oshape)

def initial_guess_avg(images, tf_matrices, scale, oshape):
    """From the given low-resolution images and transforms, make an
    initial guess of the high-resolution image.

    Parameters
    ----------
    images : list of ndarray
        Low-resolution images.
    tf_matrices : list of (3, 3) ndarray
        Transformation matrices that warp the images to the reference
        image (usually ``images[0]``).
    scale : float
        The scale of the high-resolution reconstruction relative to the
        low-resolution frames.  Typically between 1 and 2.
    oshape : tuple of int
        Shape of the high-resolution reconstruction.

    """
    HH = [x.copy() for x in tf_matrices]
    for H in HH:
        H[:2, :] *= float(scale)

    return stack.with_transform(images, HH, oshape=oshape, order=3)

def default_camera(img_nr, img, H, scale, oshape, std=1.0, _coords=[]):
    """The default camera model simply blurs and downscales the image.

    Parameters
    ----------
    img_nr : int
        The number of this image in the set.  Useful for storing image-specific
        parameters, such as coordinates.
    img : ndarray
        High-resolution image data.
    H : (3,3) ndarray
        Transformation matrix to apply to `img`.
    oshape : tuple of ints
        Output shape.
    std : float
        Standard deviation of the blur mask.
    _coords : ndarray
        Coordinates suitable for use in ``ndimage.map_coordinates``.

    """
    try:
        coords = _coords[img_nr]
    except IndexError:
        H = H.copy()
        H[:2, :] *= float(scale)
        H = np.linalg.inv(H)

        coords = _homography_coords(img, H, oshape)
        _coords.append(coords)

    out = homography(img, H, _coords=coords)
    out = out[:oshape[0], :oshape[1]]
    return out

def cost_squared_error(nr, x, y, HR, HR_avg):
    return np.sum((x - y)**2)

def cost_prior_xsq(nr, x, y, HR, HR_avg, lam=0.01):
    return lam * np.sum(np.sqrt((HR - HR_avg)**2)) + \
           np.sum(np.sqrt((x - y)**2))

def iresolve(images, tf_matrices, scale=1.3,
             initial_guess=initial_guess_avg, initial_guess_args={},
             camera=None, camera_args={},
             cost_measure=None, cost_args={}):
    """Super-resolve a set of low-resolution images.

    Parameters
    ----------
    images : list of ndarrays
        Low-resolution input frames.
    tf_matrices : list of (3, 3) ndarrays
        List of transformation matrices to transform each
        low-resolution frame to a reference image (typically,
        ``images[0]``).
    scale : float
        Resolution improvement required.
    initial_guess : callable, f(imgs, Hs, scale, oshape, **initial_guess_args)
        Function that calculates an initial estimate of the high-resolution
        image for initialising the iterative process.  If not specified,
        ``initial_guess_avg`` is used.  See ``initial_guess_avg`` for
        more information.
    initial_guess_args : dict, optional
        Optional keyword arguments for `initial_guess`.
    camera : callable, f(nr, img, H, scale, oshape, **camera_args), optional
        Function that emulates the effect of the camera on a
        high-resolution frame.  See the docstring of ``default_camera``
        for more detail.  If not specified, ``default_camera`` is used.
    camera_args : dict, optional
        Optional keyword arguments for `camera`.
    cost_measure : callable, f(nr, x, y, **cost_args)
        Function that calculates the difference between two
        low-resolution frames.  If not specified, ``cost_squared_error``
        is used.
    cost_args : dict, optional
        Optional keyword arguments for `cost_measure`.

    Returns
    -------
    out : ndarray
        Super-resolved image.

    """
    if camera is None:
        camera = default_camera

    if cost_measure is None:
        cost_measure = cost_squared_error

    oshape = [int(i) for i in np.array(images[0].shape) * float(scale)]

    HR = initial_guess(images, tf_matrices, scale=scale,
                       oshape=oshape, **initial_guess_args)

    HR_guess = HR.copy()

    def sr_func(HR, it=[0]):
        if it[0] % 100 == 0:
            log.info('Saving output for function call %d' % it[0])
            np.save('HR', HR.reshape(oshape))

        it[0] += 1
        err = 0
        save_shape = HR.shape
        HR.shape = oshape
        for i, (H, LR) in enumerate(zip(tf_matrices, images)):
            LR_est = camera(i, HR, H, scale, images[0].shape, **camera_args)

            err += cost_measure(i, LR, LR_est, HR, HR_guess, **cost_args)

        HR.shape = save_shape

        return err

    def callback(x, it=[1]):
        it[0] += 1

        log.info('Iteration #%d' % it[0])

    tic = time.time()
    log.info('Starting optimisation. This may take a long time (hour).')
    HR = opt.fmin_cg(sr_func, HR, callback=callback, maxiter=5)
    toc = time.time()

    log.info('Operation took %.2f seconds' % (toc - tic))

    return HR.reshape(oshape)
