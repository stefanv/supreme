import numpy as N
from numpy.testing import *

from tempfile import TemporaryFile

set_local_path('../../..')
from supreme import io
restore_path()

class test_SIFT(NumpyTestCase):
    def check_read(self):
        f = TemporaryFile()
        f.write('''2 128
133.92 135.88 14.38 -2.732
 3 12 23 38 10 15 78 20 39 67 42 8 12 8 39 35 118 43 17 0
 0 1 12 109 9 2 6 0 0 21 46 22 14 18 51 19 5 9 41 52
 65 30 3 21 55 49 26 30 118 118 25 12 8 3 2 60 53 56 72 20
 7 10 16 7 88 23 13 15 12 11 11 71 45 7 4 49 82 38 38 91
 118 15 2 16 33 3 5 118 98 38 6 19 36 1 0 15 64 22 1 2
 6 11 18 61 31 3 0 6 15 23 118 118 13 0 0 35 38 18 40 96
 24 1 0 13 17 3 24 98
132.36 99.75 11.45 -2.910
 94 32 7 2 13 7 5 23 121 94 13 5 0 0 4 59 13 30 71 32
 0 6 32 11 25 32 13 0 0 16 51 5 44 50 0 3 33 55 11 9
 121 121 12 9 6 3 0 18 55 60 48 44 44 9 0 2 106 117 13 2
 1 0 1 1 37 1 1 25 80 35 15 41 121 3 0 2 14 3 2 121
 51 11 0 20 93 6 0 20 109 57 3 4 5 0 0 28 21 2 0 5
 13 12 75 119 35 0 0 13 28 14 37 121 12 0 0 21 46 5 11 93
 29 0 0 3 14 4 11 99''')
        f.seek(0)
        data = io.SIFT.fromfile(f)
        f.close()

        assert_equal(len(data),2)
        assert_equal(len(data['feature'][0]),128)
        assert_equal(data['row'][0],133.92)
        assert_equal(data['column'][1],99.75)

if __name__ == "__main__":
    NumpyTest().run()
