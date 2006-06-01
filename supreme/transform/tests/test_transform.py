import numpy as N
import pylab as P
from numpy.testing import *

set_local_path('../../..')
from supreme.transform import *
import supreme.config as SC
restore_path()

class test_transform(NumpyTestCase):
    def check_logpolar(self,level=1):
        x = N.array((3,3))
        z = logpolar(x)
        assert_equal(x.shape,z.shape)

if __name__ == "__main__":
    NumpyTest().run()
