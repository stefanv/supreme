from numpy.testing import set_local_path, restore_path
import numpy as N

set_local_path('../../..')
from supreme.config import ftype,itype
restore_path()

def along_path(path,image,shape=(3,3),centre=None):
    """Cut blocks of shape from image along the specified path."""

    shape = N.asarray(shape)
    if not centre:
        if not N.all(shape % 2 == 1):
                raise UserWarning("Even elements in shape: closest integer centre taken.")
        centre = N.around((shape-1)/2.)
    else:
        centre = N.asarray(centre)

    # [[x_min,y_min],[x_max,y_max]]
    block_coords = N.array([[0,x] for x in shape]).astype(itype).transpose()
    
    img_limits = N.array([[0,x] for x in image.shape[:2]]).astype(itype).transpose()

    out = N.zeros(shape)
    for p in path:
        # Coordinates in the target matrix
        cut_coords = block_coords - centre + p

        # Limit the coordinates to the matrix extent
        cut_coords = N.where((cut_coords >= img_limits[[0],:].transpose()) &
                             (cut_coords <= img_limits[[1],:].transpose()),
                             cut_coords, img_limits)

        # Position of limited coordinates in input
        rc = cut_coords - p + centre

        dest_idx = [slice(*coord) for coord in rc.transpose()]
        src_idx = [slice(*coord) for coord in cut_coords.transpose()]

        out.fill(0)
        out[dest_idx] = image[src_idx]

        yield out
