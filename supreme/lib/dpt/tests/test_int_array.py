import numpy as np
from numpy.testing import run_module_suite

import lulu.int_array as iarr
from lulu.int_array import IntArray

def test_init():
    x = IntArray()

def test_append():
    x = IntArray()
    iarr.append(x, 3)

def test_size_increase():
    x = IntArray()
    for i in range(1000):
        iarr.append(x, 3)

def test_copy():
    x = IntArray()
    for i in range(1000):
        iarr.append(x, i)

    y = IntArray()
    for i in range(1000):
        iarr.append(y, 1000 - i)

    iarr.copy(x, y)

    assert iarr.get(y, 0) == 0

def test_from_list():
    x = IntArray()
    iarr.from_list(x, range(15))
    assert iarr.get(x, 0) == 0
    assert iarr.get(x, 14) == 14

def test_min():
    x = IntArray()
    iarr.from_list(x, [1, 5, -2, 9, 12])
    assert iarr.min(x) == -2
    assert iarr.max(x) == 12

if __name__ == "__main__":
    run_module_suite()
