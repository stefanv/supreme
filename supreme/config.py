import numpy as N
import os.path

ftype = N.float64
itype = N.int64

relative_data_path = '../data'
data_path = os.path.join(os.path.dirname(__file__),
                         relative_data_path)

class ShapeError(Exception):
    pass
