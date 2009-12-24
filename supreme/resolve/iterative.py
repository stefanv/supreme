__all__ = ['default_camera', 'cost_squared_error', 'iresolve',
           'initial_guess_avg', 'cost_prior_xsq']

import numpy as np
import scipy.optimize as opt
from supreme.register import stack
from supreme.transform import homography
from supreme.transform.transform import _homography_coords

import supreme.config
log = supreme.config.get_log(__name__)

import time

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
        H[:2, :] *= scale

    return stack.with_transform(images, HH, oshape=oshape)

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
        H[:2, :] *= scale
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

    oshape = [int(i) for i in np.array(images[0].shape) * scale]

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
##             import matplotlib.pyplot as plt
##             plt.subplot(1,3,1)
##             plt.imshow(LR, cmap=plt.cm.gray)
##             plt.subplot(1,3,2)
##             plt.imshow(LR_est, cmap=plt.cm.gray)
##             plt.subplot(1,3,3)
##             plt.imshow(LR-LR_est)
##             plt.show()

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
