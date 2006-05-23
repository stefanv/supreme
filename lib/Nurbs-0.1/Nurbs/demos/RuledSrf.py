# Demonstration of a Ruled surface

from Nurbs import Srf, Crv

pnts = [[0., 3., 4.5, 6.5, 8., 10.],
        [0., 0., 0., 0., 0., 0.],
        [2., 2., 7., 4., 6., 4.]]   
crv1 = Crv.Crv(pnts, [0., 0., 0., 1./3., 0.5, 2./3., 1., 1., 1.])

pnts= [[0., 3., 5., 8., 10.],
       [10., 10., 10., 10., 10.],
       [3., 6., 3., 6., 10.]]
crv2 = Crv.Crv(pnts, [0., 0., 0., 1./3., 2./3., 1., 1., 1.])

srf = Srf.Ruled(crv1, crv2)
srf.plot()
