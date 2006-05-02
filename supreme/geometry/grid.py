__all__ = ['Grid']

import supreme.config as SC
import numpy as N

class Grid(object):
    """Regular grid."""

    def __init__(self,rows,columns):
        """
        Create a regular grid given rows and columns.
        
        The grid is of the specified size, with each element describing the
        (x,y,z) co-ordinate of the top right-hand corner of a pixel.

        The elements of the grid can be accessed using record notation, i.e.

        Grid(3,3)['x'] # y, or z

        A regular grid allows for transformations, as long as the
        neighbours of each coordinate stay the same.

        TODO: ^ Better description of the above.
        """

        self._grid = N.empty(shape=(rows,columns),
                             dtype=[('x',SC.ftype),
                                    ('y',SC.ftype),
                                    ('z',SC.ftype)])

        # A meshgrid X of shape (2,columns,rows) are generated. Here,
        # X[0,...]^T represent the y co-ordinates, and
        # X[1,...]^T represent the x co-ordinates.
        #
        # We need to reshape these fields to have a new matrix Y for
        # which
        # Y[...,0] are the x co-ordinates and
        # Y[...,1] are the y co-ordinates.
        #
        # This is achieved by doing X.swapaxes(0,2)
        cgrid = N.empty((rows,columns,3), dtype=SC.ftype)        
        cgrid[...,:2] = N.mgrid[:columns,:rows].swapaxes(0,2).astype(SC.ftype)
        cgrid[...,2].fill(1)

        # We can't just use _grid[:], since those are not of type SC.ftype
        self._grid.view((SC.ftype, 3))[:] = cgrid[:]

    def __getitem__(self, *args, **kwargs):
        return self._grid.__getitem__(*args, **kwargs)

    @property
    def coords(self):
        return self._grid.view((SC.ftype, 3))
