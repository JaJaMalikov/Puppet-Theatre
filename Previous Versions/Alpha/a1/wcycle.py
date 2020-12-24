#!usr/bin/env python2

import pygame
from pygame.locals import *

class Entity:
	def __init__(self, name, width, height, x_pos, y_pos, size, frames):
		self.name = name
		self.rect = Pygame.Rect(x_pos, y_pos, width, height)
		self.width = width
		self.height = height
		self.ss = pygame.image.load("./" + name + ".png")
		self.dir = 0
		self.frame = 0
		self.frames = frames
		self.size = size

	def get_rect(self):
		return self.rect

	def set_pos(self, x_pos, y_pos):
		self.rect = rygame.Rect(x_pos, y_pos, self.width, self.height)

	def get_image(self):
		return self.ss.subsurface(pygame.Rect(self.frame * self.size, self.dir * self.size, self.width, self.height))

	def next_frame(self):
		self.frame += 1
		if self.frame == self.frames:
			self.frame = 0

	def change_dir(self, dir):
		self.dir = dir


class Mob(Entity):
	def __init__(self, name, width, height, x_pos, y_pos, size, frames):
		Entity.__init__(self, name, width, height, x_pos, y_pos, size, frames)

