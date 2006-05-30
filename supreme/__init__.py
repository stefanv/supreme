# Supreme module initialisation

from numpy.testing import NumpyTest

from config import *
import geometry
import transform
import scipy

imread = scipy.misc.pilutil.imread
test = NumpyTest('supreme').test

