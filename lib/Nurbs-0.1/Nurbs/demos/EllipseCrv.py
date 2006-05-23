# Demonstration of a unit circle transformed to a inclined ellipse
# by first scaling, then rotating and finally translating.

import Numeric
from Nurbs import Crv
from Nurbs.Util import translate, scale, rotx, roty, deg2rad

xx = scale([1., 2.])
xx = Numeric.dot(rotx(deg2rad(45)), xx)
xx = Numeric.dot(roty(deg2rad(12)), xx)
xx = Numeric.dot(translate([2., 1.]), xx)
crv = Crv.UnitCircle()
crv.trans(xx)
crv.plot()
