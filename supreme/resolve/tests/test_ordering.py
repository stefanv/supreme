import numpy as np
from numpy.testing import *

from supreme.resolve.ordering import *
import scipy.sparse as sparse

def test_basic():
    A = sparse.csr_matrix([[0, 1, 0, 2],
                           [2, 0, 1, 1],
                           [0, 0, 0, 1],
                           [0, 0, 1, 0],
                           [0, 0, 0, 0]])

    P = standard_form(A)

    PA = P * A

    assert_array_equal(PA.todense(), [[0, 0, 0, 0],
                                      [2, 0, 1, 1],
                                      [0, 1, 0, 2],
                                      [0, 0, 1, 0],
                                      [0, 0, 0, 1]])
