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
from ObjectList import ObjectList
from ImageList import ImageList

import data

class objCtrl(wx.Panel):
	def __init__(self, parent, data, window, Image_list):
		wx.Panel.__init__(self, parent,style = wx.RAISED_BORDER)
		self.data = data
		self.window = window
		self.mainBook = wx.Notebook(self)
		self.Image_list = Image_list

		self.newMultiImg = self.window.fileMenu.Append(wx.ID_ANY, 'Load Images', 'Multiple New images')

		mainBox = wx.BoxSizer(wx.HORIZONTAL)

		self.objList = ObjectList(self.mainBook, wx.ID_ANY, self.data, self.window, self)
		self.imgList = ImageList(self.mainBook, wx.ID_ANY, self.data, self.window, self, self.Image_list)

		self.mainBook.AddPage(self.objList , "objects" )
		self.mainBook.AddPage(self.imgList , "images" )

		mainBox.Add(self.mainBook, 4, wx.EXPAND)

		self.SetSizer(mainBox)

		self.window.Bind(wx.EVT_MENU, self.imgList.NewMultiImg , self.newMultiImg)

		self.objList.Bind(wx.EVT_LISTBOX_DCLICK, self.SwitchObject)
		self.imgList.Bind(wx.EVT_LISTBOX_DCLICK, self.SwitchImage)

	def Update(self, second):
		pass

	def set_data(self, data):
		self.data = data
		self.objList.set_data(self.data)
		self.imgList.set_data(self.data)

	def reload(self):
		self.objList.reload()
		self.imgList.reload()

	def SwitchImage(self, event):
		self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Current Image"] = self.imgList.get_selection()
		self.LoadStatus()

	def SwitchObject(self, event):
		self.data["Current Object"] = self.objList.get_string()
		self.imgList.set_current_list()

		self.LoadStatus()

	def LoadStatus(self):
		self.window.Set_First_Status(self.data["Current Object"])
		self.window.Set_Second_Status(self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Current Image"])

	def update_object(self):
		self.window.Set_First_Status(self.data["Current Object"])



class testFrame(wx.Frame):
	def __init__(self, parent, title, size):
		wx.Frame.__init__(self,
			parent, wx.ID_ANY, title, pos=(1,1), size=size,
			style = (wx.DEFAULT_FRAME_STYLE|wx.WANTS_CHARS))


		self.data = copy.deepcopy(data.data)

		self.Image_list = {}

		mainBox = wx.BoxSizer(wx.HORIZONTAL)


		self.menubar = wx.MenuBar()
		self.fileMenu = wx.Menu()

		#add elements and panels here to allow them to make changes to the window
		self.objCtrl = objCtrl(self, self.data, self, self.Image_list)

		self.loadData = self.fileMenu.Append(wx.ID_ANY, 'Load', 'Load Animation')
		self.closeWin = self.fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit Application')

		self.menubar.Append(self.fileMenu, '&File')
		self.SetMenuBar(self.menubar)

		#####################panel list

		mainBox.Add(self.objCtrl, 1, wx.EXPAND)
		#mainBox.Add(self.mainBook, 4, wx.EXPAND)

		self.SetSizer(mainBox)
		self.timer = wx.Timer(self)

		self.lastframe = datetime.now().second

		self.frames = 0
		#####################statusbar

		self.statusbar = self.CreateStatusBar(3)
		
		#####################bindings
		self.Bind(wx.EVT_TIMER, self.framerate, self.timer)

		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.Bind(wx.EVT_MENU, self.OnClose, self.closeWin)
		self.Bind(wx.EVT_MENU, self.LoadData, self.loadData)
		self.timer.Start()

	def framerate(self, event):
		if (datetime.now().second - self.lastframe) > 1:
			self.Set_Third_Status(str(self.frames) )
			self.lastframe = datetime.now().second
			self.frames = 0
		else:
			self.frames += 1


	def Set_First_Status(self, text):
		self.statusbar.SetStatusText( text , 0)

	def Set_Second_Status(self, text):
		self.statusbar.SetStatusText( text , 1)

	def Set_Third_Status(self, text):
		self.statusbar.SetStatusText( text , 2)

	def LoadData(self, event):
		with wx.FileDialog(self, "Load Animation", wildcard="PTA files (*.pta)|*.pta",
							style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
			if fileDialog.ShowModal() == wx.ID_CANCEL:
				return

			pathname = fileDialog.GetPath()

			tempData = open(pathname, "r")
			self.data = json.loads(tempData.read())
			tempData.close()
			self.LoadStatus()

	def OnClose(self, event):
		wx.Exit()
		exit()

if __name__ == '__main__':
	import pygame
	w,h = 10,10

	screen = pygame.display.set_mode((w,h))
	pygame.init()

	app = wx.App()
	view = testFrame(parent=None, title='Finger Pupper Theatre', size=(1500,700))
	view.Show()
	app.MainLoop()