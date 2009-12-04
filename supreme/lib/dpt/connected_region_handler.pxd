# -*- python -*-

from connected_region cimport ConnectedRegion
cimport numpy as np
from int_array cimport IntArray

cdef _iterate_rows(ConnectedRegion cr)
cpdef int nnz(ConnectedRegion cr)

# getters and setters
cpdef get_shape(ConnectedRegion)
cpdef int get_start_row(ConnectedRegion)
cpdef int get_value(ConnectedRegion)
cpdef list get_colptr(ConnectedRegion)
cpdef list get_rowptr(ConnectedRegion)

cpdef reshape(ConnectedRegion cr, shape=?)
cpdef set_start_row(ConnectedRegion cr, int start_row)
cpdef set_value(ConnectedRegion cr, int v)

cdef _minimum_shape(ConnectedRegion cr)
cpdef ConnectedRegion copy(ConnectedRegion cr)
cpdef int contains(ConnectedRegion cr, int r, int c)
cdef _outside_boundary(ConnectedRegion cr, int* workspace)
cpdef validate(ConnectedRegion cr)
cdef int _boundary_maximum(IntArray boundary_x, IntArray boundary_y,
                           np.int_t* img,
                           int rows, int cols)
cdef int _boundary_minimum(IntArray boundary_x, IntArray boundary_y,
                           np.int_t* img,
                           int rows, int cols)
cpdef merge(ConnectedRegion, ConnectedRegion)
cdef _set_array(np.int_t* arr, int rows, int cols, ConnectedRegion c,
                int value, int mode=?)
cpdef bounding_box(ConnectedRegion cr)

# Useful functions
cdef int min2(int a, int b)
cdef int max2(int a, int b)
cdef int gt(int a, int b)
cdef int lt(int a, int b)

# These methods are needed by the lulu decomposition to build
# connected regions incrementally

cpdef _new_row(ConnectedRegion cr)
cpdef int _current_row(ConnectedRegion cr)

