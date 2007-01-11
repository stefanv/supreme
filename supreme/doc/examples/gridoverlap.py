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

grid1 = []
for col in range(10):
    for row in range(10):
        grid1.append(Polygon([row,row+1,row+1,row,row],
                             [col,col,col+1,col+1,col]))
        
theta = 3/180.0*N.pi
t_x = 0.04
t_y = 0.04

def tf(angle,offset_x,offset_y):
    return N.array([[N.cos(angle), -N.sin(angle), offset_x],
                    [N.sin(angle),  N.cos(angle), offset_y],
                    [0,             0,            1]], float)

def poly_coords(p):
    coords = N.empty((3,len(p.x)))
    coords[0] = p.x
    coords[1] = p.y
    coords[2] = 1.

    return coords

# Create grid2 as a rotated version of grid1
grid2 = []
for poly in grid1:
    coords = poly_coords(poly)
    coords = N.dot(tf(theta,t_x,t_y), coords).transpose()

    grid2.append(Polygon(coords[:,0], coords[:,1]))
    

def plotgrid(ax, grid, mode='k-'):
    P.axis('off')
    for b in grid:
        ax.plot(b.x, b.y, mode)

def plot_overlap(n):
    # Select an overlapping pixel and highlight it
    p1 = grid1[n]
    p2 = grid2[n]
    overlap = zip(*ext.poly_clip(p2.x, p2.y,
                                 p1.x.min(), p1.x.max(),
                                 p1.y.max(), p1.y.min()))
    
    ax = P.subplot(121)
    ax.add_patch(patches.Polygon(zip(p1.x,p1.y), facecolor=[0.7, 0.7, 0.9]))
    ax.add_patch(patches.Polygon(zip(p2.x,p2.y), facecolor=[0.9, 0.8, 0.9]))
    ax.add_patch(patches.Polygon(overlap, facecolor=[0.3,0.9,0.3]))

    plotgrid(ax, grid1, 'r-')
    plotgrid(ax, grid2, 'b-')
    ax.axis('equal')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis([-2,12,-2,12])

    f = P.subplot(122).get_frame()
#    print [f.get_x(),f.get_y(),f.get_width()/2,f.get_height()/2]    
#    P.axes()

    coords = poly_coords(Polygon([0,1,1,0],[0,0,1,1]))
    angles = N.linspace(-N.pi,N.pi,50)
    offsets = N.linspace(-1,1.5,50)
    weights = N.zeros((len(angles),len(offsets)))
    print "Calculating overlaps..."
    for i,theta in enumerate(angles):
        for j,offset in enumerate(offsets):
            x,y = N.dot(tf(theta,offset,offset), coords)[:2]
            x,y = ext.poly_clip(x,y,0,1,1,0)
            if len(x) >= 3:
                weights[i,j] = Polygon(x,y).area()
                
    
    P.rcParams['figure.figsize'] = (6.67,3.335)
    P.imshow(weights)
    P.subplots_adjust(wspace=0.4)
    P.xlabel("Offset")
    P.ylabel("Angle")
    P.xlim([0,50])
    P.ylim([0,50])
    P.xticks([0,25,50],('-1','0.25','1.5'))
    P.yticks([0,25,50],('$\pi$','0','$-\pi$'))
    P.savefig('gridoverlap.eps')

plot_overlap(54)
P.show()
