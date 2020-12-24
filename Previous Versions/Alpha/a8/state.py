import pygame
from pygame.locals import Color
import listener


"""
state prototypes
"""
class State:
	def __init__(self, width, height, listener, color):
		self.width = width
		self.height = height
		self.listener = listener
		self.main_surface = pygame.Surface( (self.width, self.height) , pygame.SRCALPHA, 32).convert_alpha()
		self.main_rect = self.main_surface.get_rect()
		self.frame = 0
		self.color = color
		self.substates = {}

	def update(self):
		#this must return either it's own ID or the ID of another state
		pass

	def onExit(self, code):
		self.main_surface = pygame.Surface( (self.width, self.height) , pygame.SRCALPHA, 32).convert_alpha()
		self.main_rect = self.main_surface.get_rect()
		self.frame = 0
		return code		

	def draw(self, surf):
		surf.blit(self.main_surface, (0,0))