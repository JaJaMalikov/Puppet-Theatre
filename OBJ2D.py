#Graphical Libraries
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

#other built-in libraries
import copy

#the default vertecies, coords, and edges
#produced by vert_gen using a series of for-loops
import verts

class OBJ2D:
	def __init__(self, pathname, window):
		#sets the default state, copying the verts, coords, and edges from verts
		#loads the texture from pathname
		self.window = window
		self.pathname = pathname
		self.Image_list = self.window.Image_list
		self.loaded = False
		self.verts = copy.deepcopy(verts.verts)
		self.coords = copy.deepcopy(verts.coords)
		self.edges = copy.deepcopy(verts.edges)
		self.canvas = window.renderCtrl.canvas

		self.texture = self.load_texture()

		img_num = pathname.count("\\")
		self.img_tag = pathname.split("\\", img_num-1)[-1]

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

	def transform(self, parents, inData):
		if parents != []:
			for parent in range(len(parents)):
				if parent == 0:
					self.canvas.transform(self.window.data["Frames"][self.window.data["Current Frame"]][parents[parent]], False)
				else:
					self.canvas.transform(self.window.data["Frames"][self.window.data["Current Frame"]][parents[parent]], True)
			self.canvas.transform(inData, True)
		else:
			self.canvas.transform(inData, False)

	def draw(self, inData, scale_mod = 1.0, parent=None, draw_origin=False, parents = []):
		"""
		using the fixed function pipeline the current texture is bound and drawn
		the object data is used for translation, rotation, and scale
		future plans include an additional transformation step for the parent 
		before the transformation step for the child
		"""

		if parent == "Camera":
			self.canvas.draw_cam(self.texture, self.verts, self.coords)

		else:
			drawn = False
			self.canvas.begin()

			self.transform(parents, inData)


			self.canvas.prepTexture(self.texture)
			self.canvas.drawTexture(self.verts, self.coords)				

			self.canvas.end()

	def draw_wire(self, inData, parent=None):
		self.canvas.draw_wire(inData, self.texture, self.verts, self.edges, self.coords)

	def draw_origin(self, inData, parents=None):
		if parents != []:
			for parent in range(len(parents)):
				if parent == 0:
					self.canvas.transform(self.window.data["Frames"][self.window.data["Current Frame"]][parents[parent]], False)
				else:
					self.canvas.transform(self.window.data["Frames"][self.window.data["Current Frame"]][parents[parent]], True)

		self.canvas.draw_origin(inData, self.texture, self.verts, self.edges)
