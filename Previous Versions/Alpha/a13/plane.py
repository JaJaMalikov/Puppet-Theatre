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
from record import Record

from OpenGL.GL import *
from OpenGL.GLU import *

class OBJ2D:
	def __init__(self, dirname, HUD):
		self.HUD = HUD
		self.record = Record()
		self.data = {}
		self.data["speed"] = .05
		self.dirname = dirname
		self.texture_list = []
		self.width = 0
		self.height = 0
		self.data["scale"] = 1
		self.data["angle"] = 0
		self.data["pos"] = [0,0,0]
		self.data["flipX"] = 1.0
		self.data["flipY"] = 1.0
		self.data["mouth"] = "open"
		self.data["substate"] = 0
		self.data["state"] = 0
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

	def set_data(self):
		self.HUD.set_Animating(True)
		self.HUD.set_yoffset(0)
		self.HUD.set_xoffset(0)
		self.HUD.set_playback(self.record.is_playing())
		self.HUD.set_recording(self.record.is_playing())
		self.HUD.set_mouth(self.data["mouth"])
		self.HUD.set_substate(self.data["substate"])
		self.HUD.set_state(self.data["state"])
		self.HUD.set_angle(self.data["angle"])
		self.HUD.set_pos(self.data["pos"])
		self.HUD.set_FLIP_H(self.data["flipX"])
		self.HUD.set_FLIP_V(self.data["flipY"])
		self.HUD.set_Speed(self.data["speed"])


	def update(self):
		if self.record.is_recording():
			self.record.append(self.data)
		elif self.record.is_playing():
			self.data = self.record.get()
			self.record.next()

	def zoom(self, factor):
		self.data["scale"] += self.data["speed"] * factor

	def flipX(self):
		self.data["flipX"] *= -1.0

	def flipY(self):
		self.data["flipY"] *= -1.0

	def start_recording(self):
		self.record.start()

	def stop_recording(self):
		self.record.pause()

	def start_playing(self):
		self.record.playback()

	def stop_playing(self):
		self.record.stop()

	def places(self):
		self.record.reset()

	def m_rot(self, m_rel):
		self.data["angle"] -= m_rel[0] * .5

	def rotp(self):
		self.data["angle"] += self.data["speed"] * 100

	def rotn(self):
		self.data["angle"] += self.data["speed"] * -100

	def set_pos(self, pos):
		self.data["pos"] = [pos[0], pos[1], self.data["pos"][2]]

	def move_H(self, delta):
		self.data["pos"][0] += delta * self.data["speed"]

	def move_V(self, delta):
		self.data["pos"][1] += delta * self.data["speed"]

	def move_D(self, delta):
		self.data["pos"][2] += delta * self.data["speed"]

	def set_name(self, name):
		self.dirname = name

	def load_textures(self):
		names = os.listdir(self.dirname)
		for name in names:
			self.texture_list.append(self.load_texture(os.path.join(self.dirname, name)))

	def load_texture(self, name):
		textureSurface = pygame.image.load(name).convert_alpha()
		textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
		self.width = textureSurface.get_width()
		self.height = textureSurface.get_height()

		if self.width > self.height:
			ratio = self.height/self.width
			for x in range(len(self.verts)):
				self.verts[x][1] *= ratio

				"""self.verts = [ 
				[-1.0,ratio,0.0], 
				[0.0, ratio, 0.0], 
				[1.0,ratio,0.0], 
				[1.0,0.0,0.0], 
				[1.0,-ratio,0.0],  
				[0.0,-ratio,0.0],
				[-1.0,-ratio,0.0],
				[-1.0,0.0,0.0] ]"""

		else:
			ratio = self.width/self.height
			for x in range(len(self.verts)):
				self.verts[x][0] *= ratio

				"""self.verts = [ 
				[-ratio, 1.0 ,0.0], 
				[0.0, 1.0, 0.0], 
				[ratio, 1.0,0.0], 
				[ratio, 0.0,0.0], 
				[ratio ,-1.0,0.0],  
				[0.0,-1.0,0.0],
				[-ratio,-1.0,0.0],
				[-ratio ,0.0,0.0] ]"""

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

	def draw_surf(self):
		glPushMatrix()
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		glEnable(GL_BLEND)

		glTranslatef(self.data["pos"][0], self.data["pos"][1] , self.data["pos"][2])
		glRotatef(self.data["angle"], 0, 0, 1)
		glScalef(self.data["flipX"] * self.data["scale"],self.data["flipY"] * self.data["scale"],1.0)
		#self.data["angle"] = 0
		glBegin(GL_POLYGON)
		for x in range(len(self.verts)):
			glTexCoord2f(*self.coords[x])
			glVertex3f(*self.verts[x])

		glEnd()

		glDisable(GL_BLEND)
		glPopMatrix()

	def draw_entity(self):
		if self.dirname != None:
			glBindTexture(GL_TEXTURE_2D, self.texture_list[self.frame] )
			self.draw_surf()
			self.frame = (self.frame + 1) % len(self.texture_list)

	def draw_wire(self):
		glPushMatrix()
		glTranslatef(self.data["pos"][0], self.data["pos"][1] , self.data["pos"][2])
		glRotatef(self.data["angle"], 0, 0, 1)

		glBegin(GL_LINES)
		for Edge in self.edges:
			for Vertex in Edge:
				glVertex3fv(self.verts[Vertex])
		glEnd()
		glPopMatrix()	