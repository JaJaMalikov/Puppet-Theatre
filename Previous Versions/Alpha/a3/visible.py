import pygame
import time
import sys
import os
import random
from collections import OrderedDict
from collections import deque
import json
import copy
import pygame.font
from pygame.locals import Color
from record import Record

class Visible(pygame.sprite.Sprite):
	def __init__(self, center, w, h, listener, framerate, scale):
		pygame.sprite.Sprite.__init__(self)
		self.framerate = framerate
		self.data = {}
		self.width = w
		self.height = h
		self.scale = scale
		self.data["rect"] = pygame.Rect(0,0,int(self.width*self.scale), int(self.height*self.scale))
		self.data["rect"].center = center
		self.main_surf = None
		self.record = Record()
		self.listener = listener
		self.active = False

	def set_active(self):
		if self.active:
			self.active = False
		else:
			self.active = True

	def handle_recording(self):
		if self.active:
			#used for all recordable objects
			if self.listener.get_struck(pygame.K_EQUALS):
				self.record.start()
			if self.listener.get_struck(pygame.K_LEFTBRACKET):
				self.record.pause()
			if self.listener.get_struck(pygame.K_RIGHTBRACKET):
				self.record.resume()
			if self.listener.get_struck(pygame.K_BACKSLASH):
				self.record.clear()
			if self.listener.get_struck(pygame.K_SEMICOLON):
				self.record.playback()
			if self.listener.get_struck(pygame.K_QUOTE): 
				self.record.stop()

		if self.listener.get_struck(pygame.K_p):
			self.record.reset()
			self.record.playback()
		if self.listener.get_struck(pygame.K_SLASH):
			self.record.reset()
			self.record.playback()

		if self.record.is_recording():
			self.record.append(self.data)
		if self.record.is_playing():
			try:
				self.data = copy.deepcopy(self.record.get())
				self.record.next()

				#self.build()
			except:
				pass

	def build(self):
		#generates the full imagesets again, 
		pass

	def update(self):
		#to include a list of all nessesary actions, key listening and state manipulation
		#will always call handle_recording to ensure that recording states are handled appropriately
		pass

	def resize(self):
		#will alter the size of all images and call resize_rect(scale) in order to keep the positions of the objects on screen in their appropriate locations
		pass

	def set_scale(self, scale):
		self.scale = scale
		center = self.data["rect"].center
		#self.data["rect"] = pygame.Rect(0,0,int(self.width*self.scale), int(self.height*self.scale))
		#self.data["rect"].center = center
		self.build()

	def resize_rect(self):
		cur_rect = pygame.Rect(0,0,int(self.width*self.scale), int(self.height*self.scale))
		cur_rect.center = (self.data["rect"].center[0]*self.scale, self.data["rect"].center[1] * self.scale)
		return cur_rect

	def draw(self, camera):
		camera.blit(self.main_surf, self.resize_rect())
