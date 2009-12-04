#cython: cdivision=True
# -*- python -*-

cimport int_array
cimport stdlib

from int_array cimport HEAP_SIZE

cdef class IntArray:
    """See int_array.pxd for members.

    """
    def __cinit__(self):
        self.cap = HEAP_SIZE
        self.buf = self.heapbuf
        self.size = 0

    def __dealloc__(self):
        if self.buf != self.heapbuf:
            stdlib.free(self.buf)

cpdef inline append(IntArray arr, int x):
    if arr.size == arr.cap:
        # Array is full -- allocate new memory
        grow(arr, arr.cap * 2)

    arr.buf[arr.size] = x
    arr.size += 1

cpdef int max(IntArray arr):
    cdef int i,  m = arr.buf[0]
    for i in range(1, arr.size):
        if arr.buf[i] > m:
            m = arr.buf[i]

    return m

cpdef int min(IntArray arr):
    cdef int i, m = arr.buf[0]
    for i in range(1, arr.size):
        if arr.buf[i] < m:
            m = arr.buf[i]

    return m

cdef inline grow(IntArray arr, int cap):
    """Grow the underlying array storage so that it can
    store `cap` elements.

    """
    cdef int* new_buf
    cdef int i

    if cap <= arr.size:
        return

    arr.cap = cap
    new_buf = <int*>stdlib.malloc(sizeof(int) * cap)

    for i in range(arr.size):
        new_buf[i] = arr.buf[i]

    if arr.buf != arr.heapbuf:
        stdlib.free(arr.buf)

    arr.buf = new_buf

cpdef copy(IntArray src, IntArray dst):
    cdef int i

    grow(dst, src.size)

    dst.size = 0
    for i in range(src.size):
        append(dst, src.buf[i])

cpdef from_list(IntArray arr, list ii):
    if ii is not None:
        arr.size = 0
        for i in ii:
            append(arr, i)

cpdef int get(IntArray arr, int idx):
    return arr.buf[idx]

cpdef list to_list(IntArray arr):
    cdef list out = []
    cdef int i

    for i in range(arr.size):
        out.append(arr.buf[i])

    return out
