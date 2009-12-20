import os.path

import numpy as np
import matplotlib.pyplot as plt

import supreme as sr
import supreme.io
from supreme.config import data_path

fn0 = sr.io.imread(os.path.join(data_path,'NASA/hubble_crop.jpg'),flatten=True)
fn1 = sr.io.imread(os.path.join(data_path,'NASA/hubble_crop_rot5.jpg'),flatten=True)

def build_array(theta,tx,ty,s):
    A = np.array([[np.cos(theta),-np.sin(theta),tx],
                  [np.sin(theta), np.cos(theta),ty],
                  [0,0,1]])
    A[:2,:] *= s
    return A

scale = 2.
tf_matrices = [build_array(0,0,0,1./scale),
               build_array(-5/180.*np.pi,0,0,1./scale)]
print "Transformation matrix:\n", tf_matrices
oshape = np.array(fn0.shape)*int(scale)
print oshape

out = np.empty(oshape,float)
print "Stacking..."
sign = 1
for img,M in zip([fn0,fn1],tf_matrices):
    out += sign * sr.ext.interp_transf_polygon(img,M,oshape)
    sign *= -1

plt.imshow(np.abs(out), cmap=plt.cm.gray)
plt.show()
