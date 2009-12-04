cdef enum:
     HEAP_SIZE = 6

cdef class IntArray:
    cdef int* buf
    cdef int cap
    cdef int size

    cdef int heapbuf[HEAP_SIZE]

cpdef inline append(IntArray arr, int)
cpdef int max(IntArray)
cpdef int min(IntArray)
cdef inline grow(IntArray arr, int)
cpdef copy(IntArray, IntArray)
cpdef from_list(IntArray, list)
cpdef int get(IntArray, int)
cpdef list to_list(IntArray arr)
