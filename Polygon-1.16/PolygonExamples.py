#!/usr/bin/env python

from Polygon import *
import random, math

# polyStar() is used very often here because the polygons it produces
# are very nice to use as examples

def operationsExample():
    # create a circle with a hole
    p1 = polyStar() - polyStar(radius=0.5)
    # create a square
    p2 = polyStar(radius=0.7, nodes=4)
    # shift the square a little bit
    p2.shift(0.25, 0.35)
    plist = [p1, p2]

    # addition, the same as logical OR (p1 | p2)
    p = p1 + p2
    p.shift(2.5, 0.0)
    plist.append(p)

    # subtraction
    p = p1 - p2
    p.shift(5.0, 0.0)
    plist.append(p)

    # subtraction
    p = p2 - p1
    p.shift(7.5, 0.0)
    plist.append(p)

    # logical AND
    p = p2 & p1
    p.shift(10.0, 0.0)
    plist.append(p)

    # logical XOR
    p = p2 ^ p1
    p.shift(12.5, 0.0)
    plist.append(p)

    # draw the results of the operations
    print "Plotting Operations.svg"
    drawSVG(plist, width=800, ofile='Operations.svg')


def cookieExample():
    # construct a christmas cookie with the help of the
    # polyStar() function
    star   = polyStar(radius=2.0, center=(1.0, 3.0), nodes=5, iradius=1.4)
    circle = polyStar(radius=1.0, center=(1.0, 3.0), nodes=64)
    cookie = star-circle
    # shift star and circle to the right to plot all polygons
    # on one page
    star.shift(5.0, 0.0)
    circle.shift(10.0, 0.0)
    # plot all three to an svg file
    print "Plotting Cookie.svg"
    drawSVG((cookie, star, circle), ofile="Cookie.svg")

    # break a polygon object into a list of polygons by arranging
    # it on tiles
    # tile into 3x3 parts
    plist = tileEqual(cookie, 3, 3)
    print "Plotting CookieTiled.svg"
    drawSVG(plist, ofile='CookieTiled.svg')
    # test tile at x = 0.3, 0.5 and y = 2.7, 3.1
    plist = tile(cookie, [0.3, 0.5], [2.7, 3.1])
    print "Plotting CookieTiled2.svg"
    drawSVG(plist, ofile='CookieTiled2.svg')

    # let's simulate an explosion, move all parts away
    # from the cookie's center, small parts are faster
    xc,yc = cookie.center()
    for p in plist:
        if p:
            # speed/distance
            dval = 0.1 / p.area()
            x, y = p.center()
            # move the part a little bit
            p.shift(dval*(x-xc), dval*(y-yc))
            # and rotate it slightly ;-)
            p.rotate(0.2*math.pi*(random.random()-0.5))
    print "Plotting CookieExploded.svg"
    drawSVG(plist, ofile='CookieExploded.svg')
    

def reduceExample():
    # read Polygon from file
    p = Polygon('testpoly.gpf')
    # use ireland only, I know it's contour 0
    pnew = Polygon(p[0])
    # number of points
    l = len(pnew[0])
    # get shift value to show many polygons in drawing
    bb = pnew.boundingBox()
    xs = 1.1 * (bb[1]-bb[0])
    # list with polygons to plot
    plist = [pnew]
    while l > 30:
        # reduce points to the half
        l /= 2
        print "Reducing contour to %d points" % l
        pnew = Polygon(reducePoints(pnew[0], l))
        pnew.shift(xs, 0)
        plist.append(pnew)
    # draw the results
    print "Plotting ReduceExample.svg"
    drawSVG(plist, height=400, ofile="ReduceTest.svg")


def moonExample():
    # a high-resolution, softly flickering moon,
    # constructed by the difference of two stars ...
    moon = polyStar(radius=3, center=(1.0, 2.0), nodes=140, iradius=2.90) \
           - polyStar(radius=3, center=(-0.3, 2.0), nodes=140, iradius=2.90)
    # plot the moon and its convex hull
    print "Plotting MoonAndHull.svg"
    drawSVG((moon, convexHull(moon)), height=400, ofile="MoonAndHull.svg",
            fill_opacity=(1.0, 0.3))
    # test point containment
    d = ['outside', 'inside']
    c = moon.center()
    print 'Did you know that the center of gravitation of my moon is %s?' % d[moon.isInside(c[0], c[1])]


def xmlExample():
    cookie = polyStar(radius=2.0, center=(1.0, 3.0), nodes=5, iradius=1.4) -\
        polyStar(radius=1.0, center=(1.0, 3.0), nodes=64)
    xml = dumpXML(cookie)
    f = open('cookie.xml', 'w')
    f.write('<?xml version="1.0" encoding="iso-8859-1" standalone="no"?>\n')
    f.write(xml)
    f.close()
    print "Wrote cookie to 'cookie.xml' in xml format"
    print cookie
    p = loadXML(xml)
    if len(p) == 1:
        print p[0]
    else:
        "Something went wrong!"

        
def binaryExample():
    cookie = polyStar(radius=2.0, center=(1.0, 3.0), nodes=5, iradius=1.4) -\
        polyStar(radius=1.0, center=(1.0, 3.0), nodes=64)
    b = dumpBinary(cookie)
    p = loadBinary(b)

    
def sizeTestExample():
    import pickle
    p = Polygon('testpoly.gpf')
    p.write('sizetest.gpf')
    tlen = len(open('sizetest.gpf', 'r').read())
    blen = len(dumpBinary(p))
    xlen = len(dumpXML(p))
    plen = len(pickle.dumps(p))
    print "Text(gpc): %d, Binary: %d, XML: %d, Pickle: %d" % (tlen, blen, xlen, plen)


if __name__ == '__main__':
    operationsExample()
    cookieExample()
    reduceExample()
    moonExample()
    xmlExample()
    binaryExample()
    sizeTestExample()