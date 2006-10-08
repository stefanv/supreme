"""
Create two 10x10 grids, one rotated and translated.
Calculate and display the overlap of a single block.
"""

from numpy.testing import set_local_path, restore_path
import numpy as N
import pylab as P
from matplotlib import patches

set_local_path('../../..')
from supreme.geometry import Polygon
from supreme import ext
restore_path()


def plotgrid(grid, mode='k-'):
    for b in grid:
        P.plot(b.x, b.y, mode)

grid1 = []
for col in range(10):
    for row in range(10):
        grid1.append(Polygon([row,row+1,row+1,row,row],
                             [col,col,col+1,col+1,col]))
        
theta = 3/180.0*N.pi
t_x = 0.04
t_y = 0.04

tf = N.array([[N.cos(theta), -N.sin(theta), t_x],
             [N.sin(theta),  N.cos(theta), t_y],
             [0,             0,            1]], 'd')

# Create grid2 as a rotated version of grid1
grid2 = []
for poly in grid1:
    coords = N.empty((3,len(poly.x)))
    coords[0] = poly.x
    coords[1] = poly.y
    coords[2] = 1.
    coords = N.dot(tf, coords).transpose()

    grid2.append(Polygon(coords[:,0], coords[:,1]))

def plot_deformed_grid():
    plotgrid(grid2)
    P.axis('equal')
    P.xticks([])
    P.yticks([])
    P.axis([-2,12,-2,12])
    P.show()

def plot_overlap(N):
    # Select an overlapping pixel and highlight it
    p1 = grid1[N]
    p2 = grid2[N]
    overlap = zip(*ext.poly_clip(p2.x, p2.y,
                                 p1.x.min(), p1.x.max(),
                                 p1.y.max(), p1.y.min()))
    
    ax = P.subplot(111)
    ax.add_patch(patches.Polygon(zip(p1.x,p1.y), facecolor=[0.7, 0.7, 0.9]))
    ax.add_patch(patches.Polygon(zip(p2.x,p2.y), facecolor=[0.9, 0.8, 0.9]))
    ax.add_patch(patches.Polygon(overlap, facecolor=[0.3,0.9,0.3]))#facecolor=[0.9, 0.7, 0.7]))    

    plotgrid(grid1, 'r-')
    plotgrid(grid2, 'b-')
    P.axis('equal')
    P.xticks([])
    P.yticks([])
    P.axis([-2,12,-2,12])
    P.show()

plot_overlap(54)
