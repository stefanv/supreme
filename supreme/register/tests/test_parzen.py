import numpy as np
from numpy.testing import *

from supreme.io import imread
from supreme.register.parzen import joint_hist, mutual_info

h1 = (np.random.random((100, 100)) * 255).astype(np.uint8)

def test_basic():
    H = joint_hist(h1, h1, std=1)

    D = np.zeros((255, 255), dtype=np.bool)
    for i in range(-3, 3):
        m = np.diag(np.ones(255 - abs(i)), k=i).astype(np.bool)
        D[m] = 1

    assert_almost_equal(np.sum(H[D]), 0.97, decimal=1)
    assert_almost_equal(np.sum(H[~D]), 0.03, decimal=1)

def test_mutual_info():
    H = joint_hist(h1, h1)
    S = mutual_info(H)

    assert(S > 5)

if __name__ == "__main__":
    run_module_suite()
