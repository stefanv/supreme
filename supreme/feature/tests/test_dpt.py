import numpy as np
from numpy.testing import *

import supreme.feature as sf
import supreme.lib.dpt as dpt

def test_basic():
    x = np.zeros((100, 100), dtype=int)
    x[50, 50] = 1
    F, A = sf.dpt.features(dpt.decompose(x), x.shape)

    assert_equal(np.unravel_index(np.argmax(F), F.shape), [50, 50])

if __name__ == "__main__":
    run_module_suite()
