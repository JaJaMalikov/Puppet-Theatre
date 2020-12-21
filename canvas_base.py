#Graphical Libraries
import wx
from wx import glcanvas
from OpenGL.GL import *
from OpenGL.GLU import *


#other built-in libraries

#designated constants for program-wide use
from consts import *

loc = 74

class CanvasBase(glcanvas.GLCanvas):
	"""
	basis for the canvas object in the render control panel
	currently uses the fixe function pipeline, will be updated to modern opengl
	3.3+ in Beta 2
	"""
	def __init__(self, parent, ViewPortSize, data):
		glcanvas.GLCanvas.__init__(self, parent, -1, size=(ViewPortSize))
		self.init = False
		self.context = glcanvas.GLContext(self)
		self.data = data
		self.resized = True
		self.ViewPortSize = ViewPortSize
		self.SetCurrent(self.context)

		#self.data["Background Color"] is a 4 float list of RGBA values
		#using the * before unpacks it because clear color takes 4 inputs
		glClearColor(*self.data["Background Color"])
		glEnable(GL_DEPTH_TEST)
		glDepthFunc(GL_LEQUAL)
		self.Bind(wx.EVT_SIZE, self.OnResize)


	def is_resized(self):
		resized = self.resized
		self.resized = False
		return resized

	def set_data(self, data):
		#loads the current project data in order to get the background color
		self.data = data

	def Purge(self):
		#resets the convas identity, perspective, and position
		glLoadIdentity()
		gluPerspective(45, (self.ViewPortSize[0]/ self.ViewPortSize[1]), 0.1, 50.0 )
		glTranslatef(0.0,0.0,-10)

	def clear(self):
		#clears the canvas with the color set in self.data["Background Color"]
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

	def OnResize(self, event):
		#sets the viewportsize and readjusts the glViewport to match
		#purges the canvas to match
		size = self.GetClientSize()
		self.ViewPortSize = size
		glViewport(0, 0, size.width, size.height)
		self.Purge()
		self.resized = True

	def set_bg(self, color):
		#self.data["Background Color"] = color
		
		glClearColor(*color)

	def Update(self):


		#only purges at the moment but future proofing in case updates should do more later
		self.Purge()

	def Draw(self):
		self.SwapBuffers()
