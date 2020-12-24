import pygame
import time
import sys
import os
import random
from collections import OrderedDict
from collections import deque
import json
import copy


class Imageset:
	#holds all images for a specific object
	def __init__(self, name):
		self.frame = 0
		self.imageset = []
		filelist = os.listdir("res/" + name)
		filelist.sort()
		print(filelist)
		for file in filelist:
			try:
				self.imageset.append(pygame.image.load("res/" + name + "/" + file))
			except:
				pass

	def cur(self):
		return self.imageset[self.frame]

	def get(self, frame):
		return self.imageset[frame]

	def len(self):
		return len(self.imageset)

	def adv(self):
		self.frame += 1
		if self.frame >= len(self.imageset):
			self.frame = 0

	def rec(self):
		self.frame -= 1
		if self.frame <= 0:
			self.frame = len(self.imageset)-1