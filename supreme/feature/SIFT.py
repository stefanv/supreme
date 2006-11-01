import numpy as N

def fromfile(f):
    """Read SIFT features from a file.

    Input:
    ------
    file -- Open file object.

    Output:
    -------
    Record array with fields

    row -- row position of feature
    column -- column position of feature
    scale -- feature scale
    orientation -- feature orientation
    data -- feature values

    """
    nr_features,feature_len = map(int,f.readline().split())
    data = N.fromfile(f,sep=' ')
    if data.size != nr_features * (feature_len + 4):
        raise IOError("Invalid SIFT feature file.")

    datatype = [('row',float),('column',float),
                ('scale',float),('orientation',float),
                ('data',(float,feature_len))]
    return data.view(datatype)

def match_features(features,featureset):
    """Find the most closely matched feature from a feature-set.

    Input:
    ------
    features -- An array of M row-wise features of length N
    featureset -- An array of any number of row-wise features of
                  length N.  Typically field 'data' of the record
                  array produced by SIFT.fromfile.

    Output:
    -------
    A list of M indices into featureset.

    See original implementation by Tim Hochberg at

    http://thread.gmane.org/gmane.comp.python.numeric.general/8459/focus=8459

    """
    features,featureset = map(N.asarray,[features,featureset])

    nr_features = len(featureset)
    features_T = features.transpose().copy()
    totals = N.empty([nr_features,len(features)],float)
    featureset2 = (featureset**2).sum(-1)
    featureset2 *= -0.5
    totals[:] = featureset2[:, N.newaxis]
    for feat, tot in zip(featureset, totals):
        for di, ci in zip(features_T, feat):
            tot += di*ci

    return totals.argmax(axis=0)
