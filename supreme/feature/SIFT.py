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

def match_features(features,featureset,threshold=0.6):
    """Find the most closely matched feature from a feature-set.

    Input:
    ------
    features -- An array of M row-wise features of length N

    featureset -- An array of any number of row-wise features of
                  length N.  Typically field 'data' of the record
                  array produced by SIFT.fromfile.

    Output:
    -------
    nearest -- An array of indices into featureset.

    distances -- Distances between the provided features and the
                 closest features in featureset.

    valid -- A boolean array indicating whether the given feature
             match is valid, according to the criterion described in
             the SIFT README. It states that a match is valid when the
             match is less than 0.6 times the distance to the
             second-closest match.

    See original implementation by Tim Hochberg at

    http://thread.gmane.org/gmane.comp.python.numeric.general/8459/focus=8459

    """
    features,featureset = map(N.asarray,[features,featureset])

    # We want to find the minimum distance
    #
    # N.sqrt((b - a)^2),
    #
    # which is the same as finding the minimum distance
    #
    # (b - a)^2 or
    # 1/2 (b - a)^2 which is
    # b^2/2 - a*b + a^2
    #
    # but since a is constant, we minimise over
    #
    # b^2/2 - a*b

    features_T = features.transpose().copy()
    totals = N.empty([len(featureset),len(features)],float)
    featureset2 = (featureset**2).sum(-1)
    featureset2 *= 0.5
    totals[:] = featureset2[:, N.newaxis]
    for feat,tot in zip(featureset,totals):
        for di,ci in zip(features_T,feat):
            tot -= di*ci

    totals = N.sqrt(totals*2 + (features**2).sum(-1))

    # Pick closest match
    match = totals.argmin(axis=0)
    nrange = N.arange(len(features))
    match_dist = totals[match,nrange]

    # Increase distance to closest match so we can find the
    # second-closest match
    totals[match,nrange] = N.inf
    match2 = totals.argmin(axis=0)
    match2_dist = totals[match2,nrange]
    valid_matches = (match_dist <= threshold*match2_dist)

    return match, match_dist, valid_matches
