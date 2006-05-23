# Demonstration of a Extrude surface

from Nurbs import Srf, Crv

cntrl = [[-50., -75., 25., 0., -25., 75., 50.],
         [25., 50., 50., 0., -50., -50., 25.]]
knots = [0., 0., 0., .2, .4, .6, .8, 1., 1., 1.]
crv = Crv.Crv(cntrl, knots)
srf = Srf.Extrude(crv,[0,0,5])
srf.plot()
