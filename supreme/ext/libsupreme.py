"""C extensions implemented using ctypes to enhance speed critical algorithms."""

import sys
import numpy as N
try:
    from ctypes import c_int, c_uint8, c_double, c_char, Structure, POINTER
except:
    print "Requires ctypes > 1.0.1"
    sys.exit(-1)

from numpy.testing import set_local_path, restore_path
set_local_path('../..')
import supreme.config as SC
restore_path()

try:
    _lib = N.ctypeslib.load_library('libsupreme_',__file__)
except:
    print \
"""Failed to load libsupreme_.so.  The library can be compiled by running

python setup.py build_ext -i

or

scons

from the package root directory."""
    sys.exit(-1)

array_1d_double = N.ctypeslib.ndpointer(dtype=N.double,ndim=1,flags='CONTIGUOUS')
array_2d_double = N.ctypeslib.ndpointer(dtype=N.double,ndim=2,flags='CONTIGUOUS')
array_1d_int = N.ctypeslib.ndpointer(dtype=N.intc,ndim=1,flags='CONTIGUOUS')
array_2d_int = N.ctypeslib.ndpointer(dtype=N.intc,ndim=2,flags='CONTIGUOUS')
array_1d_uchar = N.ctypeslib.ndpointer(dtype=N.uint8,ndim=1,flags='CONTIGUOUS')
array_2d_uchar = N.ctypeslib.ndpointer(dtype=N.uint8,ndim=2,flags='CONTIGUOUS')

# Define libsupreme API

class POI(Structure):
    """Point of intersection.

    """
    _fields_ =  [("x", c_double),
                 ("y", c_double),
                 ("type", c_int)]

# Albert's ctypes pattern
libsupreme_api = {
   'npnpoly' : (None,
                [c_int, array_1d_double, array_1d_double,
                 c_int, array_1d_double, array_1d_double,
                 array_1d_uchar]),
   'variance_map' : (None,
                     [c_int, c_int, array_2d_uchar, array_2d_double,
                      c_int, c_int]),

   'line_intersect' : (None,
                       [c_double, c_double, c_double, c_double,
                        c_double, c_double, c_double, c_double,
                        POINTER(POI)]),
   'poly_clip' : (int,
                  [c_int, array_1d_double, array_1d_double,
                   c_double, c_double, c_double, c_double,
                   array_1d_double, array_1d_double]),
   'correlate' : (None,
                  [c_int, c_int, array_2d_double,
                   c_int, c_int, array_2d_double,
                   c_int, c_int, c_int, c_int,
                   array_2d_double]),
   'interp_bilinear': (None,
                       [c_int, c_int, array_2d_uchar,
                        c_int, c_int, array_2d_double, array_2d_double,
                        c_char, c_uint8, array_2d_uchar]),
   'interp_transf_polygon': (None,
                             [c_int, c_int, array_2d_uchar,
                              c_int, c_int, array_2d_double,
                              array_2d_double]),
    }

def register_api(lib,api):
    for f, (restype, argtypes) in api.iteritems():
        func = getattr(lib, f)
        func.restype = restype
        func.argtypes = argtypes

register_api(_lib,libsupreme_api)

# Python wrappers for libsupreme functions

def atype(arrays, types):
    """Return contiguous arrays of given types.

    arrays - list of input arrays
    types - list of corresponding types

    """
    out = ()
    try:
        za = zip(arrays,types)
    except:
        za = [(arrays,types)]

    out = ()
    for A,T in za:
        out += N.ascontiguousarray(A,T),

    return out

def npnpoly(x_vertices, y_vertices, x_points, y_points):
    """Calculate whether points are in a given polygon.

    Returns a boolean array of length len(x_points).

    """
    xi,yi,x,y = atype([x_vertices,y_vertices,
                        x_points,y_points],[N.double]*4)

    if xi[0] != xi[-1] or yi[0] != yi[-1]:
        xi = N.append(xi,x[0])
        yi = N.append(yi,y[0])

    out = N.empty(len(x),dtype=N.uint8)

    _lib.npnpoly(len(xi), xi, yi,
                 len(x), x, y,
                 out)
    return out

def variance_map(image, shape=(3,3)):
    """Calculate the variance map of a 2D image.

    image -- of shape MxN
    shape -- shape of window over which variance is calculated

    A window of given shape is moved over the image, and at each point
    the variance of all the pixels in the window is stored.

    """
    image, = atype(image,N.uint8)
    assert image.ndim == 2, "Image must be 2-dimensional"
    window_size_rows, window_size_columns = shape
    rows, columns = image.shape
    output = N.zeros(image.shape,SC.ftype)
    _lib.variance_map(rows, columns, image, output,
                      window_size_rows, window_size_columns)
    return output

def line_intersect(x0,y0,x1,y1,
                   x2,y2,x3,y3):
    """Calculate the intersection between two lines.

    The first line runs from (x0,y0) to (x1,y1) and the second from
    (x2,y2) to (x3,y3).

    Return the point of intersection, (x,y), and its type:
      0 -- Normal intersection
      1 -- Intersects outside given segments
      2 -- Parallel
      3 -- Co-incident
    """
    x0,x1,x2,x3,y0,y1,y2,y3 = map(c_double, [x0,x1,x2,x3,y0,y1,y2,y3])
    p = POI()
    _lib.line_intersect(x0,y0,x1,y1,x2,y2,x3,y3,p)
    return (p.x,p.y), p.type

def poly_clip(x, y, xleft, xright, ytop, ybottom):
    """Clip a polygon to the given bounding box.

    x and y are 1D arrays describing the coordinates of the vertices.
    xleft, xright, ytop and ybottom specify the borders of the
    bounding box.  Note that a cartesian axis system is used such that
    the following must hold true:

    x_left < x_right
    y_bottom < y_top

    The x and y coordinates of the vertices of the resulting polygon
    are returned.

    """
    x,y = atype([x,y],[N.double,N.double])

    assert len(x) == len(y), "Equal number of x and y coordinates required"
    assert ytop > ybottom
    assert xleft < xright

    # close polygon if necessary
    if x[0] != x[-1] or y[0] != y[-1]:
        x = N.append(x,x[0])
        y = N.append(y,y[0])

    xleft,xright,ytop,ybottom = map(N.double,[xleft,xright,ytop,ybottom])

    workx = N.empty(2*len(x)-1,dtype=N.double)
    worky = N.empty_like(workx)
    M = _lib.poly_clip(len(x),x,y,xleft,xright,ytop,ybottom,workx,worky)
    workx[M] = workx[0]
    worky[M] = worky[0]
    return workx[:M], worky[:M]

def correlate(A,B,
              rows=None,columns=None, mode_row='zero', mode_column='zero'):
    """Correlate A and B.

    Input:
    ------
    A,B : array
        Input data.
    columns : int
        Do correlation at columns 0..columns, defaults to the number of columns in A.
    rows : int
        Do correlation at columns 0..rows, defaults to the number of rows in A.
    mode_row, mode_column : string
        How values outside boundaries are handled ('zero' or 'mirror').

    Output:
    -------
    Y : array
      Rows-by-columns array of correlation values.

    """

    A,B = atype([A,B],[N.double,N.double])
    assert A.ndim == 2 and B.ndim == 2, "Input arrays must be two dimensional"

    A_r,A_c = A.shape
    B_r,B_c = B.shape

    columns = columns or A_c
    rows = rows or A_r

    assert rows <= A_r and columns <= A_c, \
           "columns and rows cannot be larger than dimensions of A"

    modes = {'zero': 0,
             'mirror': 1}

    output = N.empty((rows,columns),dtype=N.double)
    _lib.correlate(A_r, A_c, A,
                   B_r, B_c, B,
                   rows, columns,
                   modes[mode_row], modes[mode_column],
                   output)

    return output

def interp_bilinear(grey_image,
                    transform_coords_r=None,transform_coords_c=None,
                    mode='N',cval=0,output=None):
    """Calculate values at given coordinates using bi-linear interpolation.

    The output is of shape transform_coords_*.  For each pair of
    values (transform_coords_r,transform_coords_c) the input image is
    interpolated to give the output value at that point.

    Input:
    ------
    grey_image : uint8 array
        Input image.
    transform_coords_r : 2D array
        Coordinates at row positions.
    transform_coords_c : 2D array
        Coordinates at column positions.
    mode : string
        How values at borders are handled. 'C' for constant, 'M' for
        mirror and 'W' for wrap.
    cval : int or float
        Used in conjunction with mode 'C', this specifies which value
        is used when the interpolator moves outside the borders of the
        input image.

    Optimisation parameters:
    ------------------------
    output : uint8 array of same shape as transform_coords_*
        If 'output' is provided, the result is computed in-place.

    Output:
    -------
    interpolated_image : uint8 array of same shape as transform_coords_*
        The interpolated image.

    """
    grey_image, = atype(grey_image,N.uint8)
    transform_coords_r,transform_coords_c = atype([transform_coords_r,transform_coords_c],
                                                   [N.double,N.double])
    assert grey_image.ndim == 2, "Input image must be 2-dimensional"
    assert transform_coords_r.ndim == 2 and transform_coords_c.ndim == 2, \
           "Transform coordinates must be 2-dimensional"
    if output is None:
        output = N.empty(transform_coords_r.shape,dtype=N.uint8)
    else:
        output, = atype(output,N.uint8)
        output.shape = transform_coords_r.shape

    rows,columns = grey_image.shape
    tf_rows,tf_columns = transform_coords_r.shape
    _lib.interp_bilinear(rows,columns,grey_image,
                         tf_rows,tf_columns,
                         transform_coords_r,transform_coords_c,
                         mode[0],cval,output)

    return output

def interp_transf_polygon(grey_image,transform,oshape=None):
    grey_image,transform = atype([grey_image,transform],[N.uint8,N.double])
    ishape = grey_image.shape
    if oshape is None:
        oshape = ishape

    out = N.empty(oshape,dtype=SC.ftype)
    _lib.interp_transf_polygon(ishape[0],ishape[1],grey_image,
                               oshape[0],oshape[1],out,
                               transform)
    return out

