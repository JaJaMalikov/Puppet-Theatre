import wx
import os
import copy
import pygame
from pygame.locals import Color
from collections import OrderedDict
from pygamepanel import PygamePanel
import  wx.lib.newevent, wx.stc as stc
from statusctrl import StatusCtrl


class objCtrl(wx.Panel):
	def __init__(self, parent, ID, HUD):
		wx.Panel.__init__(self, parent, ID)
		self.HUD = HUD
		self.cur_obj = 0
		self.cur_group = "Actors" # Actors, Cameras, BGs, Props

		self.buttons = []
		self.selector = wx.BoxSizer(wx.HORIZONTAL)

		#selection buttons
		pic = wx.Bitmap("defport.png", wx.BITMAP_TYPE_ANY)

		for x in range(10):
			self.buttons.append(wx.BitmapButton(self, -1, pic))

		for x in range(10):
			self.selector.Add(self.buttons[x], 0, wx.EXPAND)

		self.groups = wx.BoxSizer(wx.VERTICAL)
		self.tgroup = wx.BoxSizer(wx.HORIZONTAL)
		self.bgroup = wx.BoxSizer(wx.HORIZONTAL)

		self.Actors_button = wx.Button(self, label="Actors")
		self.Cameras_button = wx.Button(self, label="Cameras")
		self.Props_button = wx.Button(self, label="Props")
		self.BGs_button = wx.Button(self, label="BGs")

		self.tgroup.Add(self.Actors_button, 0, wx.EXPAND)
		self.tgroup.Add(self.Cameras_button, 0, wx.EXPAND)
		self.groups.Add(self.tgroup, 0, wx.EXPAND)

		self.bgroup.Add(self.Props_button, 0, wx.EXPAND)
		self.bgroup.Add(self.BGs_button, 0, wx.EXPAND)
		self.groups.Add(self.bgroup, 0, wx.EXPAND)

		self.selector.Add(self.groups, 0, wx.EXPAND)

		self.SetSizer(self.selector)
		self.SetAutoLayout(1)

	def get_cur(self):
		return self.cur_obj

	def set_obj(self, obj):
		self.cur_obj = obj

	def set_group(self, group):
		self.cur_group = group

	def update(self):
		self.HUD.set_group(self.cur_group)
		self.HUD.set_selection(self.cur_obj)
		