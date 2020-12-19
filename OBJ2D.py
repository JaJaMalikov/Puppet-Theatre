#Graphical Libraries
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

#other built-in libraries
import copy

#the default vertecies, coords, and edges
#produced by vert_gen using a series of for-loops
import verts

loc = 127

class OBJ2D:
	def __init__(self, pathname):
		#sets the default state, copying the verts, coords, and edges from verts
		#loads the texture from pathname
		self.pathname = pathname
		self.loaded = False
		self.verts = copy.deepcopy(verts.verts)
		self.coords = copy.deepcopy(verts.coords)
		self.edges = copy.deepcopy(verts.edges)

		self.texture = self.load_texture()

	def load_texture(self):
		"""
		the texture surface is loaded from pathname via pygame
		pygame loads it as an image and built-in functions give the size data and the texture data
		once loaded it checks the aspect ratio and multiplies the verts accordingly
		this allows the image to be scaled more easily without warping
		"""
		textureSurface = pygame.image.load(self.pathname)
		textureData = pygame.image.tostring(textureSurface, "RGBA", 1)

		#load check probably not needed
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

		"""
		texture is bound to an ID which is saved as self.texture
		this uses the old opengl fixed function pipeline and will be replaced with Beta 2
		"""
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
		"""
		using the fixed function pipeline the current texture is bound and drawn
		the object data is used for translation, rotation, and scale
		future plans include an additional transformation step for the parent 
		before the transformation step for the child
		"""
		glBindTexture(GL_TEXTURE_2D, self.texture)

		glPushMatrix()
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		glEnable(GL_BLEND)

		#future parent transformation step goes here
		#if parent != None:
		#	self.transform(parent)
		#self.transform(indata)

		#transformation step
		glTranslatef(inData["Pos"][0], inData["Pos"][1], inData["Pos"][2] )
		glRotatef(inData["Angle"], 0, 0, 1)
		glScalef(inData["FlipX"] * inData["ScaleX"] * scale_mod, inData["FlipY"] * inData["ScaleY"] * scale_mod, 1.0)

		glBegin(GL_POLYGON)

		for x in range(len(self.verts)):
			glTexCoord2f(*self.coords[x])
			glVertex3f(*self.verts[x])

		glEnd()

		glDisable(GL_BLEND)
		glPopMatrix()

	def draw_wire(self, inData, scale_mod = 1.0):
		"""
		wire drawing for possible debug mode
		"""
		glBindTexture(GL_TEXTURE_2D, self.texture)

		glPushMatrix()

		glTranslatef(inData["Pos"][0], inData["Pos"][1], inData["Pos"][2] )
		glRotatef(inData["Angle"], 0, 0, 1)
		glScalef(inData["FlipX"] * inData["ScaleX"] * scale_mod, inData["FlipY"] * inData["ScaleY"] * scale_mod, 1.0)

		glBegin(GL_LINES)

		for Edge in self.edges:
			for Vertex in Edge:
				glVertex3fv(self.verts[Vertex])

		glEnd()
		glPopMatrix()
