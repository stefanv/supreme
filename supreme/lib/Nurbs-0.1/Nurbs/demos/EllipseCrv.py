# Demonstration of a unit circle transformed to a inclined ellipse
# by first scaling, then rotating and finally translating.

import numpy
from Nurbs import Crv
from Nurbs.Util import translate, scale, rotx, roty, deg2rad

xx = scale([1., 2.])
xx = numpy.dot(rotx(deg2rad(45)), xx)
xx = numpy.dot(roty(deg2rad(12)), xx)
xx = numpy.dot(translate([2., 1.]), xx)
crv = Crv.UnitCircle()
crv.trans(xx)
crv.plot()
