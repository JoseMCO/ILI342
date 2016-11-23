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
from PIL import Image
import zmq
import time
import sys

# Some api in the chain is translating the keystrokes to this octal string
# so instead of saying: ESCAPE = 27, we use the following.
ESCAPE 	= '\033'
LEFT	= '\037'
UP 		= '\038'
RIGHT 	= '\039'
DOWN 	= '\040'

# Number of the glut window.
window = 0

#    e-------f
#   /|      /|
#  / |     / |
# a-------b  |
# |  |    |  |
# |  g----|--h
# | /     | /
# c-------d

vertices = {}
vertices['a'] = [100.0, 101.0,  0.0]
vertices['b'] = [101.0, 101.0,  0.0]
vertices['c'] = [100.0, 100.0,  0.0]
vertices['d'] = [101.0, 100.0,  0.0]
vertices['e'] = [100.5, 101.5,  0.0]
vertices['f'] = [101.5, 101.5,  0.0]
vertices['g'] = [100.5, 100.5,  0.0]
vertices['h'] = [101.5, 100.5,  0.0]
# vNames = ['a','b','c','d','e','f','g','h']
vNames = ['a','b','c','d','e','f','h']
pickV = 0.1
currentV = 0
currentO = 0
sleepTime = 1.0
currentTime = time.time()
counter = 0
timeLeft = 10
textures = []
buffers = []
gameState = -1
ready = False

port = 0
if len(sys.argv) > 1:
	server = sys.argv[1]
	port = int(server.split(':')[1])
	# ZeroMQ Context
	context = zmq.Context()
	# Define the socket using the "Context"
	sock = context.socket(zmq.REQ)
	sock.connect("tcp://%s" % server)


def MidPoints(p, q, z=0.01):
	xdif = (q[0]-p[0])/3.0
	ydif = (q[1]-p[1])/3.0
	if xdif > 0:
		x1 = p[0]+xdif
		x2 = p[0]+(xdif*2)
	else:
		x2 = q[0]+(xdif*-1)
		x1 = q[0]+(xdif*-2)
	if ydif > 0:
		y1 = p[1]+ydif
		y2 = p[1]+(ydif*2)
	else:
		y2 = q[1]+(ydif*-1)
		y1 = q[1]+(ydif*-2)

	return [x1,y1,z],[x2,y2,z]

def LoadTextures(images):
	glTextures = glGenTextures(len(images))
	for path in images:
		print 'binding texture %s as %s' % (path, glTextures[len(textures)])
		image = Image.open(path)
		ix = image.size[0]
		iy = image.size[1]
		image = image.tostring("raw", "RGBX", 0, -1)
		glBindTexture(GL_TEXTURE_2D, glTextures[len(textures)])
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
		textures.append(glTextures[len(textures)])
		glBindTexture(GL_TEXTURE_2D, 0)


# A general OpenGL initialization function.  Sets all of the initial parameters.
def InitGL(Width, Height):				# We call this right after our OpenGL window is created.
	glClearColor(0.0, 0.0, 0.0, 0.0)	# This Will Clear The Background Color To Black
	glClearDepth(1.0)					# Enables Clearing Of The Depth Buffer
	glDepthFunc(GL_LESS)				# The Type Of Depth Test To Do
	glEnable(GL_DEPTH_TEST)				# Enables Depth Testing
	glShadeModel(GL_SMOOTH)				# Enables Smooth Color Shading

	images = [
				"numbers/number_0.bmp",
				"numbers/number_1.bmp",
	   			"numbers/number_2.bmp",
				"numbers/number_3.bmp",
				"numbers/number_4.bmp",
				"numbers/number_5.bmp",
				"numbers/number_6.bmp",
				"numbers/number_7.bmp",
				"numbers/number_8.bmp",
				"numbers/number_9.bmp",
				"numbers/number_10.bmp",
				"energies/energy-fire.bmp",
				"energies/energy-grass.bmp",
				"energies/energy-light.bmp",
				"energies/energy-fight.bmp",
				"energies/energy-water.bmp",
				"energies/energy.bmp",
				"battle/vs.bmp",
				"battle/tie.bmp",
				"battle/winner.bmp",
				"battle/loser.bmp",
			]
	LoadTextures(images)

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

def DrawColorQuad(a,b,c,d,color):
	glBegin(GL_QUADS)				# Start Drawing The Quad
	glColor3f(color[0],color[1],color[2])			# Set The Color
	glVertex3f( a[0], a[1], a[2] )
	glVertex3f( b[0], b[1], b[2] )
	glVertex3f( c[0], c[1], c[2] )
	glVertex3f( d[0], d[1], d[2] )
	glEnd()							# Done Drawing The Quad
	glColor3f(1.0, 1.0, 1.0)

def DrawColorSquare(a,b,c,d,color, z=0.0001):
	glLineWidth(2.0)
	glBegin(GL_LINES)
	glColor3f(color[0],color[1],color[2])
	glVertex3f( a[0], a[1], a[2]+z )
	glVertex3f( b[0], b[1], b[2]+z )
	glVertex3f( b[0], b[1], b[2]+z )
	glVertex3f( c[0], c[1], c[2]+z )
	glVertex3f( c[0], c[1], c[2]+z )
	glVertex3f( d[0], d[1], d[2]+z )
	glVertex3f( d[0], d[1], d[2]+z )
	glVertex3f( a[0], a[1], a[2]+z )
	glEnd()						# Done Drawing The Quad
	glColor3f(1.0, 1.0, 1.0)

def DrawTextureQuad(a,b,c,d,t):
	# print 'Using buffer %s with texture %s' % (buffers[t], textures[t])
	# glBindFramebuffer(GL_FRAMEBUFFER, buffers[t])
	glActiveTexture(GL_TEXTURE0+(t%8))
	glEnable(GL_TEXTURE_2D)
	glBindTexture(GL_TEXTURE_2D, textures[t])
	glBegin(GL_QUADS)				# Start Drawing The Quad
	glMultiTexCoord2f(GL_TEXTURE0+t, 0.0, 1.0); glVertex3f( a[0], a[1], a[2] )
	glMultiTexCoord2f(GL_TEXTURE0+t, 1.0, 1.0); glVertex3f( b[0], b[1], b[2] )
	glMultiTexCoord2f(GL_TEXTURE0+t, 1.0, 0.0); glVertex3f( c[0], c[1], c[2] )
	glMultiTexCoord2f(GL_TEXTURE0+t, 0.0, 0.0); glVertex3f( d[0], d[1], d[2] )
	glEnd()				# Done Drawing The Quad
	glBindFramebuffer(GL_FRAMEBUFFER, 0)
	glBindTexture(GL_TEXTURE_2D, 0)

# The main drawing function.
def DrawGLScene():
	global vertices, vNames, currentV, currentTime, textures, currentTime, counter, timeLeft, gameState

	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)	# Clear The Screen And The Depth Buffer
	glLoadIdentity()								# Reset The View
	gluLookAt(100.5, 100.5, 5, 100.5, 100.5, 0, 0, 1, 0)

	if port > 0 and ready:
		if timeLeft < 1 and gameState == -1:
			print "waiting for the veredict..."
			sock.send("option:%s" % currentO)
			veredict = sock.recv()
			if veredict == "win":
				gameState = 2
			elif veredict == "loss":
				gameState = 1
			else:
				gameState = 0
		else:
			gameState = -1
			print "sending tick"
			sock.send("Tick!")
			timeLeft = int(sock.recv())
			print "Time left: %ss" % timeLeft
	else:
		elapsed = time.time() - currentTime
		if elapsed > sleepTime:
			# time.sleep((sleepTime-elapsed))
			if (timeLeft > 0):
				timeLeft = timeLeft-1
			elif gameState:
				timeLeft = 10
			currentTime = time.time()


	#    e-------f
	#   /|      /|
	#  / |     / |
	# a-------b  |
	# |  |    |  |
	# |  g----|--h
	# | /     | /
	# c-------d

	# a----l01---l02----b
	# |  1  |  2  |  3  |
	# l03--l04---l05--l06
	# |  4  |  5  |  6  |
	# l07--l08---l09--l10
	# |  7  |  8  |  9  |
	# c----l11---l12----d

	# e----t01---t02----f
	# |  1  |  2  |  3  |
	# t03--t04---t05--t06
	# |  4  |  5  |  6  |
	# t07--t08---t09--t10
	# |  7  |  8  |  9  |
	# a----t11---t12----b

	a = vertices['a'];b = vertices['b'];c = vertices['c'];d = vertices['d']
	e = vertices['e'];f = vertices['f'];g = vertices['g'];h = vertices['h']
	l01,l02 = MidPoints(a,b,0);l07,l03 = MidPoints(c,a,0);l10,l06 = MidPoints(d,b,0);l11,l12 = MidPoints(c,d,0)
	l04,l05 = MidPoints(l03,l06,0);l08,l09 = MidPoints(l07,l10,0)

	t01,t02 = MidPoints(e,f,0);t07,t03 = MidPoints(a,e,0);t10,t06 = MidPoints(b,f,0);t11,t12 = MidPoints(a,b,0)
	t04,t05 = MidPoints(t03,t06,0);t08,t09 = MidPoints(t07,t10,0)

	lp = [a,l01,l02,b,l03,l04,l05,l06,l07,l08,l09,l10,c,l11,l12,d]
	tp = [e,t01,t02,f,t03,t04,t05,t06,t07,t08,t09,t10,a,t11,t12,b]
	options = [
		[  a,l01,l04,l03],
		# [l01,l02,l05,l04],
		[l02,  b,l06,l05],
		# [l03,l04,l08,l07],
		[l04,l05,l09,l08],
		# [l05,l06,l10,l09],
		[l07,l08,l11,  c],
		# [l08,l09,l12,l11],
		[l09,l10,  d,l12],
	]
	tOptions = [
		[  e,t01,t04,t03],
		# [t01,t02,t05,t04],
		[t02,  f,t06,t05],
		# [t03,t04,t08,t07],
		[t04,t05,t09,t08],
		# [t05,t06,t10,t09],
		[t07,t08,t11,  a],
		# [t08,t09,t12,t11],
		[t09,t10,  b,t12],
	]

	if not ready:
		DrawColorQuad(a,b,d,c,(1.0,0.0,0.0))
		DrawColorQuad(a,b,f,e,(0.0,1.0,0.0))
		DrawColorQuad(b,f,h,d,(0.0,0.0,1.0))
		if int(currentTime)%2:
			glBegin(GL_TRIANGLES)       # Drawing Using Triangles
			glColor3f(0.0,1.0,1.0)		# Set The Color To Blue
			glVertex3f( vertices[vNames[currentV]][0]     , vertices[vNames[currentV]][1]+0.05,0.01)
			glVertex3f( vertices[vNames[currentV]][0]-0.05, vertices[vNames[currentV]][1]-0.05,0.01)
			glVertex3f( vertices[vNames[currentV]][0]+0.05, vertices[vNames[currentV]][1]-0.05,0.01)
			glEnd()                     # Finished Drawing The Triangle

		if port == 0:
			num = int(currentTime)%len(tp)
			glBegin(GL_TRIANGLES)       # Drawing Using Triangles
			glColor3f(1.0,1.0,1.0)		# Set The Color To Blue
			glVertex3f( tp[num][0]     , tp[num][1]+0.03,0.01)
			glVertex3f( tp[num][0]-0.03, tp[num][1]-0.03,0.01)
			glVertex3f( tp[num][0]+0.03, tp[num][1]-0.03,0.01)

			glVertex3f( lp[num][0]     , lp[num][1]+0.03,0.01)
			glVertex3f( lp[num][0]-0.03, lp[num][1]-0.03,0.01)
			glVertex3f( lp[num][0]+0.03, lp[num][1]-0.03,0.01)
			glEnd()                     # Finished Drawing The Triangle
			currentTime+=0.05

	elif timeLeft==0 and gameState == 1:
		# DrawColorQuad(b,f,h,d,(0.0,1.0,0.0))
		DrawTextureQuad(t05,t06,t10,t09,currentO+11)

		# DrawColorQuad(a,b,d,c,(1.0,0.0,0.0))
		DrawTextureQuad(t07,t10,b,a,len(textures)-1)

		DrawColorQuad(t07,t10,b,a,(1.0,0.0,0.0))
		# DrawTextureQuad(e,f,b,a,timeLeft)

	elif timeLeft==0 and gameState == 2:
		# DrawColorQuad(b,f,h,d,(0.0,1.0,0.0))
		DrawTextureQuad(t05,t06,t10,t09,currentO+11)

		# DrawColorQuad(a,b,d,c,(0.0,1.0,0.0))
		DrawTextureQuad(t07,t10,b,a,len(textures)-2)

		DrawColorQuad(t07,t10,b,a,(0.0,1.0,0.0))
		# DrawTextureQuad(e,f,b,a,timeLeft)

	elif timeLeft==0 and gameState == 0:
		# DrawColorQuad(b,f,h,d,(0.0,1.0,0.0))
		DrawTextureQuad(t05,t06,t10,t09,currentO+11)

		DrawColorQuad(a,b,d,c,(0.5,0.5,0.5))
		DrawTextureQuad(t07,t10,b,a,len(textures)-3)

		DrawColorQuad(t07,t10,b,a,(0.5,0.5,0.5))
		# DrawTextureQuad(e,f,b,a,timeLeft)

	else:
		DrawColorSquare(options[currentO][0],options[currentO][1],options[currentO][2],options[currentO][3],(0.0,1.0,0.0))
		DrawColorQuad(e,f,b,a,(0.0,0.0,0.0))
		# DrawTextureQuad(b,f,h,d,currentO+11)

		# DrawColorQuad(a,b,d,c,(0.0,0.0,1.0))
		DrawTextureQuad(a,b,d,c,len(textures)-5)

		# DrawColorQuad(a,b,f,e,(1.0,0.0,0.0))
		DrawTextureQuad(b,f,h,d,timeLeft)

	#  since this is double buffered, swap the buffers to display what just got drawn.
	glutSwapBuffers()

# The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)
def keyPressed(*args):
	global vertices, vNames, currentV, ready, pickV, gameState, currentO
	# If escape is pressed, kill everything.
	if args[0] == ESCAPE:
		glutDestroyWindow(window)
		sys.exit()

	# X axis
	elif args[0] == 'a':
		vertices[vNames[currentV]][0]-=pickV
	elif args[0] == 'd':
		vertices[vNames[currentV]][0]+=pickV

	# Y axis
	elif args[0] == 's':
		vertices[vNames[currentV]][1]-=pickV
	elif args[0] == 'w':
		vertices[vNames[currentV]][1]+=pickV

	# change vertix
	elif args[0] == 'p':
		currentV = (currentV+1)%len(vNames)

	# change pickV
	elif args[0] == 'v':
		if pickV == 0.1 :
			pickV = 0.01
		else :
			pickV = 0.1

	# change option
	elif args[0] == ' ':
		if not ready:
			ready = True
		elif gameState == -1:
			currentO = (currentO+1)%5

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
	window = glutCreateWindow("P")

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
