import wx
import os
import copy
import pygame
from pygame.locals import Color
from collections import OrderedDict
from pygamepanel import PygamePanel
import  wx.lib.newevent, wx.stc as stc
from statusctrl import StatusCtrl
from objctrl import objCtrl
from listener import Key_listener

from OpenGL.GL import *
from OpenGL.GLU import *

#to be updated later when I begin adding 3D effects to my animations
#most important will be to allow for draw order to be handled by opengl itself while still allowing transparency
#and no, I'm not tracing the outline of my characters every time I want to make one
#I mean FFS this is suppose to be faster, why would I give up that just so I could have clipping
#I'm sure there's a simple solution, or at least a practical one

class OBJ3D:
	def __init__(self):
		self.cubeVertices = ((1,1,1),(1,1,-1),(1,-1,-1),(1,-1,1),(-1,1,1),(-1,-1,-1),(-1,-1,1),(-1, 1,-1))
		self.cubeEdges = ((0,1),(0,3),(0,4),(1,2),(1,7),(2,5),(2,3),(3,6),(4,6),(4,7),(5,6),(5,7))
		self.cubeQuads = ((0,3,6,4),(2,5,6,3),(1,2,5,7),(1,0,4,7),(7,4,6,5),(2,3,0,1))
		self.data = {}
		self.data["angle"] = 0
		self.data["pos"] = [0,0,0]

	def update(self):
		pass

	def draw_entity(self):
		pass

	def draw_wire(self):
		self.data["angle"] += 10
		glPushMatrix()
		glRotatef(self.data["angle"],1,1,1)

		glBegin(GL_LINES)
		for cubeEdge in self.cubeEdges:
			for cubeVertex in cubeEdge:
				glVertex3fv(self.cubeVertices[cubeVertex])
		glEnd()
		glPopMatrix()
