#!/usr/bin/env python
# encoding: utf-8
"""Polygon geometry.

Copyright (C) 2006, Stefan van der Walt
Copyright (C) 2006, Robert Hetland

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

import numpy as N
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
        x = N.asarray(xp,dtype=N.float64)
        y = N.asarray(yp,dtype=N.float64)

        assert x.shape == y.shape, 'Need the same number of x and y coordinates'
        assert x.ndim == 1, 'Vertices should be a 1-dimensional array, but is %s' % str(x.shape)
        assert len(x) >= 3, 'Need 3 vertices to create polygon.'
        
        # close polygon
        x = N.append(x,x[0])
        y = N.append(y,y[0])

        self.x = x
        self.y = y
            
    def __str__(self):
        return 'Polygon: %d vertices' % len(self.x)
    
    def __repr__(self):
        return "Polygon_%d_%d_%d" % (len(self.x),
                                     self.x.__array_interface__['data'][0],
                                     self.y.__array_interface__['data'][0])
    
    def _inside(self,xp,yp):
        """Check whether the given points are in the polygon.
        
        Input:
          xp -- 1D array of x coordinates for points
          yp -- 1D array of y coordinates for points
          
        Output:
          inside -- boolean array

        See http://www.ecse.rpi.edu/Homepages/wrf/Research/Short_Notes/pnpoly.html
        
        """

        out = []
        xpi = self.x[1:]
        ypi = self.y[1:]
        # shift        
        xpj = xpi[N.arange(xpi.size)-1]
        ypj = ypi[N.arange(ypi.size)-1]
        maybe = N.empty(len(xpi),dtype=bool)
        for x,y in zip(xp,yp):
            maybe[:] = ((ypi <= y) & (y < ypj)) | ((ypj <= y) & (y < ypi))
            out.append(sum(x < (xpj[maybe]-xpi[maybe])*(y - ypi[maybe]) \
                           / (ypj[maybe] - ypi[maybe]) + xpi[maybe]) % 2)

        return N.asarray(out,dtype=bool)

    def inside(self,xp,yp):
        """Check whether the given points are inside the polygon.
        
        Input:
          xp -- 1D array of x coordinates for points
          yp -- 1D array of y coordinates for points
          
        Output:
          inside -- boolean array
        
        See http://www.ecse.rpi.edu/Homepages/wrf/Research/Short_Notes/pnpoly.html

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
        return N.array([(c * (p[:-1] + p[1:])).sum() for p in x,y]) / (6.0*self.area())
