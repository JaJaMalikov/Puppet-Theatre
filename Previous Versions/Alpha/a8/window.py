#!/usr/bin/env python3

import pygame
from pygame.locals import Color
from listener import Key_listener
from manager import Manager

class Window:
	def __init__(self, width, height, tile_size, title, framerate):
		"""
		window class contains all sub classes, will run at framerate with manager running all subclasses
		
		"""
		pygame.init()
		self.title = title
		self.tile_size = tile_size
		self.width = width * self.tile_size
		self.height = height * self.tile_size
		self.screen = pygame.display.set_mode((self.width, self.height))
		self.listener = Key_listener()
		self.framerate = framerate
		pygame.display.set_caption(self.title)
		self.manager = Manager(self.width, self.height, self.framerate, self.listener)

	def run(self):
		#updates using the manager class, get_run return true if running
		#draw sends screen down rabbit hole to be drawn on, allows a single draw call to 
		#append everything from all objects in all states
		while self.manager.get_run():
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.manager.kill()
				if event.type == pygame.KEYDOWN:
					self.listener.set_keydown(event.key)
				if event.type == pygame.KEYUP:
					self.listener.set_keyup(event.key)
				if event.type == pygame.MOUSEBUTTONDOWN:
					self.listener.set_mouse_down(event.button)
				if event.type == pygame.MOUSEBUTTONUP:
					self.listener.set_mouse_up(event.button)

			self.listener.set_mouse_pos(pygame.mouse.get_pos())

			self.manager.update()

			self.screen.fill((0,0,0))
			self.manager.draw(self.screen)

			pygame.display.flip()
			self.listener.clear_struck()