"""
Display paths on an image, using coord_path builder.
"""

import numpy as np
import matplotlib.pyplot as plt
import os.path

import supreme
import supreme.misc
from supreme.geometry import coord_path as cp
from supreme.config import data_path

def add_path(img,p,col=[1.,0,0]):
    img[p[:,0],p[:,1]] = np.array(col)*255

def add_line(img,c0,c1,col=[1.,0,0]):
    p = cp.build(cp.line(c0,c1))
    add_path(img,p,col)

img = supreme.misc.imread(os.path.join(data_path, 'toystory/toystory000.png'))
shape = np.array(img.shape[:2])-1
height,width = shape
centre = shape/2.
add_line(img,(0,0),centre)
add_line(img,centre,(0,width),[0.,1,0])
add_line(img,centre,(height,width),[.9,.6,.6])
add_line(img,centre,(height,0),[.4,.7,.8])
add_path(img,cp.build(cp.circle(centre,50)),[0.9,0.9,0])

add_path(img,cp.build(cp.spline(((0,0),(height,80),(140,200),(150,80)))),
         [0.9,0.9,0.9])

add_path(img,cp.build(cp.spline(((0,0),(height/2.,0),(height/2.,width),(height,width)))),
         [0.6,0.7,0.9])

plt.imshow(img,interpolation='nearest')
plt.title('Trajectories of several coordinate paths')
plt.show()
