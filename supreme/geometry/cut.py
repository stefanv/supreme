"""Cut blocks from images along a given coord_path."""

from numpy.testing import set_local_path, restore_path
import numpy as N
import warnings

set_local_path('../..')
from supreme.config import ftype,itype
restore_path()

def along_path(path,image,shape=(3,3),centre=None):
    """Cut blocks of shape from image along the specified path.

    path -- at each point in the path, cut out an image
    shape -- size of image to cut out
    centre -- define the centre of the cutout (default: (shape-1)/2)

    """

    if len(shape) != 2:
        raise ValueError("Argument shape should be 2-dimensional")

    shape = N.asarray(shape)
    if not centre:
        if not N.all(shape % 2 == 1):
                warnings.warn("Even elements in shape: closest integer centre taken.")
        centre = N.around((shape-1)/2.).astype(itype)
    else:
        centre = N.asarray(centre).astype(itype)

    # [[x_min,y_min],[x_max,y_max]]
    block_coords = N.array([[0,x] for x in shape], dtype=itype).transpose()
    
    img_limits = N.array([[0,x] for x in image.shape[:2]], dtype=itype).transpose()

    oshape = N.array(image.shape)
    oshape[:2] = shape
    for p in path:
        p = N.asarray(p,dtype=int)
        out = N.zeros(oshape,dtype=image.dtype)

        # Coordinates in the target matrix
        cut_coords = block_coords - centre + p

        # Limit the coordinates to the matrix extent
        cut_coords = N.where((cut_coords >= img_limits[[0]]) & \
                             (cut_coords <= img_limits[[1]]),
                             cut_coords, img_limits)

        # Position of limited coordinates in input
        rc = cut_coords - p + centre

        # Check for case where requested cut is completely outside image
        invalid_idx = N.any(cut_coords < 0) | N.any(rc < 0)

        if not invalid_idx:
            dest_idx = [slice(*coord) for coord in rc.transpose()]
            src_idx = [slice(*coord) for coord in cut_coords.transpose()]
            out[dest_idx] = image[src_idx]
        
        yield out
