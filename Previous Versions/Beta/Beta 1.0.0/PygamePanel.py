import wx
import os

import wx.media

from pygame.locals import *

import  wx.lib.newevent, wx.stc as stc
import numpy as np

import datetime
from datetime import datetime
import sampler

from consts import * 

import copy

class PygamePanel(wx.Panel):
	def __init__(self, parent, ID, ViewPortSize, window):
		global pygame
		wx.Panel.__init__(self, parent, ID, size=ViewPortSize)
		self.Fit()
		os.environ['SDL_WINDOWID'] = str(self.GetHandle())
		os.environ['SDL_VIDEODRIVER'] = 'windib'
		import pygame
		pygame.init()

		self.SetBackgroundColour((10,100,10))
		self.set_clear_color((0,0,0))
		self.set_size(ViewPortSize)
		self.layout()

	def set_clear_color(self, color):
		self.clear_color = color

	def set_size(self, new_size):
		self.SetSize(new_size)
		self.size=new_size
		self.ViewPortSize = new_size
		self.length, self.height = new_size

	def layout(self):
		self.screen = pygame.display.set_mode(self.ViewPortSize, pygame.RESIZABLE)

	def draw(self, image, pos):
		self.screen.blit(image, pos)

	def Update(self):
		pygame.display.flip()
		self.screen.fill(self.clear_color)

	def OnClose(self):
		pygame.quit()
