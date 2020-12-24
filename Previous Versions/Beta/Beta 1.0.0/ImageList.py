import wx
import os
import copy

from wx import glcanvas

from collections import OrderedDict

import pygame
from pygame.locals import *


import  wx.lib.newevent, wx.stc as stc
import numpy as np

from OpenGL.GL import *
from OpenGL.GLU import *

import json

import random
import string

import datetime
from datetime import datetime

import verts

import random

from OBJ2D import OBJ2D

class ImageList(wx.Panel ):
	def __init__(self, parent, ID, data, window, frame, Image_list):
		wx.ListBox.__init__(self, parent, ID)
		self.Image_list = Image_list
		self.parent = parent
		self.data = data
		self.window = window
		self.frame = frame

		self.buttonSizer = wx.BoxSizer(wx.VERTICAL)
		self.pageSizer = wx.BoxSizer(wx.VERTICAL)

		self.load_btn = wx.Button(self, 1, "Load")
		self.delete_btn = wx.Button(self, 1, "Delete")
		self.up_btn = wx.Button(self, 1, "Raise")
		self.down_btn = wx.Button(self, 1, "Lower")

		self.t_b_sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.b_b_sizer = wx.BoxSizer(wx.HORIZONTAL)

		self.t_b_sizer.Add(self.load_btn)
		self.t_b_sizer.Add(self.delete_btn)
		self.b_b_sizer.Add(self.up_btn)
		self.b_b_sizer.Add(self.down_btn)
		self.buttonSizer.Add(self.t_b_sizer)
		self.buttonSizer.Add(self.b_b_sizer)

		self.imgList = wx.ListBox(self, wx.ID_ANY, style=wx.LB_HSCROLL)

		self.pageSizer.Add(self.buttonSizer, 0)
		self.pageSizer.Add(self.imgList, -1, wx.EXPAND)

		self.overwrite_panel = wx.Panel(self, size=(167, 90))

		self.overwrite_label = wx.StaticText(self.overwrite_panel, label="Overwrite:", pos=(0,25))
		self.overwrite_all = wx.Button(self.overwrite_panel, label="All", pos=(85, 22))

		self.overwrite_last = wx.Button(self.overwrite_panel, label="Previous", pos=(0, 44))
		self.overwrite_next = wx.Button(self.overwrite_panel, label="Next", pos=(85, 44))

		self.overwrite_future = wx.Button(self.overwrite_panel, label="Subsequent", pos=(0,66))
		self.overwrite_past = wx.Button(self.overwrite_panel, label="Preceeding", pos=(85,66))

		self.pageSizer.Add(self.overwrite_panel, 0)

		self.SetSizer(self.pageSizer)

		self.load_btn.Bind(wx.EVT_BUTTON, self.NewMultiImg)
		self.delete_btn.Bind(wx.EVT_BUTTON, self.removeImg)
		self.up_btn.Bind(wx.EVT_BUTTON, self.move_up)
		self.down_btn.Bind(wx.EVT_BUTTON, self.move_down)

		self.overwrite_next.Bind(wx.EVT_BUTTON, self.On_overwrite_next)
		self.overwrite_last.Bind(wx.EVT_BUTTON, self.On_overwrite_last)

		self.overwrite_all.Bind(wx.EVT_BUTTON, self.On_overwrite_all)

		self.overwrite_past.Bind(wx.EVT_BUTTON, self.On_overwrite_past)
		self.overwrite_future.Bind(wx.EVT_BUTTON, self.On_overwrite_future)

	def On_overwrite_future(self, event):
		ref = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Current Image"]
		for frame in range( self.data["Current Frame"], len(self.data["Frames"])):
			self.data["Frames"][frame][self.data["Current Object"]]["Current Image"] = ref

	def On_overwrite_past(self, event):
		ref = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Current Image"]
		for frame in range(0, self.data["Current Frame"]):
			self.data["Frames"][frame][self.data["Current Object"]]["Current Image"] = ref

	def On_overwrite_all(self, event):
		ref = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Current Image"]
		for frame in range(len(self.data["Frames"])):
			self.data["Frames"][frame][self.data["Current Object"]]["Current Image"] = ref

	def On_overwrite_last(self, event):
		ref = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Current Image"]
		self.data["Frames"][self.data["Current Frame"]-1][self.data["Current Object"]]["Current Image"] = ref
		self.window.timelineCtrl.onBack(1)

	def On_overwrite_next(self, event):
		ref = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Current Image"]
		self.data["Frames"][self.data["Current Frame"]+1][self.data["Current Object"]]["Current Image"] = ref
		self.window.timelineCtrl.onNext(1)

	def set_data(self, data):
		self.data = data

	def reload(self):
		for image in self.data["imgs"]:
			self.AddImg(image, False)
		self.set_list(self.data["Current Object"])

	def move_up(self, event):
		img = self.get_selection()
		pos = self.data["Object List"][self.data["Current Object"]]["Images"].index(img)

		if pos != 0:
			self.data["Object List"][self.data["Current Object"]]["Images"].remove(img)
			self.data["Object List"][self.data["Current Object"]]["Images"].insert(pos-1, img)
			new_pos = pos-1
		else:
			self.data["Object List"][self.data["Current Object"]]["Images"].remove(img)
			self.data["Object List"][self.data["Current Object"]]["Images"].append(img)
			new_pos = len(self.data["Object List"][self.data["Current Object"]]["Images"])-1

		self.set_list(self.data["Current Object"])
		self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Current Image"] = self.imgList.GetString(new_pos)
		self.imgList.SetSelection(new_pos)

	def move_down(self, event):
		img = self.get_selection()
		pos = self.data["Object List"][self.data["Current Object"]]["Images"].index(img)

		if pos == len(self.data["Object List"][self.data["Current Object"]]["Images"])-1:
			new_pos = 0
		else:
			new_pos = pos+1

		self.data["Object List"][self.data["Current Object"]]["Images"].remove(img)
		self.data["Object List"][self.data["Current Object"]]["Images"].insert(new_pos , img)

		self.set_list(self.data["Current Object"])
		self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Current Image"] = self.imgList.GetString(new_pos )
		self.imgList.SetSelection(new_pos)

	def NewMultiImg(self, event):
		with wx.FileDialog(self, "Import Files", wildcard="PNG files (*.png)|*.png",
							style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE) as fileDialog:
			if (fileDialog.ShowModal() == wx.ID_CANCEL):
				return

			pathnames = fileDialog.GetPaths()

			for pathname in pathnames:
				self.data["imgs"].append(pathname)
				self.AddImg(pathname, True)

	def AddImg(self, pathname, new):

		img_num = pathname.count("\\")
		img_tag = pathname.split("\\", img_num-1)[-1]

		if pathname not in self.Image_list.keys():
			self.Image_list[img_tag ] = OBJ2D(pathname)

		if new:
			self.data["Object List"][self.data["Current Object"]]["Images"].append(img_tag )

		self.set_current_list()
		if len(self.data["Object List"][self.data["Current Object"]]["Images"]) == 1:
			for x in range(len(self.data["Frames"])):
				self.data["Frames"][x][self.data["Current Object"]]["Current Image"] = self.get_first()
		self.frame.LoadStatus()

	def removeImg(self, event):
		self.data["Object List"][self.data["Current Object"]]["Images"].remove(self.get_selection())
		self.set_list(self.data["Current Object"])
		self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Current Image"] = self.get_first()

	def set_list(self, cur_obj):
		self.imgList.Set(self.data["Object List"][cur_obj]["Images"])

	def set_current_list(self):
		self.imgList.Set(self.data["Object List"][self.data["Current Object"]]["Images"])
		if len(self.data["Object List"][self.data["Current Object"]]["Images"]) == 1:
			self.frame.LoadStatus()

	def get_selection(self):
		return self.imgList.GetString(self.imgList.GetSelection())

	def get_first(self):
		return self.imgList.GetString(0)
