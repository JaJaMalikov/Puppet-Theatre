#!/usr/bin/env python2

import pygame
import time
import os
from pygame.locals import *
import testdef

settings = {
	"bg_color":(255,255,255),
	"width_and_height":(800,600),
	"name":"RPG game",
	"framerate":30
}

class game:
	def __init__(self, settings):
		self.data = settings
		pygame.init()
		self.screen = pygame.display.set_mode(self.data["width_and_height"])
		self.screen.fill(self.data["background_colour"])
		self.running = True
		self.clock = pygame.time.Clock()
		self.listener = testdef.listener()

	def run(self):
		while self.running:
			self.clock.tick(self.data["framerate"])
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
				if event.type == pygame.KEYDOWN:
					self.listener.set_keydown(event.key)
				if event.type == pygame.KEYUP:
					self.listener.set_keyup(event.key)

			############### responses go here ###################
			self.screen.fill(self.data["background_colour"])
			pygame.display.flip()

class scene:
	def __init__(self, script):
		self.script = script
		self.surf_array = OrderedDict()
		self.main_surf = pygame.Surface([self.frames*self.width, self.height*4], pygame.SRCALPHA, 32).convert_alpha()

	def update(self):
		for cur_surf in self.surf_array:
			self.main_surf.blit(self.surf_array[cur_surf], (0,0))

	def get_sur(self):
		return self.main_surf

class menu:
	def __init__(self):
		self.surf = None


	def update(self):

if __name__ == "__main__":
	game = game()
	game.run()