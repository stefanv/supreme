#!/usr/bin/env python
#       $Id: Polygon.py,v 1.27 2006/04/19 09:41:12 joerg Exp $  

""" Polygon.py - operations on polygons
Polygon.py needs the module cPolygon which implements
polygon storage and clipping using the
General Polygon Clipping Library (gpc)

This module contains all objects from cPolygon and a
few function written in pure python.
"""

from __future__ import generators
import sys
from cPolygon import *
from math import sin, cos, sqrt, fabs, pi
from operator import add
from types import StringTypes

__author__  = author
__version__ = version
__license__ = license


if sys.version_info < (2, 3):
    def enumerate(obj):
        for i, item in zip(range(len(obj)), obj):
            yield i, item


def TriStrip(p):
    """for backward compatibility only - TriStrip is no longer a type
    please use the triStrip() method of the Polygon type instead"""
    return p.triStrip()


def polyStar(radius=1.0, center=(0.0,0.0), nodes=38, iradius=None):
    """polyStar(radius=1.0, center=(0.0,0.0), nodes=38, iradius=None)
    construct stars, circles, triangles etc.
    if iradius is not None, every second point will be set to that radius,
    which will give a star instead of an approximated circle."""
    p = []
    for i in range(nodes):
        a = 2.0*pi*float(i)/nodes
        p.append((center[0]+radius*sin(a), center[1]+radius*cos(a)))
        if iradius:
            b = 2.0*pi*(float(i)+0.5)/nodes
            p.append((center[0]+iradius*sin(b), center[1]+iradius*cos(b)))
    return Polygon(p)


def fillHoles(poly):
    """fillHoles(poly) - return a copy of poly without holes"""
    n = Polygon()
    [n.addContour(poly[i]) for i in range(len(poly)) if poly.isSolid(i)]
    return n


def pointList(poly, withHoles=1):
    """pointList(poly, withHoles=1) - return a flat list of all points in poly.
    Unset withHoles to exclude the points of holes."""
    if not withHoles:
        poly = fillHoles(poly)
    return reduce(add, [list(c) for c in poly])


__left = lambda p: (p[1][0]*p[2][1]+p[0][0]*p[1][1]+p[2][0]*p[0][1]-
                    p[1][0]*p[0][1]-p[2][0]*p[1][1]-p[0][0]*p[2][1] >= 0)
def convexHull(poly):
    """convexHull(poly) - return a simple one-contour Polygon
    which is the convex hull of poly"""
    points = list(pointList(poly, 0))
    points.sort()
    u = [points[0], points[1]]
    for p in points[2:]:
        u.append(p)
        while len(u) > 2 and __left(u[-3:]):
            del u[-2]
    points.reverse()
    l = [points[0], points[1]]
    for p in points[2:]:
        l.append(p)
        while len(l) > 2 and __left(l[-3:]):
            del l[-2]
    return Polygon(u+l[1:-1])


def isCoveredBy(poly, poly1):
    """isCoveredBy(poly, poly1) - returns 1 if poly is completely covered
    by poly1, 0 if not"""
    return not (poly-poly1)


def tile(poly, x=[], y=[], bb=None):
    """tile(poly, x=[], y=[], bb=None) - tile a polygon.
    x and y are lists of the split coordinate values. If you already know the
    bounding box, you may supply it as bb to speed things up a little bit."""
    if not (x or y):
        return [poly] # nothin' to do
    bb = bb or poly.boundingBox()
    x = [bb[0]] + [i for i in x if bb[0] < i < bb[1]] + [bb[1]]
    y = [bb[2]] + [j for j in y if bb[2] < j < bb[3]] + [bb[3]]
    x.sort()
    y.sort()
    cutpoly = []
    for i in range(len(x)-1):
        for j in range(len(y)-1):
            cutpoly.append(Polygon(((x[i],y[j]),(x[i],y[j+1]),(x[i+1],y[j+1]),(x[i+1],y[j]))))
    tmp = [c & poly for c in cutpoly]
    return [p for p in tmp if p]


def tileEqual(poly, nx=1, ny=1, bb=None):
    """tileEqual(poly, nx=1, ny=1, bb=None) - tile a polygon at an regular grid.
    nx and ny are the number of intervals in each direction. If you already know the
    bounding box, you may supply it as bb to speed things up a little bit."""
    bb = bb or poly.boundingBox()
    s0, s1 = bb[0], bb[2]
    a0, a1 = (bb[1]-bb[0])/nx, (bb[3]-bb[2])/ny 
    return tile(poly, [s0+a0*i for i in range(1, nx)], [s1+a1*i for i in range(1, ny)], bb)


def warpToOrigin(poly):
    """warpToOrigin(poly) - shifts lower left corner of the bounding box to origin"""
    x0, x1, y0, y1 = poly.boundingBox()
    poly.shift(-x0, -y0)


def centerAroundOrigin(poly):
    """centerAroundOrigin(poly) - shifts center of the bounding box to origin"""
    x0, x1, y0, y1 = poly.boundingBox()
    poly.shift(-0.5(x0+x1), -0.5*(yo+y1))


__vImp = lambda p: ((sqrt((p[1][0]-p[0][0])**2 + (p[1][1]-p[0][1])**2) +
                     sqrt((p[2][0]-p[1][0])**2 + (p[2][1]-p[1][1])**2)) *
                    fabs(p[1][0]*p[2][1]+p[0][0]*p[1][1]+p[2][0]*p[0][1]-
                              p[1][0]*p[0][1]-p[2][0]*p[1][1]-p[0][0]*p[2][1]))
def reducePoints(cont, n):
    """reducePoints(cont, n) - remove points of the contour 'cont',
    return a new contour with 'n' points.
    *Very simple* approach to reduce the number of points of a contour.
    Each point gets an associated 'value of importance' which is
    the product of the lengths and absolute angle of the left and
    right vertex.
    The points are sorted by this value and the n most important points
    are returned. This method may give *very* bad results for some contours 
    like symmetric figures. It may even produce self-intersecting contours 
    which are not valid to process with this module."""
    if n >= len(cont):
        return cont
    cont = list(cont)
    cont.insert(0, cont[-1])
    cont.append(cont[1])
    a = [(__vImp(cont[i-1:i+2]), i) for i in range(1, len(cont)-1)]
    a.sort()
    ind = [x[1] for x in a[len(cont)-n-2:]]
    ind.sort()
    return [cont[i] for i in ind]


__linVal = lambda p: (p[1][0]-p[0][0])*(p[2][1]-p[0][1])-(p[1][1]-p[0][1])*(p[2][0]-p[0][0])
def prunePoints(poly):
    """prunePoints(poly) - remove unneeded points in the polygon, return a new.
    The new Polygon has no double points or points that are exactly on a straight line."""
    np = Polygon()
    for x in range(len(poly)): # loop over contours
        c = list(poly[x])
        c.insert(0, c[-1])
        c.append(c[1])
        # remove double points
        i = 1
        while (i < (len(c))):
            if c[i] == c[i-1]:
                del c[i]
            else:
                i += 1
        # remove points that are on a straight line
        n = []
        for i in range(1, len(c)-1):
            if __linVal(c[i-1:i+2]) != 0.0:
                n.append(c[i])
        if len(n) > 2:
            np.addContour(n, poly.isHole(x))
    return np


def gnuplotPolygon(filename, *poly):
    """gnuplotPolygon(filename, *poly) - save data of one or more Polygons to a gnuplot data file"""
    f = open(filename, 'w')
    for p in poly:
        for vl in p:
            for j in vl:
                f.write('%g %g\n' % tuple(j))
            f.write('%g %g\n\n' % tuple(vl[0]))
    f.close()


def gnuplotTriStrip(filename, *tri):
    """gnuplotTriStrip(filename, *tri) - save triangles of one or more TriStrips to a gnuplot data file"""
    f = open(filename, 'w')
    for t in tri:
        for vl in t:
            j = 0
            for j in range(len(vl)-2):
                f.write('%g %g \n %g %g \n %g %g \n %g %g\n\n' %
                        tuple(vl[j]+vl[j+1]+vl[j+2]+vl[j]))
            f.write('\n')
    f.close()

    
class __RingBuffer:
    def __init__(self, seq):
        self.s = seq
        self.i = 0
        self.l = len(seq)
    def __call__(self):
        o = self.s[self.i]
        self.i += 1
        if self.i == self.l:
            self.i = 0
        return o

            
def drawSVG(polygons, width=None, height=None, ofile=None, fill_color=None,
                fill_opacity=None, stroke_color=None, stroke_width=None):
    """drawSVG(polygons, width=None, height=None, ofile=None, fill_color=None,
                fill_opacity=None, stroke_color=None, stroke_width=None)
    return a svg representation of the polygons, width and/or height
    will be adapted if not given. If ofile is None, a string is returned,
    else the contents will be written/appended to the file. ofile
    may be an object with a write() method or a filename. fill_color,
    fill_opacity, stroke_color and stroke_width can be sequences
    of the corresponding SVG style attributes to use."""
    poly = [Polygon(p) for p in polygons] # use clones only
    [p.flop(0.0) for p in poly] # adopt to the SVG coordinate system 
    bbs = [p.boundingBox() for p in poly]
    bbs2 = zip(*bbs)
    minx = min(bbs2[0])
    maxx = max(bbs2[1])
    miny = min(bbs2[2])
    maxy = max(bbs2[3])
    xdim = maxx-minx
    ydim = maxy-miny
    if not (xdim or ydim):
        raise Error("Polygons have no extent in one direction!")
    a = ydim / xdim
    if not width and not height:
        if a < 1.0:
            width = 300
        else:
            height = 300
    if width and not height:
        height = width * a
    if height and not width:
        width = height / a
    npoly = len(poly)
    fill_color   = __RingBuffer(fill_color   or ('red', 'green', 'blue', 'yellow'))
    fill_opacity = __RingBuffer(fill_opacity or (1.0,))
    stroke_color = __RingBuffer(stroke_color or ('black',))
    stroke_width = __RingBuffer(stroke_width or (1.0,))
    s = ['<?xml version="1.0" encoding="iso-8859-1" standalone="no"?>',
         '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.0//EN" "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">',
         '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d">' % (width, height)]
    for i in range(npoly):
        p = poly[i]
        bb = bbs[i]
        p.warpToBox(width*(bb[0]-minx)/xdim, width*(bb[1]-minx)/xdim,
                    height*(bb[2]-miny)/ydim, height*(bb[3]-miny)/ydim)
        subl = ['<path style="fill:%s;fill-opacity:%s;fill-rule:evenodd;stroke:%s;stroke-width:%s;" d="' %
                (fill_color(), fill_opacity(), stroke_color(), stroke_width())]
        for c in p:
            subl.append('M %g, %g %s z ' % (c[0][0], c[0][1], ','.join([("L %g, %g" % (a,b)) for a,b in c[1:]])))
        subl.append('"/>')
        s.append(''.join(subl))
    s.append('</svg>')
    svg = '\n'.join(s)
    if ofile is not None:
        if type(ofile) in StringTypes:
            open(ofile, 'w').write(svg)
        else:
            ofile.write(svg)
    else:
        return '\n'.join(s)


def dumpXML(p):
    """dumpXML(p) - return a simple XML representation of the
    polygon p as a string.
    """
    l = ['<polygon contours="%d" area="%g" xMin="%g" xMax="%g" yMin="%g" yMax="%g">' % ((len(p), p.area())+p.boundingBox())]
    for i,c in enumerate(p):
        l.append('  <contour points="%d" isHole="%d" area="%g" xMin="%g" xMax="%g" yMin="%g" yMax="%g">' \
            % ((len(c), p.isHole(i), p.area(i))+p.boundingBox(i)))
        for po in c:
            l.append('    <p x="%g" y="%g"/>' % po)
        l.append('  </contour>')
    l.append('</polygon>\n')
    return '\n'.join(l)


from xml.dom.minidom import parseString, Node
def loadXML(x):
    """loadXML(x) - return a list of Polygon objects built from
    the XML representation in the string x"""
    d = parseString(x)
    plist = []
    for pn in d.getElementsByTagName('polygon'):
        p = Polygon()
        plist.append(p)
        for sn in pn.childNodes:
            if not sn.nodeType == Node.ELEMENT_NODE:
                continue
            assert sn.tagName == 'contour'
            polist = []
            for pon in sn.childNodes:
                if not pon.nodeType == Node.ELEMENT_NODE:
                    continue
                polist.append((float(pon.getAttribute('x')), float(pon.getAttribute('y'))))
            assert int(sn.getAttribute('points')) == len(polist)
            #print type(polist)
            p.addContour(polist, int(sn.getAttribute('isHole')))
            #print type(polist)
        assert int(pn.getAttribute('contours')) == len(p)
    return plist


#
# loadBinary() and dumpBinary() are still in alpha state, the functions
# may become methods of the Polygon type in the future
#
from struct import pack, unpack, calcsize

def __flatten(s):
    for a in s:
        for b in a:
            yield b

def dumpBinary(p):
    """dumpBinary(p) - return a compact binary representation of the
    polygon p as a string. The binary string will be in a standard format
    with network byte order and should be rather machine independant.
    There's no redundancy in the string, any damage will make
    the hole polygon information unusable.
    """
    l = [pack('!I', len(p))]
    for i, c in enumerate(p):
        l.append(pack('!l', len(c)*(1,-1)[p.isHole(i)]))
        l.append(pack('!%dd' %(2*len(c)), *__flatten(c)))
    return "".join(l)

        
def __couples(s):
    for i in range(0, len(s), 2):
        yield s[i], s[i+1]

def __unpack(f, b):
    s = calcsize(f)
    return unpack(f, b[:s]), b[s:]
                        
def loadBinary(b):
    """loadBinary(b) - return a Polygon built from the binary string b.
    If the string is not valid, the whole thing may break...
    """
    nC, b = __unpack('!I', b)
    p = Polygon()
    for i in range(nC[0]):
        x, b = __unpack('!l', b)
        if x[0] < 0:
            isHole = 1
            s = -2*x[0]
        else:
            isHole = 0
            s = 2*x[0]
        flat, b = __unpack('!%dd' % s, b)
        p.addContour(tuple(__couples(flat)), isHole)
    return p

                
## support for pickling and unpickling

def __createPolygon(contour, hole):
    """rebuild Polygon from pickled data"""
    p = Polygon()
    map(p.addContour, contour, hole)
    return p


def __tuples(a):
    """map an array or list of lists to a tuple of tuples"""
    return tuple(map(tuple, a))


def __reducePolygon(p):
    """return pickle data for Polygon """
    return (__createPolygon, (tuple([__tuples(x) for x in p]), p.isHole()))


import copy_reg
copy_reg.constructor(__createPolygon)
copy_reg.pickle(PolygonType, __reducePolygon)
del copy_reg

