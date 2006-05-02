import Polygon
import unittest
import sys

from operator import add
from math import fabs

aTri = lambda a,b,c: 0.5*fabs((b[0]-a[0])*(c[1]-a[1])-(c[0]-a[0])*(b[1]-a[1]))
cTri = lambda a,b,c: ((a[0]+b[0]+c[0])/3.0, (a[1]+b[1]+c[1])/3.0)
def tcenter(poly):
    a = []
    c = []
    for vl in Polygon.TriStrip(poly):
        for i in range(len(vl)-2):
            a.append(aTri(vl[i], vl[i+1], vl[i+2]))
            c.append(cTri(vl[i], vl[i+1], vl[i+2]))
    a = map(lambda x,y=reduce(add, a): x/y, a)
    return reduce(add, map(lambda i,j: i*j[0], a, c)),\
           reduce(add, map(lambda i,j: i*j[1], a, c))


def tarea(poly):
    a = []
    for vl in Polygon.TriStrip(poly):
        for i in range(len(vl)-2):
            a.append(aTri(vl[i], vl[i+1], vl[i+2]))
    return reduce(add, a)


def tboundingBox(poly):
    p = Polygon.pointList(poly, 0)
    x = map(lambda a: a[0], p)
    y = map(lambda a: a[1], p)
    return min(x), max(x), min(y), max(y)


class PolygonTestCase(unittest.TestCase):
    
    def setUp(self):
        star   = Polygon.polyStar(radius=2.0, center=(1.0, 3.0), nodes=5, iradius=1.4)
        circle = Polygon.polyStar(radius=1.0, center=(1.0, 3.0), nodes=64)
        self.cookie = star-circle
        self.cont = ((0.0, 0.0), (2.0, 1.0), (1.0, 0.0), (-2.0, 1.0), (0.0, 0.0))
        
    def testInit(self):
        Polygon.setDataStyle(Polygon.STYLE_TUPLE)
        # tuple
        p = Polygon.Polygon(self.cont)
        self.assertEqual(p[0], self.cont)
        # list
        p = Polygon.Polygon(list(self.cont))
        self.assertEqual(p[0], self.cont)
        if Polygon.withNumeric:
            # array
            import Numeric
            p = Polygon.Polygon(Numeric.array(self.cont))
            self.assertEqual(p[0], self.cont)

    def testDataStyle(self):
        p = Polygon.Polygon(self.cont)
        # tuple
        Polygon.setDataStyle(Polygon.STYLE_TUPLE)
        self.assertEqual(p[0], self.cont)
        # list
        Polygon.setDataStyle(Polygon.STYLE_LIST)
        self.assertEqual(p[0], list(self.cont))
        if Polygon.withNumeric:
            # array
            import Numeric
            Polygon.setDataStyle(Polygon.STYLE_ARRAY)
            self.assertEqual(p[0], Numeric.array(self.cont))

    def testPickle(self):
        import pickle
        p1 = self.cookie
        s = pickle.dumps(p1)
        p2 = pickle.loads(s)
        self.assertEqual(len(p1), len(p2))
        self.assertEqual(repr(p1), repr(p2))

    def testReadWrite(self):
        p1 = self.cookie
        p1.write('cookie.gpf')
        p2 = Polygon.Polygon()
        p2.read('cookie.gpf')
        self.assertEqual(len(p1), len(p2))
        self.assertEqual(repr(p1), repr(p2))

    def testClone(self):
        p1 = self.cookie
        p2 = Polygon.Polygon(p1)
        self.assertEqual(len(p1), len(p2))
        self.assertEqual(repr(p1), repr(p2))

    def testPointContainment(self):
        p = Polygon.Polygon(((0, 0), (0, 3), (5, 3), (5, 0)))
        p.addContour(((3, 1), (3, 2), (4, 2), (4, 1), (3, 1)), 1)
        self.assertEqual(p.isInside(3.5, -0.5), 0)
        self.assertEqual(p.isInside(3.5, 0.5), 1)
        self.assertEqual(p.isInside(3.5, 1.5), 0)
        self.assertEqual(p.isInside(3.5, 2.5), 1)
        self.assertEqual(p.isInside(3.5, 3.5), 0)
        self.assertEqual(p.isInside(3.5, 1.5, 0), 1)
        self.assertEqual(p.isInside(3.5, 1.5, 1), 1)

    def testCoverOverlap(self):
        p1 = Polygon.polyStar(radius=1.0, nodes=6)
        p2 = Polygon.Polygon(p1)
        p2.scale(0.9, 0.9)
        self.assertEqual(p1.covers(p2), 1)
        self.assertEqual(p1.overlaps(p2), 1)
        p2.shift(0.2, 0.2)
        self.assertEqual(p1.covers(p2), 0)
        self.assertEqual(p1.overlaps(p2), 1)
        p2.shift(5.0, 0.0)
        self.assertEqual(p1.covers(p2), 0)
        self.assertEqual(p1.overlaps(p2), 0)

    def testCenterOfGravity(self):
        x, y   = self.cookie.center()
        tx, ty = tcenter(self.cookie)
        self.assertAlmostEqual(x, tx, 10)
        self.assertAlmostEqual(y, ty, 10)
        
    def testArea(self):
        a  = self.cookie.area()
        ta = tarea(self.cookie)
        self.assertAlmostEqual(a, ta, 10)
        
    def testBoundingBox(self):
        bb   = self.cookie.boundingBox()
        tbb  = tboundingBox(self.cookie)
        self.assertEqual(bb, tbb)

    def testPrune(self):
        p1 = Polygon.Polygon(((0.0,0.0), (1.0,1.0), (2.0,2.0), \
                             (3.0,2.0), (3.0, 2.0), (3.0,1.0), \
                             (3.0,0.0), (2.0,0.0)))
        p2 = Polygon.prunePoints(p1)
        self.assertAlmostEqual(p1.area(), p2.area(), 10)

        
if __name__ == '__main__':
    if sys.version_info < (2, 3):
        print "This test works only with python >= 2.3 !"
        sys.exit(1)
    unittest.main()
