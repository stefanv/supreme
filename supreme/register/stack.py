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

def affine(images,affine_matrices,weights=None,order=1):
    """Stack images after performing affine transformations.

    affine_matrices is a list of matrices, with each matrix of the form

    [[a b c]
     [d e f]
     [0 0 1]]"""
    nr_images = len(images)
    if weights is None:
        weights = N.ones(nr_images,dtype=SC.ftype)/nr_images

    if not (len(images) == len(affine_matrices) == len(weights)):
        raise ValueError("Number of images, affine matrices and weights should match.")

    images = [N.atleast_2d(i) for i in images]
    affine_matrices = [N.atleast_2d(m) for m in affine_matrices]

    all_tf_cnrs = N.empty((0,3))
    for img,tf_matrix in zip(images,affine_matrices):
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
    oshape[:2][::-1] = N.absolute((bbox_bottom_right - bbox_top_left)).astype(int)

    out = N.zeros(oshape,dtype=SC.ftype)
    for img,tf_matrix,weight in zip(images,affine_matrices,weights):
        tf_matrix[:2,2] = tf_matrix[:2,2] - bbox_top_left
        out += weight * transform.matrix(img,tf_matrix,
                                         output_shape=oshape,order=order)

    return out
    
if __name__ == "__main__":
    img = N.array([[1,0,1,2],[2,0,1,1],[3,0,0,1],[4,5,3,2]])
    theta = 30/180.*N.pi
    stack_affine((img,),([[N.cos(theta),-N.sin(theta),0],
                          [N.sin(theta),N.cos(theta),0],
                          [0,0,1]],))
    
