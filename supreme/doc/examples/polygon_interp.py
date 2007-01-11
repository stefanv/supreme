import os.path

from numpy.testing import set_local_path, restore_path
import numpy as N
import pylab as P

set_local_path('../../..')
import supreme as sr
from supreme.config import data_path
restore_path()

fn0 = sr.imread(os.path.join(data_path,'NASA/hubble_crop.jpg'),flatten=True)
fn1 = sr.imread(os.path.join(data_path,'NASA/hubble_crop_rot5.jpg'),flatten=True)

def build_array(theta,tx,ty,s):
    A = N.array([[N.cos(theta),-N.sin(theta),tx],
                 [N.sin(theta),N.cos(theta),ty],
                 [0,0,1]])
    A[:2,:] *= s
    return A

scale = 1.
tf_matrices = [build_array(0,0,0,1./scale),
               build_array(-5/180.*N.pi,0,0,1./scale)]
print "Transformation matrix:\n", tf_matrices
oshape = N.array(fn0.shape)*int(scale)

out = N.empty(oshape,float)
print "Stacking..."
sign = 1
for img,M in zip([fn0,fn1],tf_matrices):
    out += sign * sr.ext.interp_transf_polygon(img,M,oshape)
    sign *= -1

P.imshow(N.abs(out),cmap=P.cm.gray)
P.show()
