# Demonstration of a Arc curve

import math
from Nurbs import Crv

crv = Crv.Arc(1.,None,0,math.pi/2.)
crv.plot()
