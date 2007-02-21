"""Read SIFT and SURF feature files."""

import numpy as N

def fromfile(f,mode='SIFT'):
    """Read SIFT or SURF features from a file.

    Input:
    ------
    f : string or open file
        Input file.
    mode : string
        'SIFT' or 'SURF'

    Output:
    -------
    data : record array with fields
      - row: int
          row position of feature
      - column: int
          column position of feature
      - scale: float
          feature scale
      - orientation: float
          feature orientation
      - data: array
          feature values

    """
    if not hasattr(f,'readline'):
        f = file(f,'r')

    if mode == 'SIFT':
        nr_features,feature_len = map(int,f.readline().split())
        datatype = N.dtype([('row',float),('column',float),
                            ('scale',float),('orientation',float),
                            ('data',(float,feature_len))])
    else:
        mode = 'SURF'
        feature_len = int(f.readline()) - 1
        nr_features = int(f.readline())
        datatype = N.dtype([('column',float),('row',float),
                            ('second_moment',(float,3)),
                            ('sign',float),('data',(float,feature_len))])
    data = N.fromfile(f,sep=' ')
    if data.size != nr_features * datatype.itemsize/N.dtype(float).itemsize:
        raise IOError("Invalid %s feature file." % mode)

    return data.view(datatype)
