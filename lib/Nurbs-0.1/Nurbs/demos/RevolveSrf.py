# Demonstration of a Revolve surface

from Nurbs import Srf, Crv

crv = Crv.Crv([[0,30,6,90],[0,0,50,50]],[0,0,0,0,1,1,1,1])
srf = Srf.Revolve(crv)
srf.plot()
