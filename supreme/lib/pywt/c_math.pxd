# Copyright (c) 2006-2009 Filip Wasilewski <http://filipwasilewski.pl/>
# See COPYING for license details.

# $Id: c_math.pxd 117 2009-05-02 20:25:59Z filipw $

cdef extern from "math.h":
    double sqrt (double x)
    double exp (double x)
    double pow (double x, double y)
