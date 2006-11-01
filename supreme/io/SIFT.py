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
    feature -- feature values

    """
    nr_features,feature_len = map(int,f.readline().split())
    data = N.fromfile(f,sep=' ')
    if data.size != nr_features * (feature_len + 4):
        raise IOError("Invalid SIFT feature file.")

    dtype = [('row',float),('column',float),
             ('scale',float),('orientation',float),
             ('feature',(float,feature_len))]

    return data.view(dtype)


