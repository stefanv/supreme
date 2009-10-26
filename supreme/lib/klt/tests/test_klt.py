from numpy.testing import *
import numpy as np

from supreme.lib import klt

class TestLibklt:
    def test_basic(self):
        img1 = np.zeros((128, 128), dtype=np.uint8)
        img2 = np.zeros((128, 128), dtype=np.uint8)

        rand = lambda x: (np.random.random(x) * x).astype(np.uint8)

        img1[rand(128), rand(128)] = 255
        img2[rand(128), rand(128)] = 255

        tc = klt.TrackingContext()
        fl = klt.FeatureList(100)
        klt.select_good_features(tc, img1, fl)
        klt.track_features(tc, img1, img2, fl)
        fl.to_image(img2)

        assert_equal(len(fl), 100)

        fa = fl.as_array()
        values = fa['val']
        assert 0 <= len(values[values != -1]) <= 100

if __name__ == "__main__":
    run_module_suite()

