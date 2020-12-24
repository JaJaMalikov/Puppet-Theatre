import wx
import os
import copy
import pygame
from pygame.locals import Color
from collections import OrderedDict
from listener import Key_listener

class Drawable(pygame.sprite.Sprite):
	def __init__(self, width, height):
		pygame.sprite.Sprite.__init__(self)
		self.width = width
		self.height = height
		self.main_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32).convert_alpha()
		self.rect = self.main_surf.get_rect()

	def draw(self, camera):
		camera.blit(self.main_surf, (self.rect))
