#!/usr/bin/env python
# encoding: utf-8
"""Polygon geometry.

Copyright (C) 2006, Robert Hetland
Copyright (C) 2006, Stefan van der Walt

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the
   distribution.
3. The name of the author may not be used to endorse or promote
   products derived from this software without specific prior written
   permission.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
"""

import numpy as np
import string
import sys
import math

import supreme.ext

__all__ = ['Polygon']

class Polygon:
    """
    Polygon class
    """

    def __init__(self, xp, yp):
        """
        Given xp and yp (both 1D arrays or sequences), create a new
        polygon.  The polygon is closed at instantiation.
        
        p.inside(x, y) - Calculate whether points lie inside the polygon.
        p.area() - The area enclosed by the polygon.
        p.centroid() - The centroid of the polygon
        
        """
        x = np.asarray(xp,dtype=np.float64)
        y = np.asarray(yp,dtype=np.float64)

        assert x.shape == y.shape, 'Need the same number of x and y coordinates'
        assert x.ndim == 1, 'Vertices should be a 1-dimensional array, but is %s' % str(x.shape)
        assert len(x) >= 3, 'Need 3 vertices to create polygon.'
        
        # close polygon
        x = np.append(x,x[0])
        y = np.append(y,y[0])

        self.x = x
        self.y = y
            
    def __str__(self):
        return 'Polygon: %d vertices' % len(self.x)
    
    def __repr__(self):
        return "Polygon_%d_%d_%d" % (len(self.x),
                                     self.x.__array_interface__['data'][0],
                                     self.y.__array_interface__['data'][0])
    
    def _inside(self,xp,yp):
        """Check whether given points are in the polygon.

        See http://www.ecse.rpi.edu/Homepages/wrf/Research/Short_Notes/pnpoly.html    
        """

        out = []
        xpi = self.x[1:]
        ypi = self.y[1:]
        # shift        
        xpj = xpi[np.arange(xpi.size)-1]
        ypj = ypi[np.arange(ypi.size)-1]
        maybe = np.empty(len(xpi),dtype=bool)
        for x,y in zip(xp,yp):
            maybe[:] = ((ypi <= y) & (y < ypj)) | ((ypj <= y) & (y < ypi))
            out.append(sum(x < (xpj[maybe]-xpi[maybe])*(y - ypi[maybe]) \
                           / (ypj[maybe] - ypi[maybe]) + xpi[maybe]) % 2)

        return np.asarray(out,dtype=bool)

    def inside(self,xp,yp):
        """Return true if (xp,yp) is inside the polygon.

        """
        return supreme.ext.npnpoly(self.x,self.y,xp,yp).astype(bool)
    
    def area(self):
        """
        Return the area of the polygon.

        From Paul Bourke's webpage:
          http://astronomy.swin.edu.au/~pbourke/geometry
          
        """
        return 0.5 * (self.x[:-1] * self.y[1:] - self.x[1:] * self.y[:-1]).sum()

    def centroid(self):
        """Return the centroid of the polygon

        """
        x,y = self.x,self.y
        c = x[:-1]*y[1:] - x[1:]*y[:-1]
        return np.array([(c * (p[:-1] + p[1:])).sum() for p in x,y]) / (6.0*self.area())

if __name__ == '__main__':
    import pylab as pl
    grid_y, grid_x = np.mgrid[0:1:0.1,0:1:0.1].reshape(2,-1)
    
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
    pl.plot(grid_x[inside], grid_y[inside], 'g.')
    pl.plot(grid_x[~inside], grid_y[~inside],'r.')
    pl.plot(pb.x,pb.y, '-k')    
    pl.plot([xc], [yc], 'co')
    pl.show()
    
    # many points in a semicircle, to test speed
    grid_x,grid_y = np.mgrid[0:1:.01,-1:1:.01].reshape(2,-1)
    
    xp = np.sin(np.arange(0,np.pi,0.01))
    yp = np.cos(np.arange(0,np.pi,0.01))
    pc = Polygon(xp,yp)
    xc, yc = pc.centroid()
    
    print pc
    print "Area: ", pc.area()
    print "Centroid: ", xc, yc    
    print "%d points inside %d vertex poly..." % (grid_x.size/2,len(pc.x)),
    sys.stdout.flush()
    inside = pc.inside(grid_x,grid_y)
    print "done."
    
    pl.plot(grid_x[inside], grid_y[inside], 'g.')
    pl.plot(grid_x[~inside], grid_y[~inside], 'r.')
    pl.plot(pc.x, pc.y, '-k')
    pl.plot([xc], [yc], 'co')
    pl.show()
