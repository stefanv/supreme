"""
Stack warped images.
"""

from numpy.testing import set_local_path, restore_path
import numpy as N
from scipy import ndimage as ndi

set_local_path('../..')
import supreme.config as SC
from supreme import transform
restore_path()

def corners(dims):
    """Return the corner coordinates for a matrix of the given
    dimensions."""

    dims = N.array(dims)
    L = len(dims)
    corners = N.empty((2**L,L),dtype=dims.dtype)
    zeros = dims.copy()*0
    for i in range(2**L):
        bin = list(N.binary_repr(i).zfill(L))
        mask = N.array(bin).astype(N.bool8)
        corners[i] = N.where(mask,dims-1,zeros)
    return corners

def with_transform(images,matrices,weights=None,order=1,mode='constant'):
    """Stack images after performing coordinate transformations.

    images - list of arrays
    matrices - list of coordinate transformation matrices
    weights - weights of input images (default: weighted equally)

    For each image, a 3x3 coordinate transformation matrix, A,
    must be given. Each coordinate, c = [[x],[y],[1]], in the source image
    is then translated to its position in the destination image,

    d = A*c.

    Each image is transformed, weighted by the given weight and
    stacked.
    """
    nr_images = len(images)
    if weights is None:
        weights = N.ones(nr_images,dtype=SC.ftype)/nr_images

    if not (len(images) == len(matrices) == len(weights)):
        raise ValueError("Number of images, transformation matrices and weights should match.")

    images = [N.atleast_2d(i) for i in images]
    affine_matrices = [N.atleast_2d(m) for m in matrices]

    all_tf_cnrs = N.empty((0,3))
    for img,tf_matrix in zip(images,matrices):
        rows,cols = img.shape[:2]
        cnrs = corners((cols,rows))        
        # Turn into homogenous coordinates by adding a column of ones
        cnrs = N.hstack((cnrs,N.ones((len(cnrs),1)))).astype(SC.ftype)
        # Transform coordinates and add to list
        all_tf_cnrs = N.vstack((all_tf_cnrs,N.dot(cnrs,tf_matrix.transpose())))

    # Calculate bounding box [(x0,y0),(x1,y1)]
    bbox_top_left = N.floor(all_tf_cnrs.min(axis=0))[:2]
    bbox_bottom_right = N.ceil(all_tf_cnrs.max(axis=0))[:2]

    oshape = N.array(images[0].shape)
    oshape[:2][::-1] = N.absolute(bbox_bottom_right - bbox_top_left).astype(int)+1

    out = N.zeros(oshape,dtype=SC.ftype)
    for img,tf_matrix,weight in zip(images,matrices,weights):
        tf_matrix[:2,2] = tf_matrix[:2,2] - bbox_top_left
        out += weight * transform.matrix(img,tf_matrix,
                                         output_shape=oshape,order=order,
                                         mode=mode)

    return out
