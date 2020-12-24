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

class Imageset(pygame.sprite.Sprite):
	def __init__(self, res_dir, set_name, scale):
		pygame.sprite.Sprite.__init__(self)
		self.set = []
		self.res_dir = res_dir
		self.set_name = set_name
		self.scale = scale
		self.rect = pygame.rect.Rect((0,0,0,0))
		self.center = None

	def load_images(self):
		self.set = []
		filelist = os.listdir(os.path.join(self.res_dir, self.set_name))
		filelist.sort()
		for file in filelist:
			try:
				#self.set.append(pygame.transform.rotozoom(pygame.image.load(os.path.join(self.res_dir, self.set_name, file)).convert_alpha(),0,self.scale))
				img = pygame.image.load(os.path.join(self.res_dir, self.set_name, file)).convert_alpha()
				self.set.append(pygame.transform.smoothscale(img, (int(self.scale*img.get_rect().w),int(self.scale*img.get_rect().h)) ))
			except:
				pass
		self.rect = self.set[0].get_rect()

	def append(self, img):
		self.set.append(img)
		self.rect = self.set[0].get_rect()

	def reset(self):
		self.rect.center = self.center

	def set_scale(self, scale):
		self.scale = scale

	def get(self, index):
		return self.set[index]

	def len(self):
		return len(self.set)

	def max(self):
		return len(self.set)-1

	def clear(self):
		self.set = []

	def set_pos(self, center):
		self.center = center
		self.rect.center = center

	def get_pos(self):
		cur_rect = self.set[0].get_rect()
		cur_rect.center = (int(self.rect.center[0] * self.scale), int(self.rect.center[1] * self.scale))
		return cur_rect

