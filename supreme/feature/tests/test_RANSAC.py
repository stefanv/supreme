from numpy.testing import *
import numpy as np

from supreme.feature import RANSAC
from supreme.misc.inject import interface

class Line(object):
    """y = mx + c

    :SeeAlso:

        - supreme.feature.RANSAC

    """
    @property
    def ndp(self): return 2

    def __init__(self, m, c):
        self.parameters = m, c

    def set_parameters(self, (m, c)):
        assert np.isscalar(m), "m should be scalar, is %s" % m
        assert np.isscalar(c), "c should be scalar, is %s" % c
        self._params = (m, c)

    def get_parameters(self):
        return self._params

    parameters = property(fget=get_parameters, fset=set_parameters)

    def __call__(self, data, confidence=0.8):
        m, c = self.parameters
        err = np.array(len(data), dtype=float)
        err = np.abs(data[:,1] - m*data[:,0] - c)
        return err, err <= (1-confidence) * m

    def generate(self, (x_min, x_max), inliers, outliers,
                 noise, noise_bias=0):
        """Generate points around the line.

        :Parameters:
            (x_min,x_max) : tuple of floats
                Range of generated points.
            inliers : int
                Number of inlying points.
            outliers : int
                Number of outlying points.
            noise : float
                Maximum deviation of outlier noise.
            noise_bias : float between -0.5 and 0.5
                0 is on the line, anything else biases the noise
                above or below.

        :Returns:
            data : Mx2 array of float
                Points around the line.

        """
        m, c = self.parameters
        data_x = np.random.random(inliers + outliers) * \
                 (x_max - x_min) + x_min
        data_y = m * data_x + c
        data_y[inliers:] = data_y[inliers:] + \
                           (np.random.random(outliers) - 0.5 + noise_bias) *\
                           2 * noise
        return np.column_stack((data_x, data_y))

    def estimate(self, data):
        a = data[:, 0]
        a = np.column_stack((a, np.ones(len(a))))
        b = data[:, 1]
        x, res, rank, s = np.linalg.lstsq(a, b)
        return x, res

interface(Line, RANSAC.IModel)

class TestRansac:
    def test_linefit(self):
        # Experiment parameters
        m,x = 5, 3
        inliers = 80
        outliers = 40

        # Setup model and generate data
        line = Line(m, x)
        xrange = np.array([20, 100])
        data = line.generate(xrange, inliers, outliers, 50, 0.25)

        # Determine parameters using ransac
        (rsc_m, rsc_c), res = RANSAC.RANSAC(model=line,
                                            p_inlier=0.66)\
                              (data=data, inliers_required=30, confidence=0.9)

        # Determine parameters without RANSAC
        (m, c), res = line.estimate(data)

##         # Visualise test
##         import pylab as P
##         x = data[:,0]
##         y = data[:,1]
##         P.plot(x[:inliers],y[:inliers],'b.',label='Inliers')
##         P.plot(x[inliers:],y[inliers:],'r.',label='Outliers')
##         P.plot(xrange,xrange*m + c,':k',label='Estimation based on all data')
##         P.plot(xrange,xrange*rsc_m + rsc_c,'g',label='Estimation based on RANSAC')
##         P.legend()
##         P.show()
##         P.close()

        assert_array_almost_equal((rsc_m,rsc_c),line.parameters,decimal=1,
             err_msg='Note: this is a statistical test and may fail sometimes')

if __name__ == "__main__":
    run_module_suite()

