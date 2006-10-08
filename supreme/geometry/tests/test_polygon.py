import numpy as N
from numpy.testing import *

set_local_path('../../..')
from supreme import geometry as G
from supreme.config import ftype,itype
restore_path()

class test_polygon(NumpyTestCase):
    def check_area(self,level=1):
        p = G.Polygon([1,0,1],[1,0,0])
        assert_equal(p.area(),0.5)
        
        p = G.Polygon([0,1,1],[0,1,0])        
        assert_equal(p.area(),0.5)

    def check_centroid(self,level=1):
        p = G.Polygon([0,1,1,0],[0,0,1,1])        
        assert_equal(p.centroid(),[0.5,0.5])

    def check_inside(self,level=1):
        p = G.Polygon([0,1,1,0],[0,0,1,1])        
        assert_equal(p.inside(0.5,0.5),True)

        x = [-0.5,0.5,1.5]
        y = [0.5,0.5,0.5]
        assert_equal(p.inside(x,y),[False,True,False])

if __name__ == "__main__":
    NumpyTest().run()
