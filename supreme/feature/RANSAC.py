"""RANdom SAmple Consensus

Martin A. Fischler and Robert C. Bolles,
"Random sample consensus: a paradigm for model fitting with applications to
image analysis and automated cartography",
Communications of the ACM, 1981

"""

__all__ = ['IModel','RANSAC']

from supreme.config import get_log
log = get_log(__name__)

import numpy as np

class IModel:
    """This class defines the structure for a model.

    Attributes
    ----------
    parameters : tuple, ndarray, any
        Model parameters.  RANSAC attempts to find the model parameters that
        best fit the data.
    ndp : int
        Number of defining points: the minimum number of points
        required to estimate the model parameters (e.g., 2 for a line)

    """
    parameters = None
    ndp = 0

    def __call__(data, confidence=0):
        """Evaluate data fit.

        Parameters
        ----------
        data : array
            Data points as row vectors.
        confidence : float
            Value between 0 and 1 indicating how well a point must fit
            the model to be considered an inlier.  A value of zero
            implies almost any data point is considered fitting the
            model.

        Returns
        -------
        score : array of float
            Fit of data points to model.
        inlier : array of bool
            Whether a data point is an inlier or not.

        """

    def estimate(data):
        """Estimate model parameters from data.

        Parameters
        ----------
        data : array
            Data points as row vectors.

        Returns
        -------
        parameters:
           Model parameters in any format the model can interpret.
        residual : float
           Measure of data fit.

        """

class RANSAC(object):
    """RANdom SAmple Consensus"""

    def __init__(self, model=None, p_inlier=None):
        """
        Parameters
        ----------
        model : Model
            Model describing inlier data.
        p_inlier : float (0..1)
            Probability that any data point is an inlier.

        """
        for param in [model, p_inlier]:
            assert param is not None

        self.model = model
        self.p_inlier = p_inlier

    def __call__(self, data=None, inliers_required=None, confidence=None,
                 T=None):
        """Execute RANSAC.

        Parameters
        ----------
        data : MxN array
            M data points as row features.
        inliers_required : int
            Number of inliers (in addition to those randomly chosen)
            needed to successfully terminate RANSAC.
        confidence : float (0..1)
            How well a point must fit the model to be considered
            an inlier.  A value of zero implies almost any data
            point fits the model, while one implies that it must
            lie exactly on the model prediction.
        T : float
            Penalty applied for each outlier, according to MSAC. By default,
            T is set to `confidence`.

        """
        for param in [data, inliers_required]:
            assert param is not None

        if confidence is None:
            confidence = 0.8 # sensible default value

        if T is None:
            T = confidence

        model = self.model
        L = len(data)

        max_iter = 3 * np.ceil(self.p_inlier ** (-model.ndp)).astype(int)
        log.debug("Maximum number of RANSAC iterations: %i" % max_iter)

        success = False
        best_set = None
        best_err = np.inf
        i = 0
        while i < max_iter:
            i += 1

            rand_idx = np.floor(
                np.random.random(model.ndp) * L).astype(int)
            model.parameters,res = model.estimate(data[rand_idx, ...])
            score, inliers = model(data, confidence=confidence)

            ip = np.sum(inliers) / float(L)
            new_max = np.log(0.01) / np.log(1 - ip**model.ndp)
            if new_max < max_iter:
                max_iter = new_max

            inliers_found = np.sum(inliers)
            err = np.sum(score[inliers]) + (L - inliers_found) * T

            if err < best_err:
                best_set = inliers
                best_err = err

        if np.sum(best_set) == 0:
            raise RuntimeError('RANSAC did not converge')

        log.info("RANSAC terminated after %s iterations "
                 "with %s inliers (%s requested). Best error "
                 "was %.2f." % (i, np.sum(best_set),
                               inliers_required, best_err))

        np.savetxt('/tmp/ransac.txt', data[best_set,...])

        data = data[best_set,...]
        return model.estimate(data)
