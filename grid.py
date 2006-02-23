import supreme as S
import numpy as N

class Grid(N.ndarray):
    def __new__(cls, rows, columns):
        """
        Create a regular grid given rows and columns.
        
        The grid is of the specified size, with each element describing the
        (x,y,z) co-ordinate of the top right-hand corner of a pixel (note that
        x and y here are the columns and the rows respectively).

        The elements of the grid can be accessed using record notation, i.e.

        Grid(3,3)['x'] # y, or z

        A regular grid allows for transformations, as long as the
        neighbours of each coordinate stay the same.
        """
        coords = super(Grid, cls).__init__(cls)
        coords = N.empty((rows,columns), dtype=[('x',S.ftype),('y',S.ftype),('z',S.ftype)], fortran=1)

        cgrid = N.empty((3, rows, columns), dtype=S.ftype)
        cgrid[:2, :, :] = N.float32(N.mgrid[:columns, :rows].swapaxes(1,2))
        cgrid[2,:,:].fill(1)

        coords.view((S.ftype, 3))[:] = cgrid

        return coords

