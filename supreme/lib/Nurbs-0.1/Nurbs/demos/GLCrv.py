from Nurbs import Crv
import numpy

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
	
	glMatrixMode(GL_MODELVIEW)
	
	glNewList(1, GL_COMPILE)
	
	cntrl = [[-5., -7.5, 2.5, 0, -2.5, 7.5, 5.0],
                 [2.5, 5.0, 5.0, .0, -5.0, -5.0, 2.5]]
	knots = [0., 0., 0., .2, .4, .6, .8, 1., 1., 1.]
	crv = Crv.Crv(cntrl, knots)
	
	glPointSize(10.)
	glDisable(GL_LIGHTING)
	glColor3f(1., 1., 1.)

	glBegin(GL_POINTS)
	for i in range(crv.cntrl.shape[1]):
		w = crv.cntrl[-1,i]
		glVertex3f(crv.cntrl[0, i]/w, crv.cntrl[1, i]/w, crv.cntrl[2, i]/w)
	glEnd()
	
	glBegin(GL_LINE_STRIP)
	for i in range(crv.cntrl.shape[1]):
		w = crv.cntrl[-1,i]
		glVertex3f(crv.cntrl[0, i]/w, crv.cntrl[1, i]/w, crv.cntrl[2, i]/w)
	glEnd()
	
	glColor3f(1., 1., 0.)
	gluBeginCurve(nurb)
	gluNurbsCurve(nurb, crv.uknots, numpy.transpose(crv.cntrl), GL_MAP1_VERTEX_4)
	gluEndCurve(nurb)

	glEndList()

if __name__ == '__main__':
	try:
		GLU_VERSION_1_2
	except:
		print "Need GLU 1.2 to run this demo"
		sys.exit(1)
	main()
	glutMainLoop()

