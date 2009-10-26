"""Coordinate grids."""

__all__ = ['Grid']

import numpy as np
from numpy.testing import *

import supreme as SR
import supreme.config as SC

class Grid(object):
    """Regular grid."""

    def __init__(self,rows,cols):
        """
        Create a grid given rows and columns.

        Input:
        ------
        rows,cols : 1D array
            If the grid is rectangular, the coordinates are specified
            as 1D arrays.  Otherwise give all the coordinates, as in a
            meshgrid.  If cols and rows are scalar, a rectangular grid
            is generated with

               rows == np.arange(rows), cols == np.arange(cols)

        Output:
        -------
        A grid object representing homogenous coordinates.  Each coordinate
        describes the (col,row,z) co-ordinate of the top right-hand
        corner of a pixel.

        The elements of the grid can be accessed using record notation, i.e.

        Grid(3,3)['cols'] # rows, or z

        A regular grid allows for transformations, as long as the
        neighbours of each coordinate stay the same.

        TODO: ^ Better description of the above.
        """
        if np.isscalar(cols) or np.isscalar(rows):
            cols,rows = map(np.arange,[cols,rows])
        cols,rows = map(np.array,[cols,rows])
        assert cols.ndim == rows.ndim, "Must provide same number of cols and rows coordinates as 1D arrarowss"

        if cols.ndim == 1:
            shape = (len(cols),len(rows))
            cols,rows = np.meshgrid(cols,rows)

        shape = cols.shape
        _grid = np.empty(shape=shape,dtype=[('cols',SC.ftype),
                                           ('rows',SC.ftype),
                                           ('z',SC.ftype)])

        _grid['cols'],_grid['rows'] = cols,rows
        _grid['z'] = 1

        self._grid = _grid.view(np.recarray)

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
