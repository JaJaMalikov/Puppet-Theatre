import wx
import os
import copy
import pygame
from pygame.locals import Color
from collections import OrderedDict
from pygamepanel import PygamePanel
import  wx.lib.newevent, wx.stc as stc
from statusctrl import StatusCtrl
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
		self.width = 0
		self.height = 0
		self.texture_dict = {}
		self.portrait = None
		self.data["scale"] = 1
		self.data["angle"] = 0
		self.data["pos"] = [0,0,0]
		self.data["flipX"] = 1.0
		self.data["flipY"] = 1.0
		self.data["mouth"] = ord("z")
		self.data["substate"] = ord("a")
		self.data["state"] = ord("q")
		self.data["dir"] = pygame.K_DOWN
		self.data["visible"] = True
		self.data["frame"] = 0
		self.data["toggle"] = False
		self.verts = [ 
				[-1.0,1.0,0.0], 
				[0.0, 1.0, 0.0], 
				[1.0,1.0,0.0], 
				[1.0,0.0,0.0], 
				[1.0,-1.0,0.0],  
				[0.0,-1.0,0.0],
				[-1.0,-1.0,0.0],
				[-1.0,0.0,0.0] ]

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

	def load_all(self, dirname):
		self.dirname = dirname
		#mouth - z,x,c,v,b,n,m
		#state - q,w,e,r,t,y,u,i,o,p
		#substate - a,s,d,f,g,h,j,k,l
		#dirs - up, down, left, right

		mouth = ["z", "x", "c", "v", "b", "n", "m"]
		state = ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"]
		substate = ["a", "s", "d", "f", "g", "h", "j", "k", "l"]
		dirs = {"up":pygame.K_UP, "down":pygame.K_DOWN, "left":pygame.K_LEFT, "right":pygame.K_RIGHT}

		fullpath = os.path.join("res", self.dirname)
		file_list = os.listdir(fullpath)
		if "portrait.png" in file_list:
			self.portrait = os.path.join(fullpath, "portrait.png")

		for mouth_key in mouth:
			if mouth_key in file_list:
				self.texture_dict[ord(mouth_key)] = {}
				mouth_file_list = os.listdir(os.path.join(fullpath, mouth_key))

				for state_key in state:
					if state_key in mouth_file_list:
						self.texture_dict[ord(mouth_key)][ord(state_key)] = {}
						state_file_list = os.listdir(os.path.join(fullpath, mouth_key, state_key))

						for substate_key in substate:
							if substate_key in state_file_list:
								self.texture_dict[ord(mouth_key)][ord(state_key)][ord(substate_key)] = {}
								substate_file_list = os.listdir(os.path.join(fullpath, mouth_key, state_key, substate_key))

								for Dir in dirs.keys():
									if Dir in substate_file_list:
										self.texture_dict[ord(mouth_key)][ord(state_key)][ord(substate_key)][dirs[Dir]] = self.load_textures(os.path.join(fullpath, mouth_key, state_key, substate_key, Dir))

	def get_portrait(self):
		return self.portrait

	def space_toggle(self, toggle):
		self.data["toggle"] = toggle

	def set_data(self):
		self.HUD.set_Animating(True)
		self.HUD.set_yoffset(0)
		self.HUD.set_xoffset(0)
		self.HUD.set_playback(self.record.is_playing())
		self.HUD.set_recording(self.record.is_recording())
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

	def set_mouth(self, mouth):
		if mouth in self.texture_dict.keys():
			self.data["mouth"] = mouth

	def set_state(self, state):
		if state in self.texture_dict[self.data["mouth"]].keys():
			self.data["state"] = state

	def set_substate(self, substate):
		if substate in self.texture_dict[self.data["mouth"]][self.data["state"]].keys():
			self.data["substate"] = substate

	def set_dir(self, Dir):
		if Dir in self.texture_dict[self.data["mouth"]][self.data["state"]][self.data["substate"]].keys():
			self.data["dir"] = Dir

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
		if self.record.has_recorded():
			self.record.playback()

	def stop_playing(self):
		if self.record.has_recorded():
			self.record.stop()

	def clear(self):
		self.record.clear()

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

	def load_textures(self, dirname):
		text_list = []
		names = os.listdir(dirname)
		for name in names:
			text_list.append(self.load_texture(os.path.join(dirname, name)))
		return text_list

	def load_texture(self, name):

		self.verts = [ 
				[-1.0,1.0,0.0], 
				[0.0, 1.0, 0.0], 
				[1.0,1.0,0.0], 
				[1.0,0.0,0.0], 
				[1.0,-1.0,0.0],  
				[0.0,-1.0,0.0],
				[-1.0,-1.0,0.0],
				[-1.0,0.0,0.0] ]

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
		if self.dirname != None and self.data["visible"]:

			if self.data["toggle"] and (pygame.K_x in self.texture_dict.keys()):
				glBindTexture(GL_TEXTURE_2D, self.texture_dict[pygame.K_x][self.data["state"]][self.data["substate"]][self.data["dir"]][self.data["frame"]] )
				self.data["frame"] = (self.data["frame"] + 1) % len(self.texture_dict[pygame.K_x][self.data["state"]][self.data["substate"]][self.data["dir"]])
			else:
				glBindTexture(GL_TEXTURE_2D, self.texture_dict[self.data["mouth"]][self.data["state"]][self.data["substate"]][self.data["dir"]][self.data["frame"]] )
				self.data["frame"] = (self.data["frame"] + 1) % len(self.texture_dict[self.data["mouth"]][self.data["state"]][self.data["substate"]][self.data["dir"]])

			self.draw_surf()

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