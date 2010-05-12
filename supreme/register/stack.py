"""
Stack warped images.
"""

import numpy as np
from scipy import ndimage as ndi

import supreme.config as sc
from supreme import transform
from supreme.geometry import Grid, Polygon
from supreme.ext import interp_transf_polygon

import supreme
log = supreme.config.get_log(__name__)

__all__ = ['with_transform', 'mask_roi', 'corners']

def corners(dims):
    """Return the corner coordinates for a matrix of the given
    dimensions."""

    dims = np.array(dims)
    L = len(dims)
    corners = np.empty((2**L, L), dtype=dims.dtype)
    zeros = dims.copy() * 0
    for i in range(2**L):
        bin = list(np.binary_repr(i).zfill(L))
        mask = np.array(bin).astype(np.bool8)
        corners[i] = np.where(mask, dims - 1, zeros)
    return corners

def _tf_corners(rows, cols, M):
    """Transform the corner-coordinates of a (rows, cols)-shaped array,
    using the matrix M.

    Parameters
    ----------
    rows, cols : int
        Dimensions of the array.
    M : (3, 3) ndarray
        Transformation matrix.

    Returns
    -------
    corners : (M, 3) ndarray
        Transformed coordinates.

    """
    cnrs = corners((cols, rows))
    # Turn into homogenous coordinates by adding a column of ones
    cnrs = np.hstack((cnrs, np.ones((len(cnrs), 1)))).astype(sc.ftype)
    # Transform coordinates and add to list
    tf_cnrs = np.dot(cnrs, M.transpose())
    tf_cnrs /= np.atleast_2d(tf_cnrs[:, 2]).T

    return tf_cnrs[:, :2]

def mask_roi(rows, cols, bounds):
    """Return a mask for operating only on pixels inside the given bounds.

    Parameters
    ----------
    rows, cols : int
        Shape of the target image.
    bounds : (M, 3) array of (x, y, 1) coordinates
        Boundary coordinates.

    """
    # Sort corners clockwise.  This can be done with a single
    # swap operation, but that's a bit more work.
    mask = (bounds < 1e-14)
    bounds[mask] -= 0.5
    bounds[~mask] += 0.5

    centroid = bounds.mean(axis=0)
    diff = bounds - centroid
    angle = np.arctan2(diff[:, 1], diff[:, 0])
    bounds = bounds[np.argsort(angle)]
    bounds = np.vstack((bounds, bounds[0]))

    p = Polygon(bounds[:, 0], bounds[:, 1])
    g = Grid(rows, cols)
    return p.inside(g['cols'].flat, g['rows'].flat).reshape(rows, cols)

def with_transform(images, matrices, weights=None, order=1,
                   oshape=None, save_tiff=False,
                   method='interpolate'):
    """Stack images after performing coordinate transformations.

    Parameters
    ----------
    images : list of ndarray
        Images to be stacked.
    matrices : list of (3,3) ndarray
        Coordinate transformation matrices.
    weights : list of float
        Weight of each input image.  By default, all images are
        weighted equally.  The merging algorithm takes into account
        whether images overlap.
    order : int
        Order of the interpolant used by the scaling algorithm.  Linear,
        by default.
    oshape : tuple of int
        Output shape.  If not specified, the output shape is auto determined to
        include all images.
    save_tiff : bool
        Whether to save copies of the warped images.  False by default.
    method : {'interpolate', 'polygon'}
        Use standard interpolation (default) or polygon interpolation.
        Note: Polygon interpolation is currently disabled.

    Notes
    -----
    For each image, a 3x3 coordinate transformation matrix, ``A``,
    must be given. Each coordinate, ``c = [x,y,1]^T``, in the source
    image is then translated to its position in the destination image,
    ``d = A*c``.

    After warping the images, they are combined according to the given
    weights.  Note that the overlap of frames is taken into account.
    For example, in areas where only one image occurs, the pixels of
    that image will carry a weight of one, whereas in other areas it
    may be less, depending on the overlap of other images.

    """
    nr_images = len(images)
    if weights is None:
        weights = np.ones(nr_images, dtype=sc.ftype) / nr_images

    if not (len(images) == len(matrices) == len(weights)):
        raise ValueError("Number of images, transformation matrices and "
                         "weights should match.")

    images = [np.atleast_2d(i) for i in images]
    affine_matrices = [np.atleast_2d(m) for m in matrices]

    reshape = (oshape is None)
    if reshape:
        all_tf_cnrs = np.empty((0,2))
        for img, tf_matrix in zip(images, matrices):
            rows, cols = img.shape[:2]
            tf_cnrs = _tf_corners(rows, cols, tf_matrix)
            all_tf_cnrs = np.vstack((all_tf_cnrs, tf_cnrs))

        # Calculate bounding box [(x0,y0),(x1,y1)]
        bbox_top_left = np.floor(all_tf_cnrs.min(axis=0))
        bbox_bottom_right = np.ceil(all_tf_cnrs.max(axis=0))

        oshape = np.array(images[0].shape)
        oshape[:2][::-1] = np.absolute(bbox_bottom_right -
                                       bbox_top_left).astype(int) + 1

    sources = []
    boundaries = []
    for n, (img, tf_matrix, weight) in \
            enumerate(zip(images, affine_matrices, weights)):
        if reshape:
            tf_matrix = tf_matrix.copy()
            tf_matrix[:2,2] -= bbox_top_left

        boundaries.append(_tf_corners(img.shape[0] + 1,
                                      img.shape[1] + 1, tf_matrix))
#        if method == 'polygon':
#            sources.append(interp_transf_polygon(img, np.linalg.inv(tf_matrix),
#                                                 oshape))
#        else:
        sources.append(transform.matrix(img, tf_matrix,
                                        output_shape=oshape, order=order,
                                        mode='reflect'))

        log.info('Transformed image %d' % n)

    if save_tiff:
        from scipy.misc import imsave
        for n, (s, bounds) in enumerate(zip(sources, boundaries)):
            # Convert to 4-channel RGBA
            tmp = np.empty(np.append(s.shape[:2], 4), dtype=s.dtype)
            if s.ndim == 3:
                print tmp.shape, s.shape
                tmp[..., :3] = s[..., :3]

                # Keep red layer for use as mask
                s = s[..., 0]
            else:
                # Fill R, G, and B
                tmp.T.swapaxes(1, 2)[:] = s

            tmp[..., 3] = 0

            mask = mask_roi(s.shape[0], s.shape[1], bounds)

            # Set the alpha mask
            t = tmp[...,3]
            t.fill(255)
            t[~mask] = 0

            imsave('stack_%d.tiff' % n, tmp)

    out = np.zeros(oshape, dtype=sc.ftype)
    total_weights = np.zeros(oshape, dtype=float)
    for (s, bounds), w in zip(zip(sources, boundaries), weights):
        mask = mask_roi(s.shape[0], s.shape[1], bounds)
        out[mask] += (w * s)[mask]
        total_weights[mask] += w

    mask = (total_weights != 0)
    out[mask] = out[mask] / total_weights[mask]

    return out
