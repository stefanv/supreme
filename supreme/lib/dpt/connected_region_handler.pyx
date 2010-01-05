#cython: cdivision=True
# -*- python -*-

import numpy as np

# "cimport" is used to import special compile-time information
# about the numpy module (this is stored in a file numpy.pxd which is
# currently part of the Cython distribution).
cimport numpy as np
cimport stdlib

cimport connected_region_handler as crh
cimport int_array as iarr
from int_array cimport IntArray

# Cython does not make it particularly easy to cdef static methods,
# so we define these methods in their own module so they handle
# similarly to static methods.

cdef _iterate_rows(ConnectedRegion cr):
    """For each row, return the connected columns as

    (row, start, end)

    Note that this row includes the row offset.

    """
    cdef int* rowptr = cr.rowptr.buf
    cdef int* colptr = cr.colptr.buf

    cdef list out = []
    cdef int r, c, start, end
    for r in range(cr.rowptr.size - 1):
        for c in range((rowptr[r + 1] - rowptr[r]) / 2):
            start = colptr[rowptr[r] + 2*c]
            end = colptr[rowptr[r] + 2*c + 1]

            # Cython does not yet support "yield"
            out.append((r + cr._start_row, start, end))

    return out

cpdef int nnz(ConnectedRegion cr):
    """Return the number of non-zero elements.

    """
    cdef int n = 0
    cdef int i
    cdef int *rowptr, *colptr

    rowptr = cr.rowptr.buf
    colptr = cr.colptr.buf

    for i in range((rowptr[cr.rowptr.size - 1] - rowptr[0]) / 2):
        n += colptr[2*i + 1] - colptr[2*i]

    return n

cpdef get_shape(ConnectedRegion cr):
    return cr._shape

cdef _minimum_shape(ConnectedRegion cr):
    """Return the minimum shape into which the connected region can fit.

    """
    return (cr._start_row + cr.rowptr.size - 1, iarr.max(cr.colptr))

cpdef reshape(ConnectedRegion cr, shape=None):
    """Set the shape of the connected region.

    Useful when converting to dense.
    """
    if shape is None:
        cr._shape = crh._minimum_shape(cr)
    elif (shape >= crh._minimum_shape(cr)):
        cr._shape = shape
    else:
        raise ValueError("Minimum shape is %s." % \
                         crh._minimum_shape(cr))

cpdef ConnectedRegion copy(ConnectedRegion cr):
    """Return a deep copy of the connected region.

    """
    cdef int i

    cdef ConnectedRegion tmp = ConnectedRegion(shape=cr._shape, value=cr._value,
                                               start_row=cr._start_row)
    iarr.copy(cr.rowptr, tmp.rowptr)
    iarr.copy(cr.colptr, tmp.colptr)

    tmp._nnz = crh.nnz(tmp)

    return tmp

cpdef set_start_row(ConnectedRegion cr, int start_row):
    """Set the first row where values occur.

    """
    if start_row <= ((<int>cr._shape[0]) - cr.rowptr.size + 1):
        cr._start_row = start_row
    else:
        raise ValueError("Start row is too large for the current "
                         "shape.  Reshape the connectedregion first.")

cpdef int get_start_row(ConnectedRegion cr):
    return cr._start_row

cpdef list get_colptr(ConnectedRegion cr):
    return iarr.to_list(cr.colptr)

cpdef list get_rowptr(ConnectedRegion cr):
    return iarr.to_list(cr.rowptr)

cpdef int contains(ConnectedRegion cr, int r, int c):
    """Does the connected region contain an element at (r, c)?

    """
    cdef int i, rows
    cdef int *colptr, *rowptr
    colptr = cr.colptr.buf
    rowptr = cr.rowptr.buf

    r -= cr._start_row

    rows = cr.rowptr.size

    if r < 0 or r > rows - 2:
        return False

    if c < 0 or c >= <int>cr._shape[1]:
        return False

    for i in range((rowptr[r + 1] - rowptr[r]) / 2):
        if (c >= colptr[rowptr[r] + 2*i]) and \
           (c < colptr[rowptr[r] + 2*i + 1]):
            return True

    return False

cdef _outside_boundary(ConnectedRegion cr, int* workspace):
    """Calculate the outside boundary using a scanline approach.

    Notes
    -----
    A scanline is constructed that is as wide as the region.  The
    scanline moves down the image from the top.  For each position
    in the scanline, if

    - the pixel above or below or diagonally is part of the region
    - and the pixel at the current position is not

    then assign this position as part of the outside boundary.

    The advantage of this approach is that we are guaranteed the
    boundary positions ordered from top left to bottom right,
    which will be useful later when we join two regions together.

    Theoretically, an interval tree should be more efficient to
    determine the overlap between connected intervals, but the
    data structures and allocations required are more complex.  We
    shall have to benchmark both to know for sure.

    As an optimisation, we evaluate only points next to inside
    boundary positions.

    Parameters
    ----------
    cr : ConnectedRegion
        Region for which the boundary must be calculated.
    workspace : int*
        BLock of memory that can hold ``3 * sizeof(int) * (columns + 2)``
        where columns is the largest number of columns spanned by cr
        in a single row.

    """
    cdef int i # scanline row-position
    cdef int j # column position in scanline
    cdef int start, end, k, c
    cdef IntArray x = IntArray()
    cdef IntArray y = IntArray()

    cdef int* rowptr = cr.rowptr.buf
    cdef int* colptr = cr.colptr.buf

    cdef int rows = cr.rowptr.size - 1

    cdef int col_min = iarr.min(cr.colptr)
    cdef int col_max = iarr.max(cr.colptr)
    cdef int columns = col_max - col_min

    cdef int* line_above = <int*><void*>workspace
    cdef int* line = <int*><void*>line_above + columns + 2
    cdef int* line_below = <int*><void*>line + columns + 2

    for j in range(columns + 2):
        line[j] = 0
        line_below[j] = 0
        line_above[j] = 0

    for i in range(-1, rows + 2):
        # Update scanline and line above scanline
        if i >= 0:
            for j in range(columns + 2):
                line_above[j] = line[j]
                line[j] = line_below[j]

        # When the scanline reaches the last line,
        # fill line_below with zeros
        if i <= rows:
            for j in range(columns + 2):
                line_below[j] = 0

        # Update line below scanline
        if i + 1 < rows:
            for j in range((rowptr[i + 2] - rowptr[i + 1]) / 2):
                start = colptr[rowptr[i + 1] + 2*j]
                end = colptr[rowptr[i + 1] + 2*j + 1]

                for k in range(start - col_min, end - col_min):
                    line_below[k + 1] = 1

        # Note that the columns run from -1...columns, but the
        # array indices run from 0...columns+2

        for j in range(-1, columns + 1):
            # Test eight neighbours for connections
            if (line[j + 1] == 0) and \
               (line_above[j + 1] == 1 or \
                line_below[j + 1] == 1 or \
                (j >= 0 and
                 (line_above[j] == 1 or
                  line[j] or
                  line_below[j] == 1)) or \
                (j < columns and
                 (line_above[j + 2] == 1 or
                  line[j + 2] == 1 or
                  line_below[j + 2] == 1))):
                iarr.append(x, j + col_min)
                iarr.append(y, i + cr._start_row)

    return y, x

def outside_boundary(ConnectedRegion cr):
    cdef int* workspace = <int*>stdlib.malloc(sizeof(int) * 3 *
                                              (cr._shape[1] + 2))
    cdef IntArray y, x
    y, x = _outside_boundary(cr, workspace)

    stdlib.free(workspace)

    return y, x

cpdef set_value(ConnectedRegion cr, int v):
    cr._value = v

cpdef int get_value(ConnectedRegion cr):
    return cr._value


cpdef validate(ConnectedRegion cr):
    if cr.rowptr.buf[cr.rowptr.size - 1] != cr.colptr.size:
        raise RuntimeError("ConnectedRegion was not finalised.  Ensure "
                           "rowptr[-1] points beyond last entry of "
                           "colptr.")

    if cr.colptr.size % 2 != 0:
        raise RuntimeError("Colptr must have 2xN entries.")

# Return type should be bool, but cython complains
cdef int gt(int a, int b):
    return a > b

cdef int lt(int a, int b):
    return a < b

cdef int _boundary_extremum(IntArray boundary_x, IntArray boundary_y,
                            np.int_t* img,
                            int max_rows, int max_cols,
                            int (*func)(int, int),
                            int initial_extremum = 0):
    """Determine the extremal value on the boundary of a
    ConnectedRegion.

    Parameters
    ----------
    boundary_x, boundary_y : list
        X and Y coordinates of boundary.
    img : Input image as integer array
    max_rows, max_cols : int
        Dimensions of img.
    func : callable
        Function used to test for the extreme value:

        func(img[r, c], cr.value)
    initial_extremum : int

    """
    cdef int i, r, c
    cdef np.int_t img_val
    cdef int extremum = initial_extremum

    for i in range(boundary_y.size):
        r = boundary_y.buf[i]
        c = boundary_x.buf[i]

        if r < 0 or r >= max_rows or c < 0 or c >= max_cols:
            continue

        img_val = img[r*max_cols + c]
        if func(img_val, extremum) == 1:
            extremum = img_val

    return extremum

cdef int _boundary_maximum(IntArray boundary_x, IntArray boundary_y,
                           np.int_t* img,
                           int max_rows, int max_cols):
    return _boundary_extremum(boundary_x, boundary_y, img,
                              max_rows, max_cols, gt, -1)

cdef int _boundary_minimum(IntArray boundary_x, IntArray boundary_y,
                           np.int_t* img,
                           int max_rows, int max_cols):
    return _boundary_extremum(boundary_x, boundary_y, img,
                              max_rows, max_cols, lt, 256)

# Python wrappers for the above two functions
def boundary_maximum(ConnectedRegion cr,
                     np.ndarray[np.int_t, ndim=2] img):
    cdef IntArray y, x
    y, x = outside_boundary(cr)
    return _boundary_maximum(x, y, <np.int_t*>img.data,
                             img.shape[0], img.shape[1])

def boundary_minimum(ConnectedRegion cr,
                     np.ndarray[np.int_t, ndim=2] img):
    cdef IntArray y, x
    y, x = outside_boundary(cr)
    return _boundary_minimum(x, y, <np.int_t*>img.data,
                             img.shape[0], img.shape[1])


cdef int min2(int a, int b):
    if a < b:
        return a
    else:
        return b

cdef int max2(int a, int b):
    if a > b:
        return a
    else:
        return b

cpdef merge(ConnectedRegion a, ConnectedRegion b):
    """Merge b into a.  b and a must be connected.

    """
    cdef int i, r, rpt, cpt
    cdef int start_row = min2(a._start_row, b._start_row)
    cdef int end_row = max2(a._start_row + a.rowptr.size - 2,
                            b._start_row + b.rowptr.size - 2)

    cdef IntArray new_colptr = IntArray()
    cdef IntArray new_rowptr = IntArray()

    cdef list cols, merged_cols

    for r in range(start_row, end_row + 1):
        iarr.append(new_rowptr, new_colptr.size)

        # Non-overlapping, use b
        if r < a._start_row or r > (a.rowptr.size + a._start_row - 2):
            rpt = r - b._start_row
            for i in range(b.rowptr.buf[rpt], b.rowptr.buf[rpt + 1]):
                iarr.append(new_colptr, b.colptr.buf[i])

        # Non-overlapping, use a
        elif r < b._start_row or r > (b.rowptr.size + b._start_row - 2):
            rpt = r - a._start_row
            for i in range(a.rowptr.buf[rpt], a.rowptr.buf[rpt + 1]):
                iarr.append(new_colptr, a.colptr.buf[i])

        # Overlapping: merge
        else:
            cols = []
            merged_cols = []
            rpt = r - a._start_row
            for i in range((a.rowptr.buf[rpt + 1] - a.rowptr.buf[rpt]) // 2):
                cpt = a.rowptr.buf[rpt] + 2 * i

                cols.append([a.colptr.buf[cpt], a.colptr.buf[cpt + 1]])

            rpt = r - b._start_row
            for i in range((b.rowptr.buf[rpt + 1] - b.rowptr.buf[rpt]) // 2):
                cpt = b.rowptr.buf[rpt] + 2 * i

                cols.append([b.colptr.buf[cpt], b.colptr.buf[cpt + 1]])

            cols.sort()

            for i in range(len(cols) - 1):
                if cols[i][1] == cols[i+1][0]:
                    cols[i+1][0] = cols[i][0]
                    continue
                merged_cols.extend(cols[i])

            merged_cols.extend(cols[-1])

            for i in merged_cols:
                iarr.append(new_colptr, i)

    iarr.append(new_rowptr, new_colptr.size)

    a.colptr = new_colptr
    a.rowptr = new_rowptr
    a._start_row = start_row
    reshape(a)
    a._nnz = a._nnz + b._nnz

cdef _set_array(np.int_t* arr, int rows, int cols,
                ConnectedRegion cr, int value,
                int mode=0):
    """Set the value of arr over the connected region.

    Mode: 0 == replace, 1 == add

    """
    cdef int* rowptr = cr.rowptr.buf
    cdef int* colptr = cr.colptr.buf

    cdef int r, c, start, end, k, start_row = cr._start_row

    for r in range(cr.rowptr.size - 1):
        for c in range((rowptr[r + 1] - rowptr[r]) / 2):
            start = colptr[rowptr[r] + 2*c]
            end = colptr[rowptr[r] + 2*c + 1]

            for k in range(start, end):
                # This could probably be done more efficiently
                if r >= 0 and r < rows and \
                   start >= 0 and start < cols and \
                   end >= 0 and end <= cols:
                    if mode == 0:
                        arr[(r + start_row)*cols + k] = value
                    else:
                        arr[(r + start_row)*cols + k] += value

def set_array(np.ndarray[np.int_t, ndim=2] arr,
              ConnectedRegion c, int value, str mode='replace'):

    cdef int add_mode = 0
    if mode == 'add':
        add_mode = 1

    return _set_array(<np.int_t*>arr.data, arr.shape[0], arr.shape[1],
                      c, value, add_mode)

cpdef bounding_box(ConnectedRegion cr):
    return (cr._start_row, iarr.min(cr.colptr),
            cr._start_row + cr.rowptr.size - 2, iarr.max(cr.colptr) - 1)

# These methods are needed by the lulu decomposition to build
# connected regions incrementally

cpdef _new_row(ConnectedRegion cr):
    cdef int L = cr.colptr.size

    if not cr.rowptr.buf[cr.rowptr.size - 1] == L:
        iarr.append(cr.rowptr, L)

cpdef int _current_row(ConnectedRegion cr):
    return cr.rowptr.size + cr._start_row - 1

# This internal method is only used to construct proper test data
def _append_colptr(ConnectedRegion cr, *ints):
    for i in ints:
        iarr.append(cr.colptr, i)

def todense(ConnectedRegion cr):
    """Convert the connected region to a dense array.

    """
    crh.validate(cr)

    shape = cr._shape
    if shape is None:
        shape = crh._minimum_shape(cr)

    cdef np.ndarray[np.int_t, ndim=2] out = np.zeros(shape, dtype=np.int)

    cdef int row, start, end

    for row, start, end in crh._iterate_rows(cr):
        for k in range(start, end):
            out[row, k] = cr._value

    return out
