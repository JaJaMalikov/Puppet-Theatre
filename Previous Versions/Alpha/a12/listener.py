import wx
import os
import copy
import pygame
from pygame.locals import Color
from collections import OrderedDict

class Key_listener:
	#holds current key states
	def __init__(self):
		self.keymap = {v: k for v, k in enumerate([False] * 512 )}
		self.struck = [False]*512
		self.mouse_button = [False]*10
		self.mouse_pos = (0,0)

	def set_keydown(self, key):
		self.struck[key] = True
		self.keymap[key] = True

	def set_keyup(self, key):
		self.struck[key] = False
		self.keymap[key] = False

	def set_mouse_down(self, button):
		"""
		event.button: [1:left, 2:middle, 3:right, 4:scroll up, 5:scroll down]
		"""
		self.mouse_button[button] = True

	def set_mouse_up(self, button):
		self.mouse_button[button] = False

	def set_mouse_pos(self, pos):
		self.mouse_pos = pos

	def get_mouse_button(self, button):
		return self.mouse_button[button]

	def get_mouse_pos(self):
		return self.mouse_pos

	def get_key(self, key):
		return self.keymap[key]

	def get_state(self):
		return copy.deepcopy(self.keymap)

	def get_struck(self, key):
		return self.struck[key]

	def clear_struck(self):
		self.struck = [False]*512

	def get_all(self):
		return [k for k,v in self.keymap.items() if v == True]