import wx
import os
import copy
import pygame
from pygame.locals import Color
from collections import OrderedDict
from manager import Manager
from listener import Key_listener


class PygamePanel(wx.Panel):
	def __init__(self, parent, ID, ViewPortSize):
		#in the name of god do not touch this part
		global pygame
		wx.Panel.__init__(self, parent, ID, size=ViewPortSize)
		self.Fit()
		os.environ['SDL_WINDOWID'] = str(self.GetHandle())
		os.environ['SDL_VIDEODRIVER'] = 'windib'
		import pygame # this has to happen after setting the environment variables.
		pygame.init()
		#seriously do not fuck with anything between these lines


		self.width, self.height = ViewPortSize

		self.screen = pygame.display.set_mode(ViewPortSize)
		self.listener = Key_listener()
		self.manager = Manager(self.width, self.height, self.listener, "freesansbold.ttf")

	def update(self, evt):
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				self.listener.set_keydown(event.key)
			if event.type == pygame.KEYUP:
				self.listener.set_keyup(event.key)
			if event.type == pygame.MOUSEBUTTONDOWN:
				self.listener.set_mouse_down(event.button)
			if event.type == pygame.MOUSEBUTTONUP:
				self.listener.set_mouse_up(event.button)
		self.listener.set_mouse_pos(pygame.mouse.get_pos())

		self.screen.fill((0,0,0))

		###########update functions go here
		self.manager.update()

		###########end update functions

		self.manager.draw(self.screen)

		self.listener.clear_struck()

		pygame.display.flip()

	def OnClose(self):
		self.manager.kill()
		pygame.quit()