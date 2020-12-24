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

from visible import Visible

import imgset

class Captions(Visible):
	#static bar which holds the captions, records itself as you tab through the script, imposing black bar on the bottom
	def __init__(self, length, script, w, h, center, font, size, listener, scale):
		Visible.__init__(self, center, w, h, listener, 1, scale, 1)
		self.font = font
		self.script = script
		self.font_size = size
		self.data["cur_line"] = 0
		self.parsed_script = []
		self.imgset = imgset.Imageset(None, None, scale)
		self.split_string(length)
		self.main_surf = pygame.Surface([self.data["rect"].w, self.data["rect"].h], pygame.SRCALPHA, 32).convert_alpha()
		#self.resize_rect(scale)
		self.build()

	def split_string(self,limit, sep=" "):
		sentences = self.script.split("\n")
		final = []
		for sentence in sentences:
			try:
				words = sentence.split()
				if max(map(len, words)) > limit:
					raise ValueError("limit is too small")
				res, part, others = [], words[0], words[1:]
				for word in others:
					if len(sep)+len(word) > limit-len(part):
						res.append(part)
						part = word
					else:
						part += sep+word
				if part:
					res.append(part)
				print(res)
				final += res
			except:
				final.append("")
		self.parsed_script = final

	def next(self):
		self.data["cur_line"] += 1
		if self.data["cur_line"] >= self.imgset.len():
			self.data["cur_line"] = 0

	def prev(self):
		self.data["cur_line"] -= 1
		if self.data["cur_line"] < 0:
			self.data["cur_line"] = self.imgset.max()

	def update(self):
		if self.active:
			#personalized keys
			if self.listener.get_struck(pygame.K_LEFT):
				self.prev()
			if self.listener.get_struck(pygame.K_RIGHT):
				self.next()

		self.handle_recording()
		self.main_surf = self.imgset.get(self.data["cur_line"])

	def build(self):
		self.imgset.clear()
		for line in self.parsed_script:
			cur_font = pygame.font.Font(self.font + '.ttf', int(self.font_size*self.scale))
			cur_surf = pygame.Surface([int(self.width*self.scale), int(self.height*self.scale)], pygame.SRCALPHA, 32).convert_alpha()
			cur_surf.fill(Color("black"))
			render = cur_font.render(line, True, Color("white"))
			rend_rect = render.get_rect()
			rend_rect.center = (int(self.width*self.scale)/2, int(self.height*self.scale/2))
			cur_surf.blit(render, rend_rect)
			self.imgset.append(cur_surf)
