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
import data

from OBJ2D import OBJ2D

class ObjectList(wx.Panel):
	def __init__(self, parent, ID, data, window, frame):
		wx.Panel.__init__(self, parent, ID)
		self.data = data
		self.window = window
		self.frame = frame
		self.buttonSizer = wx.BoxSizer(wx.VERTICAL)
		self.pageSizer = wx.BoxSizer(wx.VERTICAL)

		self.btn1 = wx.Button(self, 1, "New")
		self.btn2 = wx.Button(self, 1, "Delete")
		self.btn3 = wx.Button(self, 1, "Save")
		self.btn4 = wx.Button(self, 1, "Load")

		self.t_b_sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.b_b_sizer = wx.BoxSizer(wx.HORIZONTAL)

		self.t_b_sizer.Add(self.btn1)
		self.t_b_sizer.Add(self.btn2)
		self.b_b_sizer.Add(self.btn3)
		self.b_b_sizer.Add(self.btn4)
		self.buttonSizer.Add(self.t_b_sizer)
		self.buttonSizer.Add(self.b_b_sizer)
		self.pageSizer.Add(self.buttonSizer, 0)

		self.objList = wx.ListBox(self, wx.ID_ANY)

		self.pageSizer.Add(self.objList, -1, wx.EXPAND)

		self.SetSizer(self.pageSizer)

		self.objList.Set(list(self.data["Object List"].keys()) )

		self.btn1.Bind(wx.EVT_BUTTON, self.CreateNewObject)
		self.btn2.Bind(wx.EVT_BUTTON, self.DeleteObject)

	def set_data(self, data):
		self.data = data

	def reload(self):
		self.objList.Set(list(self.data["Object List"].keys()) )

	def DeleteObject(self, event):
		if self.data["Current Object"] != "Camera":
			self.window.Set_Third_Status(self.data["Current Object"] + " deleted")

			self.data["Object List"].pop(self.data["Current Object"])
			for frame in range(len(self.data["Frames"])):
				self.data["Frames"][frame].pop(self.data["Current Object"])

			self.data["Current Object"] = list(self.data["Object List"].keys())[0]

			self.objList.Set(list(self.data["Object List"].keys()) )

			self.frame.update_object()


	def CreateNewObject(self, event):
		box = wx.TextEntryDialog(None, "", "New Object Name", "new object")
		first = False
		if box.ShowModal() == wx.ID_OK:
			if len(self.data["Object List"]) < 1:
				first = True
			self.data["Object List"][box.GetValue()] = {"Images":[ "none" ]}

			for frame in range(len(self.data["Frames"])):
				self.data["Frames"][frame][box.GetValue()] = copy.deepcopy(data.default)

			self.data["Current Object"] = box.GetValue()
		self.objList.Set(list(self.data["Object List"].keys()) )
		self.frame.update_object()

	def get_string(self):
		return self.objList.GetString(self.objList.GetSelection())