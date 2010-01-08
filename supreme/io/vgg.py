"""Load a super-resolution dataset from Oxford's Vision and Geometry Group.

"""

__all__ = ['load_vgg']

import numpy as np

from _io import ImageCollection

import os
from glob import glob

def load_vgg(path):
    """Load a VGG super-resolution data-set.

    Parameters
    ----------
    path : str
        Path to the data-set.

    Returns
    -------
    ic : ImageCollection
        An imagecollection of all the images, with the homographies
        stored in ``x.info['H']`` for each ``x`` in `ic`.

    Notes
    -----
    A VGG data-set stores the transformations from one frame to the
    next.  This loader modifies all the homographies to be relative to
    the first frame.

    References
    ----------
    .. [1] Super-resolution test sequences by David Capel, VGG,
           University of Oxford.
           http://www.robots.ox.ac.uk/~vgg/data/data-various.html

    """
    data_paths = ['pgm', 'fields', 'png', 'jpg']
    H_paths = ['H']

    data_paths = [os.path.join(path, p) for p in data_paths]
    data_paths = [p for p in data_paths if os.path.exists(p)]

    H_paths = [os.path.join(path, p) for p in H_paths]
    H_paths = [p for p in H_paths if os.path.exists(p)]

    if not len(data_paths) == len(H_paths) or \
       len(data_paths) == 0:
        raise ValueError('Cannot find VGG directory structure.')

    data_path = data_paths[0]
    H_path = H_paths[0]

    ic = ImageCollection(os.path.join(data_path, '*'), conserve_memory=False,
                         grey=True)

    H_sofar = np.eye(3)
    for i, img in enumerate(ic):
        if i == 0:
            img.info['H'] = np.eye(3)
        else:
            H_pat = os.path.join(H_path, '*%03d.%03d*.H' % (i - 1, i))
            H_file_glob = glob(H_pat)
            if not len(H_file_glob) > 0:
                raise RuntimeError("Could not locate appropriate H-files "
                                   "searching for %s" % H_pat)
            H_file = H_file_glob[0]
            H = np.loadtxt(H_file)
            if not H.shape == (3, 3):
                raise RuntimeError("Invalid H-file found: %s" % H_file)

            H_sofar = np.dot(H, H_sofar)
            img.info['H'] = np.linalg.inv(H_sofar)
            img.info['H_rel'] = H

    return ic
