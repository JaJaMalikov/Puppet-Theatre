import wx
import os
import copy

from wx import glcanvas

from collections import OrderedDict

import pygame
from pygame.locals import *


import  wx.lib.newevent, wx.stc as stc
import numpy as np

from OpenGL.GL import *
from OpenGL.GLU import *

import json

import random
import string

import datetime
from datetime import datetime

import verts

import random


class OBJ2D:
	def __init__(self, pathname):
		self.pathname = pathname
		self.loaded = False
		self.verts = copy.deepcopy(verts.verts)
		self.coords = copy.deepcopy(verts.coords)
		self.edges = copy.deepcopy(verts.edges)
		self.cur_verts = copy.deepcopy(verts.verts)

		self.texture = self.load_texture()

	def load_texture(self):
		textureSurface = pygame.image.load(self.pathname)
		textureData = pygame.image.tostring(textureSurface, "RGBA", 1)

		if not self.loaded:
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

			self.loaded = True

		glEnable(GL_TEXTURE_2D)
		texture = glGenTextures(1)
		glBindTexture(GL_TEXTURE_2D, texture)
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height,
					0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

		glGenerateMipmap(GL_TEXTURE_2D)
		return texture

	def draw(self, inData, scale_mod = 1.0):
		glBindTexture(GL_TEXTURE_2D, self.texture)

		glPushMatrix()
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		glEnable(GL_BLEND)

		glTranslatef(inData["pos"][0], inData["pos"][1], inData["pos"][2] )
		glRotatef(inData["angle"], 0, 0, 1)
		glScalef(inData["flipX"] * inData["scaleX"] * scale_mod, inData["flipY"] * inData["scaleY"] * scale_mod, 1.0)
		glBegin(GL_POLYGON)

		self.cur_verts = self.verts

		for x in range(len(self.verts)):
			glTexCoord2f(*self.coords[x])
			glVertex3f(*self.cur_verts[x])

		glEnd()

		glDisable(GL_BLEND)
		glPopMatrix()

	def draw_wire(self, inData, scale_mod = 1.0):
		glBindTexture(GL_TEXTURE_2D, self.texture)

		glPushMatrix()

		glTranslatef(inData["pos"][0], inData["pos"][1], inData["pos"][2] )
		glRotatef(inData["angle"], 0, 0, 1)
		glScalef(inData["flipX"] * inData["scaleX"] * scale_mod, inData["flipY"] * inData["scaleY"] * scale_mod, 1.0)
		self.cur_verts = self.verts

		glBegin(GL_LINES)

		for Edge in self.edges:
			for Vertex in Edge:
				glVertex3fv(self.verts[Vertex])

		glEnd()
		glPopMatrix()
