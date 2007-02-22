"""Read and write image files."""

__all__ = ['ImageCollection','imread']

from glob import glob

import numpy as N
from numpy.testing import set_local_path, restore_path
from scipy.misc.pilutil import imread

set_local_path('../..')
import supreme
restore_path()

class ImageCollection(object):
    """Load and manage a collection of images."""

    def __init__(self,file_pattern,conserve_memory=True):
        """Load image files.

        Note that files are always stored in alphabetical order.

        Input:
        ------
        file_pattern : string
            Path and pattern of files to load, e.g. 'data/*.jpg'.
        conserve_memory : bool
            If True, never keep more than one in memory at a specific
            time.  Otherwise, images will be cached once they are loaded.

        Example:
        --------
        >>> from os.path import dirname, join
        >>> data_dir = join(dirname(__file__),'tests')

        >>> c = ImageCollection(data_dir + '/*.png')
        >>> len(c)
        3
        >>> c[2].shape
        (20, 20, 3)

        """
        self.files = sorted(glob(file_pattern))

        if conserve_memory:
            memory_slots = 1
        else:
            memory_slots = len(self.files)

        self.conserve_memory = conserve_memory
        self.data = N.empty(memory_slots,dtype=object)

    def __getitem__(self,n,_cached=N.array(-1)):
        """Return image n in the queue.

        Loading is done on demand.

        Input:
        ------
        n : int
            Number of image required.

        Output:
        -------
        img : array
           Image #n in the collection.

        """
        idx = n % len(self.data)
        if (_cached != n and self.conserve_memory) or (self.data[idx] is None):
            self.data[idx] = imread(self.files[n])

        _cached.flat = n

        return self.data[idx]

    def __iter__(self):
        """Iterate over the images."""
        for i in range(len(self)):
            yield self[i]

    def __len__(self):
        """Number of images in collection."""
        return len(self.files)
