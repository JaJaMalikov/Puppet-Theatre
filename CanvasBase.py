import wx
import os
import copy

from wx import glcanvas

from OpenGL.GL import *
from OpenGL.GLU import *

import OpenGL.GL.shaders
from pyrr import Matrix44

from datetime import datetime

import json

import numpy

from consts import *
import time



class CanvasBase(glcanvas.GLCanvas):
	def __init__(self, parent, ViewPortSize, data):
		glcanvas.GLCanvas.__init__(self, parent, -1, size=(ViewPortSize))
		self.init = False
		self.context = glcanvas.GLContext(self)
		self.data = data
		self.resized = True
		self.ViewPortSize = ViewPortSize
		self.SetCurrent(self.context)

		glClearColor(*self.data["Background Color"])

		self.Bind(wx.EVT_SIZE, self.OnResize)

	def is_resized(self):
		resized = self.resized
		self.resized = False
		return resized

	def set_data(self, data):
		self.data = data

	def Purge(self):
		glLoadIdentity()
		gluPerspective(45, (self.ViewPortSize[0]/ self.ViewPortSize[1]), 0.1, 50.0 )
		glTranslatef(0.0,0.0,-10)

	def clear(self):
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

	def OnResize(self, event):
		size = self.GetClientSize()
		self.ViewPortSize = size
		glViewport(0, 0, size.width, size.height)
		self.Purge()
		self.resized = True

	def set_bg(self, color):
		glClearColor(*color)

	def Update(self):
		self.Purge()

	def Draw(self):
		self.SwapBuffers()
