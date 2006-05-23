# Demonstration of a bilinear surface

from Nurbs import Srf
srf = Srf.Bilinear([0, 0, .25], [2, 0, 0], [0, 1, 0], [2, 1, 1.8])
srf.plot()