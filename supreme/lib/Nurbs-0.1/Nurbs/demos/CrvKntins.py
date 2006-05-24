# Demonstration of kntins function

from Nurbs import Crv

cntrl = [[.5, 1.5, 4.5, 3., 7.5, 6., 8.5],
        [3., 5.5, 5.5, 1.5, 1.5, 4., 4.5]]

crv = Crv.Crv(cntrl, [0., 0., 0., 1./4., 1./2., 3./4., 3./4., 1., 1., 1.])
crv.plot()
crv.kntins([0.125, 0.375, 0.625, 0.875])
crv.plot()
