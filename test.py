#!/usr/bin/env python

#    e-------f
#   /|      /|
#  / |     / |
# a-------b  |
# |  |    |  |
# |  g----|--h
# | /     | /
# c-------d

#
# This code was created by Richard Campbell '99 (ported to Python/PyOpenGL by John Ferguson and Tony Colston 2000)
# To be honst I stole all of John Ferguson's code and just added the changed stuff for lesson 5. So he did most
# of the hard work.
#
# The port was based on the PyOpenGL tutorial module: dots.py  
#
# If you've found this code useful, please let me know (email John Ferguson at hakuin@voicenet.com).
# or Tony Colston (tonetheman@hotmail.com)
#
# See original source and C based tutorial at http:#nehe.gamedev.net
#
# Note:
# -----
# This code is not a good example of Python and using OO techniques.  It is a simple and direct
# exposition of how to use the Open GL API in Python via the PyOpenGL package.  It also uses GLUT,
# which in my opinion is a high quality library in that it makes my work simpler.  Due to using
# these APIs, this code is more like a C program using function based programming (which Python
# is in fact based upon, note the use of closures and lambda) than a "good" OO program.
#
# To run this code get and install OpenGL, GLUT, PyOpenGL (see http:#www.python.org), and NumPy.
# Installing PyNumeric means having a C compiler that is configured properly, or so I found.  For 
# Win32 this assumes VC++, I poked through the setup.py for Numeric, and chased through disutils code
# and noticed what seemed to be hard coded preferences for VC++ in the case of a Win32 OS.  However,
# I am new to Python and know little about disutils, so I may just be not using it right.
#
# NumPy is not a hard requirement, as I am led to believe (based on skimming PyOpenGL sources) that
# PyOpenGL could run without it. However preformance may be impacted since NumPy provides an efficient
# multi-dimensional array type and a linear algebra library.
#
# BTW, since this is Python make sure you use tabs or spaces to indent, I had numerous problems since I 
# was using editors that were not sensitive to Python.
#
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys

# Some api in the chain is translating the keystrokes to this octal string
# so instead of saying: ESCAPE = 27, we use the following.
ESCAPE 	= '\033'
LEFT		= '\037'
UP 			= '\038'
RIGHT 	= '\039'
DOWN 		= '\040'

# Number of the glut window.
window = 0

# Rotation angle for the triangle. 
rtri = 0.0

# Rotation angle for the quadrilateral.
rquad = 0.0
rquadSum = 0.0

#    e-------f
#   /|      /|
#  / |     / |
# a-------b  |
# |  |    |  |
# |  g----|--h
# | /     | /
# c-------d

vertices = {}
vertices['a'] = [-1.0,  1.0,  1.0]
vertices['b'] = [ 1.0,  1.0,  1.0]
vertices['c'] = [-1.0, -1.0,  1.0]
vertices['d'] = [ 1.0, -1.0,  1.0]
vertices['e'] = [-1.0,  1.0, -1.0]
vertices['f'] = [ 1.0,  1.0, -1.0]
vertices['g'] = [-1.0, -1.0, -1.0]
vertices['h'] = [ 1.0, -1.0, -1.0]
vNames = ['a','b','c','d','e','f','g','h']
currentV = 0
currentTime = 0


# A general OpenGL initialization function.  Sets all of the initial parameters. 
def InitGL(Width, Height):				# We call this right after our OpenGL window is created.
		glClearColor(0.0, 0.0, 0.0, 0.0)	# This Will Clear The Background Color To Black
		glClearDepth(1.0)					# Enables Clearing Of The Depth Buffer
		glDepthFunc(GL_LESS)				# The Type Of Depth Test To Do
		glEnable(GL_DEPTH_TEST)				# Enables Depth Testing
		glShadeModel(GL_SMOOTH)				# Enables Smooth Color Shading
	
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()					# Reset The Projection Matrix
										# Calculate The Aspect Ratio Of The Window
		gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)

		glMatrixMode(GL_MODELVIEW)

# The function called when our window is resized (which shouldn't happen if you enable fullscreen, below)
def ReSizeGLScene(Width, Height):
		if Height == 0:						# Prevent A Divide By Zero If The Window Is Too Small 
			Height = 1

		glViewport(0, 0, Width, Height)		# Reset The Current Viewport And Perspective Transformation
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
		glMatrixMode(GL_MODELVIEW)

# The main drawing function. 
def DrawGLScene():
	global rtri, rquad, rquadSum, vertices, vNames, currentV, currentTime

	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);	# Clear The Screen And The Depth Buffer
	glLoadIdentity()								# Reset The View

	
	glTranslatef(0.0, 0.0, -7.0)		# Move Right And Into The Screen

	rquad += rquadSum
	glRotatef(rquad,1.0,1.0,1.0)		# Rotate The Cube On X, Y & Z

	currentTime = (currentTime + 0.5)%10
	if currentTime < 5:
		glBegin(GL_TRIANGLES)       # Drawing Using Triangles
		glColor3f(1.0,1.0,1.0)			# Set The Color To Violet
		glVertex3f( vertices[vNames[currentV]][0]     , vertices[vNames[currentV]][1]+0.05,vertices[vNames[currentV]][2])
		glVertex3f( vertices[vNames[currentV]][0]-0.05, vertices[vNames[currentV]][1]-0.05,vertices[vNames[currentV]][2])
		glVertex3f( vertices[vNames[currentV]][0]+0.05, vertices[vNames[currentV]][1]-0.05,vertices[vNames[currentV]][2])
		glEnd()                            				 # Finished Drawing The Triangle

	glBegin(GL_QUADS)								# Start Drawing The Cube

	# TOP face
	glColor3f(0.0,1.0,0.0)			# Set The Color To Blue
	glVertex3f(vertices['a'][0],vertices['a'][1],vertices['a'][2])
	glVertex3f(vertices['b'][0],vertices['b'][1],vertices['b'][2])
	glVertex3f(vertices['f'][0],vertices['f'][1],vertices['f'][2])
	glVertex3f(vertices['e'][0],vertices['e'][1],vertices['e'][2])

	# BOTTOM face
	# glColor3f(1.0,0.5,0.0)			# Set The Color To Orange
	# glVertex3f(vertices['c'][0],vertices['c'][1],vertices['c'][2])
	# glVertex3f(vertices['d'][0],vertices['d'][1],vertices['d'][2])
	# glVertex3f(vertices['h'][0],vertices['h'][1],vertices['h'][2])
	# glVertex3f(vertices['g'][0],vertices['g'][1],vertices['g'][2])

	# FRONT face
	glColor3f(1.0,0.0,0.0)			# Set The Color To Red
	glVertex3f(vertices['a'][0],vertices['a'][1],vertices['a'][2])
	glVertex3f(vertices['b'][0],vertices['b'][1],vertices['b'][2])
	glVertex3f(vertices['d'][0],vertices['d'][1],vertices['d'][2])
	glVertex3f(vertices['c'][0],vertices['c'][1],vertices['c'][2])

	# BACK face
	# glColor3f(1.0,1.0,0.0)			# Set The Color To Yellow
	# glVertex3f(vertices['e'][0],vertices['e'][1],vertices['e'][2])
	# glVertex3f(vertices['f'][0],vertices['f'][1],vertices['f'][2])
	# glVertex3f(vertices['h'][0],vertices['h'][1],vertices['h'][2])
	# glVertex3f(vertices['g'][0],vertices['g'][1],vertices['g'][2])

	# # LEFT face
	# glColor3f(0.0,0.0,1.0)			# Set The Color To Blue
	# glVertex3f(vertices['a'][0],vertices['a'][1],vertices['a'][2])
	# glVertex3f(vertices['e'][0],vertices['e'][1],vertices['e'][2])
	# glVertex3f(vertices['g'][0],vertices['g'][1],vertices['g'][2])
	# glVertex3f(vertices['c'][0],vertices['c'][1],vertices['c'][2])

	# RIGHT face
	glColor3f(1.0,0.0,1.0)			# Set The Color To Violet
	glVertex3f(vertices['b'][0],vertices['b'][1],vertices['b'][2])
	glVertex3f(vertices['f'][0],vertices['f'][1],vertices['f'][2])
	glVertex3f(vertices['h'][0],vertices['h'][1],vertices['h'][2])
	glVertex3f(vertices['d'][0],vertices['d'][1],vertices['d'][2])

	glEnd()				# Done Drawing The Quad

	# What values to use?  Well, if you have a FAST machine and a FAST 3D Card, then
	# large values make an unpleasant display with flickering and tearing.  I found that
	# smaller values work better, but this was based on my experience.
	# rtri  = rtri + 0.2                  # Increase The Rotation Variable For The Triangle
	# rquad = rquad - 0.15                 # Decrease The Rotation Variable For The Quad


	#  since this is double buffered, swap the buffers to display what just got drawn. 
	glutSwapBuffers()

# The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)  
def keyPressed(*args):
	global vertices, vNames, currentV, rquadSum
	# If escape is pressed, kill everything.
	if args[0] == ESCAPE:
		glutDestroyWindow(window)
		sys.exit()

	# X axis
	elif args[0] == 'a':
		vertices[vNames[currentV]][0]-=0.1
	elif args[0] == 'd':
		vertices[vNames[currentV]][0]+=0.1
		
	# Y axis
	elif args[0] == 's':
		vertices[vNames[currentV]][1]-=0.1
	elif args[0] == 'w':
		vertices[vNames[currentV]][1]+=0.1

	# Z axis
	elif args[0] == 'e':
		vertices[vNames[currentV]][2]-=0.1
	elif args[0] == 'q':
		vertices[vNames[currentV]][2]+=0.1

	# change vertix
	elif args[0] == 'p':
		currentV = (currentV+1)%8

	# rotate
	elif args[0] == 'o':
		rquadSum = (rquadSum + 0.5)%1

		
def main():
	global window

	glutInit(sys.argv)

	# Select type of Display mode:   
	#  Double buffer 
	#  RGBA color
	# Alpha components supported 
	# Depth buffer
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
	
	# get a 640 x 480 window 
	glutInitWindowSize(640, 480)
	
	# the window starts at the upper left corner of the screen 
	glutInitWindowPosition(0, 0)
	
	# Okay, like the C version we retain the window id to use when closing, but for those of you new
	# to Python (like myself), remember this assignment would make the variable local and not global
	# if it weren't for the global declaration at the start of main.
	window = glutCreateWindow("Jeff Molofee's GL Code Tutorial ... NeHe '99")

		# Register the drawing function with glut, BUT in Python land, at least using PyOpenGL, we need to
	# set the function pointer and invoke a function to actually register the callback, otherwise it
	# would be very much like the C version of the code.	
	glutDisplayFunc(DrawGLScene)
	#glutDisplayFunc()
	
	# Uncomment this line to get full screen.
	# glutFullScreen()

	# When we are doing nothing, redraw the scene.
	glutIdleFunc(DrawGLScene)
		
	# Register the function called when our window is resized.
	glutReshapeFunc(ReSizeGLScene)
	
	
	# Register the function called when the keyboard is pressed.  
	glutKeyboardFunc(keyPressed)
	
	# Initialize our window. 
	InitGL(640, 480)

	
# Print message to console, and kick off the main to get it rolling.
print "Hit ESC key to quit."

if __name__ == '__main__':
	try:
		GLU_VERSION_1_2
	except:
		print "Need GLU 1.2 to run this demo"
		sys.exit(1)
	main()
	glutMainLoop()
			
