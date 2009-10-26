from numpy.testing import *

from supreme import feature

class TestFeature:
    def test_match(self):
        f = [[0, 1, 2, 3],
             [3, 2, 1, 2],
             [0, 1, 2, 3.1]]
        featureset = [[3, 2, 1, 0],
                      [0, 1, 2, 3],
                      [9, 10, 11, 12],
                      [3, 2, 1, 0.5]]
        match,dists,valid = feature.match(f, featureset)
        assert_equal(match, [1, 3, 1])
        assert_equal(valid, [True, False, True])
        assert_array_almost_equal(dists, [0, 1.5, 0.1])

if __name__ == "__main__":
    run_module_suite()
