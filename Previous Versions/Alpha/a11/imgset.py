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
		self.set = OrderedDict()
		self.res_dir = res_dir
		self.set_name = set_name
		self.scale = scale
		self.rect = pygame.rect.Rect((0,0,0,0))
		self.center = None
		self.cur_img = 0

	def get_loaded(self):
		return (len(self.set) > 0)

	def change_set(self, res_dir, set_name, scale):
		self.scale = scale
		self.res_dir = res_dir
		self.set_name = set_name
		self.load_images()

	def load_images(self):
		self.set = OrderedDict()
		filelist = os.listdir(self.res_dir)
		print(filelist)
		filelist.remove("portrait.png")
		filelist.sort()
		for file in filelist:
			#try:
				#self.set.append(pygame.transform.rotozoom(pygame.image.load(os.path.join(self.res_dir, self.set_name, file)).convert_alpha(),0,self.scale))
			img = pygame.image.load(os.path.join(self.res_dir, file)).convert_alpha()
			self.set[file[:-4]] = (pygame.transform.smoothscale(img, (int(self.scale*img.get_rect().w),int(self.scale*img.get_rect().h)) ))
			#except:
			#	pass
		self.rect = self.get_index(0).get_rect()
		print(len(self.set))

	def append(self, name, img):
		self.set[name] = img
		self.rect = self.get_index(0).get_rect()

	def next(self):
		self.cur_img = (self.cur_img + 1) % len(self.set)

	def prev(self):
		self.cur_img = (self.cur_img - 1) % len(self.set)

	def get(self):
		return self.get_index(self.cur_img)

	def reset(self):
		self.rect.center = self.center
		#print(self.set_name, self.rect.center)

	def set_scale(self, scale):
		self.scale = scale

	def get_index(self, index):
		return self.set[list(self.set.keys())[index]]

	def get_key(self, key):
		return self.set[key]

	def len(self):
		return len(self.set)

	def max(self):
		return len(self.set)-1

	def clear(self):
		self.set = OrderedDict()

	def set_pos(self, center):
		self.center = center
		self.rect.center = center

	def get_pos(self):
		cur_rect = self.get_index(0).get_rect()
		cur_rect.center = (int(self.rect.center[0] * self.scale), int(self.rect.center[1] * self.scale))
		return cur_rect

