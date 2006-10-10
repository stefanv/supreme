#!/usr/bin/env python
# encoding: utf-8
"""Polygon geometry."""

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
        if (x[0] != x[-1] or y[0] != y[-1]):
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

        out = N.empty(len(xp),dtype=bool)
        xpi = self.x[1:]
        ypi = self.y[1:]
        # shift        
        xpj = xpi[N.arange(xpi.size)-1]
        ypj = ypi[N.arange(ypi.size)-1]
        maybe = N.empty(len(xpi),dtype=bool)
        for i,(x,y) in enumerate(zip(xp,yp)):
            maybe[:] = ((ypi <= y) & (y < ypj)) | ((ypj <= y) & (y < ypi))
            out[i] = sum(x < (xpj[maybe]-xpi[maybe])*(y - ypi[maybe]) \
                     / (ypj[maybe] - ypi[maybe]) + xpi[maybe]) % 2

        return out

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
        return abs(0.5 * (self.x[:-1] * self.y[1:] - self.x[1:] * self.y[:-1]).sum())

    def centroid(self):
        """Return the centroid of the polygon

        """
        x,y = self.x,self.y
        c = x[:-1]*y[1:] - x[1:]*y[:-1]
        return N.array([(c * (p[:-1] + p[1:])).sum() for p in x,y]) / (6.0*self.area())
