__all__ = ['Grid']

import numpy as N
from numpy.testing import *

set_local_path('../../..')
import supreme as SR
import supreme.config as SC
restore_path()

class Grid(object):
    """Regular grid."""

    def __init__(self,rows,cols):
        """
        Create a grid given rows and columns.

        Input
        -----
        
        cols,rows -- If the grid is rectangular, the coordinates are
                     specified as 1D arrays.  Otherwise give all
                     the coordinates, as in a meshgrid.  If cols and
                     rows are scalar, a rectangular grid is generated with

               cols == N.arange(cols), rows == N.arange(rows)

        Output
        ------
        A grid object representing homogenous coordinates.  Each coordinate
        describes the (col,row,z) co-ordinate of the top right-hand
        corner of a pixel.

        The elements of the grid can be accessed using record notation, i.e.

        Grid(3,3)['cols'] # rows, or z

        A regular grid allows for transformations, as long as the
        neighbours of each coordinate stay the same.

        TODO: ^ Better description of the above.
        """
        if N.isscalar(cols) or N.isscalar(rows):
            cols,rows = map(N.arange,[cols,rows])
        cols,rows = map(N.array,[cols,rows])
        assert cols.ndim == rows.ndim, "Must provide same number of cols and rows coordinates as 1D arrarowss"
        
        if cols.ndim == 1:
            shape = (len(cols),len(rows))
            cols,rows = N.meshgrid(cols,rows)

        shape = cols.shape
        _grid = N.empty(shape=shape,dtype=[('cols',SC.ftype),
                                           ('rows',SC.ftype),
                                           ('z',SC.ftype)])

        _grid['cols'],_grid['rows'] = cols,rows
        _grid['z'] = 1

        self._grid = _grid.view(N.recarray)

    def __getitem__(self, *args, **kwargs):
        return self._grid.__getitem__(*args, **kwargs)

    def __getattr__(self, *args, **kwargs):
        return self._grid.__getattribute__(*args, **kwargs)

    @property
    def coords(self):
        """Return an array of all coordinates.

        Example: show coordinate at grid position (1,0)
        -----------------------------------------------
        coords()[1,0]

        """
        
        return self._grid.view((SC.ftype, 3))
