# Create two 10x10 grids, one rotated and translated
# Calculate and display the overlap
# Each block in the grid is a polygon

from numarray import array, transpose, matrixmultiply
from pylab import *
from math import pi, cos, sin
from Polygon import Polygon, pointList
from matplotlib import patches

def plotgrid(grid, mode='k-'):
    for b in grid:
        x = [c[0] for c in b[0]]
        y = [c[1] for c in b[0]]
        plot(x,y, mode)

grid1 = []
for col in range(10):
    for row in range(10):
        grid1.append(Polygon([(row,col),(row+1,col),
                                   (row+1,col+1), (row, col+1),
                                   (row,col)]))
        
theta = 3/180.0*pi
t_x = 0.04
t_y = 0.04

tf = array([[cos(theta), -sin(theta), t_x],
            [sin(theta),  cos(theta), t_y],
            [0,                0,                1]], 'd')

# Create grid2 as a rotated version of grid1
grid2 = []
for poly in grid1:
    new_coords = []
    for point in poly[0]:
        coord = array([ [point[0]], [point[1]], [1] ], 'd')
        coord = matrixmultiply(tf, coord).transpose()
        new_coords.append(coord[0, 0:2])

    grid2.append(Polygon(new_coords))

def plot_deformed_grid():
    plotgrid(grid2)
    axis('equal')
    xticks([])
    yticks([])
    axis([-2,12,-2,12])
    show()

def plot_overlap():
    # Select an overlapping pixel and highlight it
    N = 54
    overlap = grid1[N] & grid2[N]
    
    pl1 = pointList(grid1[N] - overlap)
    pl2 = pointList(grid2[N] - overlap)
    pl3 = pointList(overlap)

    ax = subplot(111)
    ax.add_patch(patches.Polygon(pl1, facecolor=[0.9, 0.7, 0.7]))
    ax.add_patch(patches.Polygon(pl2, facecolor=[0.7, 0.7, 0.9]))
    ax.add_patch(patches.Polygon(pl3, facecolor=[0.9, 0.8, 0.9]))

    plotgrid(grid1, 'r-')
    plotgrid(grid2, 'b-')
    axis('equal')
    xticks([])
    yticks([])
    axis([-2,12,-2,12])
    show()

#plot_deformed_grid()
plot_overlap()
