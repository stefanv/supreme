import numpy as N
from numpy.testing import *

set_local_path('../../..')
from supreme import register
from supreme.config import ftype,itype
restore_path()

class test_logpolar(NumpyTestCase):
    def check_blah(self):
        pass

if __name__ == "__main__":
    NumpyTest().run()
