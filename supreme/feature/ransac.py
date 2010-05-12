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

    def __init__(self, model=None, p_inlier=0.5):
        """
        Construct a RANSAC model fitter.

        Parameters
        ----------
        model : Model
            Model describing inlier data.
        p_inlier : float (0..1)
            Probability that any data point is an inlier.

        """
        assert model is not None

        self.model = model
        self.p_inlier = p_inlier

    def __call__(self, data=None, inliers_required=None, confidence=None,
                 max_iter=None, T=None, LO_RANSAC=None, min_iter=100):
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
        max_iter : int
            Hard limit on the maximum number of iterations.  By default,
            the algorithms figures out a sufficient number of iterations.
        T : float
            Penalty applied for each outlier, according to MSAC. By default,
            T is set to 1.  Note that `T` must be large enough to
            *increment* the error when a point moves from being an inlier
            to an outlier, otherwise outliers are preferred by
            RANSAC.

        Other Parameters
        ----------------
        LO_RANSAC : ndarray of bool
            Used in the implementation of LO-RANSAC, this variable provide
            the inliers for the inner RANSAC loop.

        """
        if confidence is None:
            confidence = 0.8 # sensible default value

        if T is None:
            T = 1

        model = self.model
        L = len(data)

        if max_iter is None:
            max_iter = max(3 * np.ceil(
                self.p_inlier ** (-model.ndp)).astype(int),
                           min_iter)

        if LO_RANSAC is None:
            log.debug("Maximum number of RANSAC iterations: %i" % max_iter)

        success = False
        best_set = None
        best_err = np.inf
        i = 0
        while i < max_iter:
            i += 1

            if LO_RANSAC is not None:
                M = np.sum(LO_RANSAC)
                from_data = data[LO_RANSAC, ...]
            else:
                M = L
                from_data = data

            rand_idx = np.floor(
                np.random.random(model.ndp) * M).astype(int)

            model.parameters, res = model.estimate(from_data[rand_idx,...])

            score, inliers = model(data, confidence=confidence)
            inliers_found = np.sum(inliers)

            err = np.sum(score[inliers]) + (L - inliers_found) * T

            if err < best_err:
                best_set = inliers
                best_err = err

                if np.sum(inliers) > 1.5 * model.ndp and \
                   (LO_RANSAC is None):
                    new_best_set, new_best_err = self(data, confidence,
                                                      max_iter=10, T=T,
                                                      LO_RANSAC=inliers)

                    if new_best_err < best_err:
                        best_err = new_best_err
                        best_set = new_best_set

            ip = np.sum(best_set) / float(L)
            new_max = np.log(0.1) / np.log(1 - ip**model.ndp)
            if new_max < max_iter and new_max > min_iter:
                max_iter = new_max
                log.debug("Maximum iterations down-adjusted to %d." % max_iter)


        if LO_RANSAC is not None:
            return best_set, best_err

        if np.sum(best_set) == 0:
            raise RuntimeError('RANSAC did not converge')

        log.info("RANSAC terminated after %s iterations "
                 "with %s inliers (%s requested). Best error "
                 "was %.2f." % (i, np.sum(best_set),
                               inliers_required, best_err))

        return model.estimate(data[best_set, ...])
