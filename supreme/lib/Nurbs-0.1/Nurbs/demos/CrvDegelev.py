# Demonstration of degelev function

from Nurbs import Crv

cntrl = [[.5, 1.5, 4.5, 3., 7.5, 6., 8.5],
        [3., 5.5, 5.5, 1.5, 1.5, 4., 4.5]]

crv = Crv.Crv(cntrl, [0., 0., 0., 1./4., 1./2., 3./4., 3./4., 1., 1., 1.])
crv.plot()
crv.degelev(1)
crv.plot()
