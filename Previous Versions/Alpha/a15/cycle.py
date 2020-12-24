import wx
import os
import copy
import pygame
from pygame.locals import Color
from collections import OrderedDict
import  wx.lib.newevent, wx.stc as stc
from record import Record

from OpenGL.GL import *
from OpenGL.GLU import *

class cycle:
	def __init__(self, directory):
		self.set = OrderedDict()
		self.directory = directory
		self.texture_list = []
		self.verts = [ 
				[-1.0,1.0,0.0], 
				[0.0, 1.0, 0.0], 
				[1.0,1.0,0.0], 
				[1.0,0.0,0.0], 
				[1.0,-1.0,0.0],  
				[0.0,-1.0,0.0],
				[-1.0,-1.0,0.0],
				[-1.0,0.0,0.0] ]

		self.frame = 0
		self.coords = ((0.0,1.0),
						(0.5,1.0),
						(1.0,1.0),
						(1.0,0.5),
						(1.0,0.0),
						(0.5,0.0),
						(0.0,0.0),
						(0.0,0.5))

		self.edges = [
		[0,1],
		[1,2],
		[2,3],
		[3,4],
		[4,5],
		[5,6],
		[6,7],
		[7,0]
		]
		self.load_textures()

	def get_loaded(self):
		return (len(self.set) > 0)

	def change_set(self, directory):
		self.set = OrderedDict()
		self.directory = directory
		self.load_textures()

	def load_textures(self):
		names = os.listdir(self.directory)
		for name in names:
			self.texture_list.append(self.load_texture(os.path.join(self.directory, name)))

	def load_texture(self, name):
		textureSurface = pygame.image.load(name).convert_alpha()
		textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
		self.width = textureSurface.get_width()
		self.height = textureSurface.get_height()

		if self.width > self.height:
			ratio = self.height/self.width
			for x in range(len(self.verts)):
				self.verts[x][1] *= ratio

		else:
			ratio = self.width/self.height
			for x in range(len(self.verts)):
				self.verts[x][0] *= ratio

		glEnable(GL_TEXTURE_2D)

		texid = glGenTextures(1)

		glBindTexture(GL_TEXTURE_2D, texid)
		
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height,
					 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
		
		glGenerateMipmap(GL_TEXTURE_2D)
		
		return texid

	def draw_surf(self, data):
		glPushMatrix()
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		glEnable(GL_BLEND)

		glTranslatef(data["pos"][0], data["pos"][1] , data["pos"][2])
		glRotatef(data["angle"], 0, 0, 1)
		glScalef(data["flipX"] * data["scale"],data["flipY"] * data["scale"],1.0)
		#data["angle"] = 0
		glBegin(GL_POLYGON)
		for x in range(len(self.verts)):
			glTexCoord2f(*self.coords[x])
			glVertex3f(*self.verts[x])

		glEnd()

		glDisable(GL_BLEND)
		glPopMatrix()

	def draw_entity(self, data):
		if self.dirname != None and data["visible"]:
			glBindTexture(GL_TEXTURE_2D, self.texture_list[self.frame] )
			self.draw_surf()
			self.frame = (self.frame + 1) % len(self.texture_list)

	def draw_wire(self, data):
		glPushMatrix()
		glTranslatef(data["pos"][0], data["pos"][1] , data["pos"][2])
		glRotatef(data["angle"], 0, 0, 1)

		glBegin(GL_LINES)
		for Edge in self.edges:
			for Vertex in Edge:
				glVertex3fv(self.verts[Vertex])
		glEnd()
		glPopMatrix()	