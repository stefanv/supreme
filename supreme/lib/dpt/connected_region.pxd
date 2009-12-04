# -*- python -*-

from int_array cimport IntArray

cdef class ConnectedRegion:
    cdef int _value
    cdef int _start_row
    cdef int _nnz
    cdef tuple _shape # fixme: split into x and y

    cdef IntArray rowptr
    cdef IntArray colptr
