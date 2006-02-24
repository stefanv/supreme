import supreme.config as SC
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
        return super(Grid, cls).__new__(cls, shape=(rows,columns),
                                        dtype=[('x',SC.ftype),
                                               ('y',SC.ftype),
                                               ('z',SC.ftype)])

    def __init__(self, rows, columns):
        """Initialise the grid values. See __new__."""
        cgrid = N.empty((3, rows, columns), dtype=SC.ftype)
        cgrid[:2, :, :] = N.float32(N.mgrid[:columns, :rows].swapaxes(1,2))
        cgrid[2,:,:].fill(1)

        # c = cgrid generates a mesh with
        #
        # c[0,:,:] = y values
        # c[1,:,:] = x values
        #
        # axes (0,1,2)
        #       ^ ^ ^
        #       | | `- column-wise position in grid
        #       | `--- row-wise position in grid
        #       `----- stacked dimension (x, y values)
        #
        # If we flatten this matrix, iteration will be done along
        # dimension 2, then 1 then 0.  We want iteration over the stacked
        # dimension, therefore we reverse axes by doing
        #
        # c = c.swapaxes(0,2)
        #
        # Since cgrid produces (row,column) and not (x,y) we need to do
        # another axes swop:
        #
        # c = c.swapaxes(0,1)
        #
        # So the final axes are (1,2,0)
        
        self.view((SC.ftype, 3))[:] = cgrid.swapaxes(0,2).swapaxes(0,1)[:]

    @property
    def coords(self):
        return self.view((SC.ftype, 3)).reshape(-1,3)
