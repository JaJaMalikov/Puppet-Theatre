# -*- coding: ascii -*-
import wx, sys, os, wx.lib.newevent, wx.stc as stc, string
from datetime import datetime
import threading, random, socket, select
from time import ctime
from manager import Manager
from listener import Key_listener


class PygamePanel(wx.Panel):
	def __init__(self, parent, ID, tplSize, frameType):
		global pygame
		wx.Panel.__init__(self, parent, ID, size=tplSize)
		self.Fit()
		os.environ['SDL_WINDOWID'] = str(self.GetHandle())
		os.environ['SDL_VIDEODRIVER'] = 'windib'
		import pygame # this has to happen after setting the environment variables.
		pygame.init()
		self.frame = 0
		self.screen = pygame.display.set_mode(tplSize,  pygame.RESIZABLE)
		self.listener = Key_listener()
		if frameType == "animator":
			self.manager = Manager(tplSize[0], tplSize[1], 1000, self.listener)

	def importPNG(self, name):
		#try:
		self.manager.importPNG(name)
		#except IOError:
		#	raise

	def importAnimation(self, name):
		#try:
		self.manager.importAnimation(name)
		#except IOError:
		#	raise 

	def importObject(self, name, ID):
		#try:
		self.manager.importObject(name, ID)
		#except IOError:
		#	raise 

	def resize(self):
		self.manager.resize(self.GetSize())

	def update(self, evt):
		self.frame += 1
		for event in pygame.event.get():
			print(event)
			if event.type == pygame.QUIT:
				self.manager.kill()
			if event.type == pygame.KEYDOWN:
				self.listener.set_keydown(event.key)
			if event.type == pygame.KEYUP:
				self.listener.set_keyup(event.key)
			if event.type == pygame.MOUSEBUTTONDOWN:
				self.listener.set_mouse_down(event.button)
			if event.type == pygame.MOUSEBUTTONUP:
				self.listener.set_mouse_up(event.button)
		self.listener.set_mouse_pos(pygame.mouse.get_pos())


		self.manager.update()

		self.screen.fill((self.frame%255,0,0))
		self.manager.draw(self.screen)

		self.listener.clear_struck()

		pygame.display.flip()

	def OnClose(self):
		pygame.quit()
