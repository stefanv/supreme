import math

dependencies = '''This module requires:
	Numeric Python
'''

try:
    import numpy
except ImportError, value:
    print dependencies
    raise

def uniformknots(cntrlpts, degree):
    knots = numpy.zeros(degree + cntrlpts + 1, numpy.Float)
    knots[cntrlpts:] = 1.
    knots[degree+1:cntrlpts] = numpy.arange(1., cntrlpts-degree)* (1./(cntrlpts - degree))
    return knots

def translate(txyz):
    ret = numpy.identity(4).astype(numpy.Float)
    ret[0:len(txyz), 3] = txyz
    return ret

def scale(sxyz):
    ret = numpy.identity(4).astype(numpy.Float)
    s = numpy.ones(3, numpy.Float)
    s[0:len(sxyz)] = sxyz
    ret[0,0] = s[0]
    ret[1,1] = s[1]
    ret[2,2] = s[2]
    return ret

def deg2rad(angle):
    return math.pi * angle / 180.

def rad2deg(angle):
    return angle * 180./math.pi

def rotx(angle):
    ret = numpy.identity(4).astype(numpy.Float)
    ret[1,1] = ret[2,2] = numpy.cos(angle)
    sn = numpy.sin(angle)
    ret[1,2] = -sn
    ret[2,1] = sn
    return ret

def roty(angle):
    ret = numpy.identity(4).astype(numpy.Float)
    ret[0,0] = ret[2,2] = numpy.cos(angle)
    sn = numpy.sin(angle)
    ret[0,2] = sn
    ret[2,0] = -sn
    return ret

def rotz(angle):
    ret = numpy.identity(4).astype(numpy.Float)
    ret[0,0] = ret[1,1] = numpy.cos(angle)
    sn = numpy.sin(angle)
    ret[0,1] = -sn
    ret[1,0] = sn
    return ret

def rotxyz(angles):
    ret = numpy.identity(4).astype(numpy.Float)
    
    ret[1,1] = ret[2,2] = numpy.cos(angles[0])
    sn = numpy.sin(angles[0])
    ret[1,2] = -sn
    ret[2,1] = sn
    
    cs = numpy.cos(angles[1])
    ret[0,0] = cs
    ret[2,2] += cs
    sn = numpy.sin(angles[1])
    ret[0,2] = sn
    ret[2,0] = -sn

    cs = numpy.cos(angles[2])
    ret[0,0] += cs
    ret[1,1] += cs
    sn = numpy.sin(angles[2])
    ret[0,1] = -sn
    ret[1,0] = sn
    return ret

