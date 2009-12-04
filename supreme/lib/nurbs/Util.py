import math

dependencies = '''This module requires:
	Numeric Python
'''

try:
    import numpy.oldnumeric as numerix
except ImportError, value:
    print dependencies
    raise

def uniformknots(cntrlpts, degree):
    knots = numerix.zeros(degree + cntrlpts + 1, numerix.Float)
    knots[cntrlpts:] = 1.
    knots[degree+1:cntrlpts] = numerix.arange(1., cntrlpts-degree)* (1./(cntrlpts - degree))
    return knots

def translate(txyz):
    ret = numerix.identity(4).astype(numerix.Float)
    ret[0:len(txyz), 3] = txyz
    return ret

def scale(sxyz):
    ret = numerix.identity(4).astype(numerix.Float)
    s = numerix.ones(3, numerix.Float)
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
    ret = numerix.identity(4).astype(numerix.Float)
    ret[1,1] = ret[2,2] = numerix.cos(angle)
    sn = numerix.sin(angle)
    ret[1,2] = -sn
    ret[2,1] = sn
    return ret

def roty(angle):
    ret = numerix.identity(4).astype(numerix.Float)
    ret[0,0] = ret[2,2] = numerix.cos(angle)
    sn = numerix.sin(angle)
    ret[0,2] = sn
    ret[2,0] = -sn
    return ret

def rotz(angle):
    ret = numerix.identity(4).astype(numerix.Float)
    ret[0,0] = ret[1,1] = numerix.cos(angle)
    sn = numerix.sin(angle)
    ret[0,1] = -sn
    ret[1,0] = sn
    return ret

def rotxyz(angles):
    ret = numerix.identity(4).astype(numerix.Float)
    
    ret[1,1] = ret[2,2] = numerix.cos(angles[0])
    sn = numerix.sin(angles[0])
    ret[1,2] = -sn
    ret[2,1] = sn
    
    cs = numerix.cos(angles[1])
    ret[0,0] = cs
    ret[2,2] += cs
    sn = numerix.sin(angles[1])
    ret[0,2] = sn
    ret[2,0] = -sn

    cs = numerix.cos(angles[2])
    ret[0,0] += cs
    ret[1,1] += cs
    sn = numerix.sin(angles[2])
    ret[0,1] = -sn
    ret[1,0] = sn
    return ret

