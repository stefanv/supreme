import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches

import supreme
from supreme.ext import poly_clip

def plotpoly(x,y,mode='-'):
    x = np.append(x,x[0])
    y = np.append(y,y[0])
    plt.plot(x,y,mode)

def plotclip(x,y,xleft,xright,ytop,ybottom):
    boxx = [xleft,xright,xright,xleft,xleft]
    boxy = [ytop,ytop,ybottom,ybottom,ytop]
    pcx, pcy = poly_clip(x, y, xleft, xright, ytop, ybottom)
    plotpoly(boxx, boxy, 'r-')
    plotpoly(x,y)
    plt.gca().add_patch(patches.Polygon(zip(x,y), alpha=0.4))
    plt.gca().add_patch(patches.Polygon(zip(boxx,boxy), alpha=0.4, facecolor=[1,0,0]))
    plt.gca().add_patch(patches.Polygon(zip(pcx,pcy), linewidth=0, facecolor=[1,1,1]))

ax = plt.subplot(111)

plotclip([-3, 3, -3, -3, 10, 12, 1, 5,  19, 5,  17.5, 5,  5,  3,  3],
         [11, 5, 5,  -3, 10, 8, -3, -3, 11, 11, 18.5, 13, 18, 18, 11+42/15.],
         0, 10, 15, 0)

plotclip([15, 20, 20, 15],
         [0,  0, 5,  5],
         16, 19, 3, -3)

plt.axis('equal')
plt.show()
