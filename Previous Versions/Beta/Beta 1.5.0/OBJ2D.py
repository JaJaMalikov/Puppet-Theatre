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
	def __init__(self, pathname, window):
		#sets the default state, copying the verts, coords, and edges from verts
		#loads the texture from pathname
		self.pathname = pathname
		self.loaded = False
		self.verts = copy.deepcopy(verts.verts)
		self.coords = copy.deepcopy(verts.coords)
		self.edges = copy.deepcopy(verts.edges)
		self.canvas = window.renderCtrl.canvas

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
		return self.canvas.loadTexture(textureData, self.width, self.height)


	def draw(self, inData, scale_mod = 1.0, parent = None):
		"""
		using the fixed function pipeline the current texture is bound and drawn
		the object data is used for translation, rotation, and scale
		future plans include an additional transformation step for the parent 
		before the transformation step for the child
		"""
		self.canvas.prepTexture(self.texture)

		if parent != None:
			self.canvas.transform(parent, False)
			self.canvas.transform(inData, True)
		else:
			self.canvas.transform(inData, False)
		#transformation step

		self.canvas.drawTexture(self.verts, self.coords)

	def draw_wire(self, inData):
		self.canvas.draw_wire(inData, self.texture, self.verts, self.edges)