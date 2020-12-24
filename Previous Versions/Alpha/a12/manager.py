import wx
import os
import copy
import pygame
from pygame.locals import Color
from collections import OrderedDict
#from drawable import Drawable
from HUD import HUD
from itertools import chain
import random

class Drawable(pygame.sprite.Sprite):
	def __init__(self, width, height):
		pygame.sprite.Sprite.__init__(self)
		self.data = {}
		self.width = width
		self.height = height
		self.build()

	def draw(self, camera):
		camera.blit(self.main_surf, (self.data["rect"]))

	def build(self):
		self.main_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32).convert_alpha()
		self.data["rect"] = self.main_surf.get_rect()

	def set_size(self, width, height):
		self.width = width
		self.height = height

class Stage(Drawable):
	def __init__(self):
		Drawable.__init__(self, 1,1)


class Onstage(Drawable):
	def __init__(self, HUD):
		Drawable.__init__(self, 1,1)
		self.HUD = HUD
		self.data["dist"] = random.randrange(30)
		self.data["speed"] = random.randrange(10)
		self.data["Flip H"] = random.choice([False,True])
		self.data["Flip V"] = random.choice([False,True])
		self.data["angle"] = random.randrange(360)
		self.data["state"] = "default"
		self.data["substate"] = "default"
		self.data["mouth"] = "default"
		self.data["X offset"] = random.randrange(200)
		self.data["Y offset"] = random.randrange(200)
		self.data["Animating"] = random.choice([True,False])
		self.recording = False
		self.playback = False

	def set_data(self):
		self.HUD.set_Speed(self.data["speed"])
		self.HUD.set_FLIP_H(self.data["Flip H"])
		self.HUD.set_FLIP_V(self.data["Flip V"])
		self.HUD.set_pos(self.data["rect"].center)
		self.HUD.set_angle(self.data["angle"])
		self.HUD.set_state(self.data["state"])
		self.HUD.set_substate(self.data["substate"])
		self.HUD.set_mouth(self.data["mouth"])
		self.HUD.set_xoffset(self.data["X offset"])
		self.HUD.set_yoffset(self.data["Y offset"])
		self.HUD.set_Animating(self.data["Animating"])
		self.HUD.set_recording(self.recording)
		self.HUD.set_playback(self.playback)

class Actor(Onstage):
	def __init__(self, HUD):
		Onstage.__init__(self, HUD)

	def update(self):
		self.set_data()

class BG(Onstage):
	def __init__(self, HUD):
		Onstage.__init__(self, HUD)

	def update(self):
		self.set_data()

class Prop(Onstage):
	def __init__(self, HUD):
		Onstage.__init__(self, HUD)

	def update(self):
		self.set_data()

class contain:
	def __init__(self, thing, HUD):
		self.HUD = HUD
		self.obj_list = []
		for x in range(10):
			self.obj_list.append(thing(self.HUD))
		self.selection = random.randrange(10)

	def get(self):
		return self.obj_list

	def set_data(self):
		self.HUD.set_selection(self.selection)
		self.obj_list[self.selection].set_data()

	def get_index(self, index):
		return self.obj_list[index]

	def get_selection(self):
		return self.get_index(self.selection)

	def set_selection(self, selection):
		self.selection = selection

class Actors(contain):
	def __init__(self, HUD):
		contain.__init__(self, Actor, HUD)

class BGs(contain):
	def __init__(self, HUD):
		contain.__init__(self, BG, HUD)

class Props(contain):
	def __init__(self, HUD):
		contain.__init__(self, Prop, HUD)

class Cameras:
	def __init__(self, visisble, HUD):
		pass

class Camera:
	def __init__(self):
		pass

class Cards(Drawable):
	def __init__(self, width, height):
		Drawable.__init__(self, width, height)

class Visible:
	def __init__(self, *groups):
		print(type(groups))
		print(type(groups[0].get()))
		self.sprites = []#list(chain([ obj.get() for obj in groups]))
		for obj in groups:
			self.sprites.extend(obj.get())
		self.default_order = [x for x in range(len(self.sprites))]

	def order(self):
		return [x for _, x in sorted(zip( self.sprites, self.default_order ), key=lambda x: x[0].data["dist"] )]

	def get_list(self):
		return self.sprites

	def get_sprite(self, index):
		return self.sprites[index]

class Manager(Drawable):
	def __init__(self, width, height, listener, font):
		Drawable.__init__(self, width, height)
		self.clock = pygame.time.Clock()
		self.font = pygame.font.Font(font, 20)
		self.listener = listener
		self.HUD = HUD(self.width, self.height, self.font)
		self.running = True

		self.mouse = 0
		self.mouse_range = ["center", "rotate", "drag"]

		self.group = "Actors"

		self.groups = {"Actors": Actors(self.HUD),"Props": Props(self.HUD),"BGs": BGs(self.HUD)}

		self.visible = Visible( self.groups["Actors"], self.groups["Props"], self.groups["BGs"] )
		self.cameras = Cameras(self.visible, self.HUD)

	def update(self):
		if self.running:
			self.main_surf.fill((255,255,255))

			#### track input events
			if self.listener.get_struck(pygame.K_BACKSLASH):
				self.mouse = (self.mouse + 1) %3

			if self.listener.get_key(pygame.K_F1):
				self.group = "Actors"
			if self.listener.get_key(pygame.K_F2):
				self.group = "Cameras"
			if self.listener.get_key(pygame.K_F3):
				self.group = "Props"
			if self.listener.get_key(pygame.K_F4):
				self.group = "BGs"

			if self.listener.get_key(pygame.K_KP0):
				self.groups[self.group].set_selection(0)
			if self.listener.get_key(pygame.K_KP1):
				self.groups[self.group].set_selection(1)
			if self.listener.get_key(pygame.K_KP2):
				self.groups[self.group].set_selection(2)
			if self.listener.get_key(pygame.K_KP3):
				self.groups[self.group].set_selection(3)
			if self.listener.get_key(pygame.K_KP4):
				self.groups[self.group].set_selection(4)
			if self.listener.get_key(pygame.K_KP5):
				self.groups[self.group].set_selection(5)
			if self.listener.get_key(pygame.K_KP6):
				self.groups[self.group].set_selection(6)
			if self.listener.get_key(pygame.K_KP7):
				self.groups[self.group].set_selection(7)
			if self.listener.get_key(pygame.K_KP8):
				self.groups[self.group].set_selection(8)
			if self.listener.get_key(pygame.K_KP9):
				self.groups[self.group].set_selection(9)

			self.HUD.set_group(self.group)
			self.HUD.set_FPS(int(self.clock.get_fps()))
			self.HUD.set_MPos(self.listener.get_mouse_pos())
			self.HUD.set_mouse(self.mouse_range[self.mouse])

			if self.group in self.groups.keys():
				self.groups[self.group].set_data()

			self.HUD.update()
			self.HUD.draw(self.main_surf)
			self.clock.tick(2000)

	def kill(self):
		self.running = False