cimport numpy as np

cdef imin(int a, int b)
cdef imax(int a, int b)
cpdef np.ndarray sat(np.ndarray X)
cpdef np.uint64_t sat_sum(np.ndarray sat, int r0, int c0, int r1, int c1)
cpdef np.ndarray window_wrap(int m0, int n0, int m1, int n1,
                             int rows, int cols)
cpdef ncc(np.ndarray imgS, np.ndarray imgT)
