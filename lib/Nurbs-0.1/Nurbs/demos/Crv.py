# Demonstration of a curve

from Nurbs import Crv

cntrl = [[-50., -75., 25., 0., -25., 75., 50.],
         [25., 50., 50., 0., -50., -50., 25.]]
knots = [0., 0., 0., .2, .4, .6, .8, 1., 1., 1.]

crv = Crv.Crv(cntrl, knots)
crv.plot()
