import numpy as N

def fromfile(f):
    """Read SIFT or SURF features from a file.

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
        raise IOError("Invalid SIFT or SURF feature file.")

    datatype = [('row',float),('column',float),
                ('scale',float),('orientation',float),
                ('data',(float,feature_len))]
    return data.view(datatype)
