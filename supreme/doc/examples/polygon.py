# Example originally contributed by Robert Hetland

import numpy as N
import pylab as P
from numpy.testing import set_local_path, restore_path

import sys

set_local_path('../../..')
import supreme
from supreme.geometry import Polygon
restore_path()

grid_y, grid_x = N.mgrid[0:1:0.1,0:1:0.1].reshape(2,-1)

# simple area test
xp = [0.15,0.85,0.85,0.15]
yp = [0.15,0.15,0.85,0.85]

pa = Polygon(xp,yp)
print pa
print "Area expected: %f, area found: %f" % ((0.85-0.15)**2, pa.area())
print "Centroid: ", pa.centroid()
print

# concave enclosure test-case for inside.
xp = [0.15,0.25,0.45,0.45,0.25,0.25,0.65,0.65,0.85,0.85,0.15]
yp = [0.15,0.15,0.15,0.25,0.25,0.55,0.55,0.15,0.15,0.85,0.85]
pb = Polygon(xp,yp)
xc, yc = pb.centroid()
print pb
print "Area: ", pb.area()
print "Centroid: ", xc, yc
print

inside = pb.inside(grid_x,grid_y)
P.plot(grid_x[inside], grid_y[inside], 'g.')
P.plot(grid_x[~inside], grid_y[~inside],'r.')
P.plot(pb.x,pb.y, '-k')    
P.plot([xc], [yc], 'co')
P.show()

# many points in a semicircle, to test speed
grid_x,grid_y = N.mgrid[0:1:.01,-1:1:.01].reshape(2,-1)

xp = N.sin(N.arange(0,N.pi,0.01))
yp = N.cos(N.arange(0,N.pi,0.01))
pc = Polygon(xp,yp)
xc, yc = pc.centroid()

print pc
print "Area: ", pc.area()
print "Centroid: ", xc, yc    
print "%d points inside %d vertex poly..." % (grid_x.size/2,len(pc.x)),
sys.stdout.flush()
inside = pc.inside(grid_x,grid_y)
print "done."

P.plot(grid_x[inside], grid_y[inside], 'g.')
P.plot(grid_x[~inside], grid_y[~inside], 'r.')
P.plot(pc.x, pc.y, '-k')
P.plot([xc], [yc], 'co')
P.show()
