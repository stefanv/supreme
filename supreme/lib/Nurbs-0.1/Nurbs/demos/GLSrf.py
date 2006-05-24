from Nurbs import Srf, Crv
import Numeric

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

lastx = 0
lasty = 0

def on_motion(x, y):
	# store the mouse coordinate
	global lastx, lasty
	lastx = x
	lasty = y
	# redisplay
	glutPostRedisplay()

def on_reshape(width, height):
	# setup the viewport
	glViewport(0, 0, width, height)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	aspect = float(width)/float(height)
	if aspect < 1.:
		glOrtho(-10., 20., -10. / aspect, 20. / aspect, -25., 25.)
	else:
		glOrtho(-10. * aspect, 20. * aspect, -10., 20., -25., 25.)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
		
def on_display():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	
	global lastx, lasty
	glRotatef(lastx, 0.0, 1.0, 0.0)
	glRotatef(lasty, 1.0, 0.0, 0.0)
	
	glCallList(1)
	
	glutSwapBuffers()

def main():
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
	glutInitWindowSize(640, 480)
	glutCreateWindow('GLSrf - Press MB and drag to rotate')

	glutMotionFunc(on_motion)
	glutDisplayFunc(on_display)
	glutReshapeFunc(on_reshape)
	
	nurb = gluNewNurbsRenderer()
	gluNurbsProperty(nurb, GLU_SAMPLING_TOLERANCE, 50.)
	gluNurbsProperty(nurb, GLU_DISPLAY_MODE, GLU_FILL)

	glMatrixMode(GL_MODELVIEW)
	
	glNewList(1, GL_COMPILE)
	
	glMaterialfv(GL_FRONT, GL_SPECULAR, ( 1.0, 1.0, 1.0, 1.0 ))
	glMaterialfv(GL_FRONT, GL_SHININESS, 100.0)
	glMaterialfv(GL_FRONT, GL_DIFFUSE, ( 0.7, 0.0, 0.1, 1.0 ))
	glEnable(GL_LIGHTING)
	glEnable(GL_LIGHT0)
	glEnable(GL_DEPTH_TEST)
	glEnable(GL_AUTO_NORMAL)
	glEnable(GL_NORMALIZE)
	
	pnts = [[0., 3., 4.5, 6.5, 8., 10.],
		[0., 0., 0., 0., 0., 0.],
		[2., 2., 7., 4., 6., 4.]]   
	crv1 = Crv.Crv(pnts, [0., 0., 0., 1./3., 0.5, 2./3., 1., 1., 1.])

	pnts= [[0., 3., 5., 8., 10.],
	       [10., 10., 10., 10., 10.],
	       [3., 6., 3., 6., 10.]]
	crv2 = Crv.Crv(pnts, [0., 0., 0., 1./3., 2./3., 1., 1., 1.])

	srf = Srf.Ruled(crv1, crv2)
	
	gluBeginSurface(nurb)
	gluNurbsSurface(nurb, srf.uknots, srf.vknots, Numeric.transpose(srf.cntrl, (1,2,0)), GL_MAP2_VERTEX_4)
	gluEndSurface(nurb)

	glEndList()

if __name__ == '__main__':
	try:
		GLU_VERSION_1_2
	except:
		print "Need GLU 1.2 to run this demo"
		sys.exit(1)
	main()
	glutMainLoop()

