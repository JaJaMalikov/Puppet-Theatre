import wx
import os
import copy
import pygame
from pygame.locals import Color
from collections import OrderedDict
from pygamepanel import PygamePanel
import  wx.lib.newevent, wx.stc as stc
from statusctrl import StatusCtrl
from objctrl import objCtrl
from listener import Key_listener
from plane import OBJ2D as plane
from model import OBJ3D as massObj
import numpy as np

from OpenGL.GL import *
from OpenGL.GLU import *

from PG_GL import PygamePanel

"""
Laughware Finger Puppet Theatre
purpose: to easily control characters and props in an animated environment in real time
methods: using pygame's sprite system to group, control, and render sprites as in a videogame
		using wxpython's widgets to access controls and windows to make file loading dramatically easier

custom file formats:
	script:
		rendering of all used sprites, their position, type, recorded actions(if any), and location of object file

	object file:
		detailed list of all resources and their corrisponding keys, as well as the sprite's name

UI:
##################################################################################
# File________________________________________________________________________10?#
#                    #        |       |       |       |       |        |         #
# FPS: 30            #        |       |       |       |       |        |      200#
# group: Actors      #        |       |       |       |       |        |         #
# selection: jack    #________|_______|_______|_______|_______|________|___200___#
# speed: 10          #                                                           #
# Flip H: True       #                                                           #
# Flip V: False      #                                                           #750
# Pos X: 100         #                                                           #
# Pos Y: 100         #                                                           #
# Mouse: rotate/pos  #                                                        540#
# Angle: 30 degrees  #                                                           #
# State: angry       #                                                           #
# substate: running  #                                                           #
# Mouth: Open        #                                                           #
# Recording: False   #                                                           #
# Playback: False    #                                                           #
#        300         #                            960                            #
##################################################################################
		                             1260


"""


class PuppetTheatre(wx.Frame):
	def __init__(self, parent, title, size):
		#main frame, sets up menu bar and SDL frame where the animation happens
		wx.Frame.__init__(self, parent, wx.ID_ANY, title, pos=(1,1), size=size, style= (wx.DEFAULT_FRAME_STYLE|wx.WANTS_CHARS) ^ (wx.RESIZE_BORDER|wx.MAXIMIZE_BOX) )

		#setting up the icon
		icon = wx.Icon()
		icon.CopyFromBitmap(wx.Bitmap("icon.bmp", wx.BITMAP_TYPE_ANY))
		self.SetIcon(icon)

		##########Begin menubar setup
		#menu bar contains loading and saving of script files
		menubar = wx.MenuBar()

		#file menu contains load script, save script, and close window
		#will also contain help menu at a later date
		fileMenu = wx.Menu()

		loadScript = fileMenu.Append(wx.ID_OPEN, 'Load Script', 'Load Script from File')
		saveScript = fileMenu.Append(wx.ID_SAVE, 'Save Script', 'Save Script to File')
		closeWin = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit Application')

		#adding menus to the menu bar
		menubar.Append(fileMenu, '&File')

		#adds the menu bar to the window
		self.SetMenuBar(menubar)
		#########End MenuBar setup

		############# inset useful panels here

		self.topBox = wx.BoxSizer(wx.HORIZONTAL)
		self.HUD = StatusCtrl(self, size= (300,600) )
		self.ObjCtrl = objCtrl(self, wx.ID_ANY, self.HUD)
		self.topBox.Add(self.ObjCtrl, 1)

		self.botBox = wx.BoxSizer(wx.HORIZONTAL)

		self.timer = wx.Timer(self)

		self.botBox.Add(self.HUD, 0, wx.EXPAND)

		self.gamePanel = PygamePanel(self, -1, (1140, 640), self.HUD, self.ObjCtrl)
		self.botBox.Add(self.gamePanel, 0, wx.EXPAND)

		self.mainBox = wx.BoxSizer(wx.VERTICAL)		
		self.mainBox.Add(self.topBox, 0, wx.EXPAND)
		self.mainBox.Add(self.botBox, 0, wx.EXPAND)

		self.SetSizer(self.mainBox)
		self.SetAutoLayout(1)

		############# end useful panels

		############# bindings

		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.Bind(wx.EVT_MENU, self.OnClose, closeWin)
		self.Bind(wx.EVT_MENU, self.OnLoad, loadScript)
		self.Bind(wx.EVT_MENU, self.OnSave, saveScript)
		self.Bind(wx.EVT_TIMER, self.gamePanel.Update, self.timer)

		############# end bindings


		############# Timers
		self.timer.Start(20)

		############# End Timers

	##################event methods

	def OnLoad(self, event):
		with wx.FileDialog(self, "Load Script File", wildcard="Script files (*.tscr)|*.tscr",
							style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
			if fileDialog.ShowModal() == wx.ID_CANCEL:
				return

			pathname = fileDialog.GetPath()
			print(pathname)
			try:
				with open(pathname, 'r') as file:
					print(file.read())
			except IOError:
				wx.LogError("Cannot Open file %s" % pathname)


	def OnSave(self, event):
		with wx.FileDialog(self, "Save Script File", wildcard="Script files (*.tscr)|*.tscr",
							style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
			if fileDialog.ShowModal() == wx.ID_CANCEL:
				return

			pathname = fileDialog.GetPath()

			try:
				with open(pathname, 'w') as file:
					file.write("this is a test")
			except IOError:
				wx.LogError("Cannot save current data in file %s" % pathname)

	def OnClose(self, event):
		self.gamePanel.OnClose()
		wx.Exit()
		exit()	

if __name__ == '__main__':
	app = wx.App()
	view = PuppetTheatre(parent=None, title='Finger Puppet Theatre', size=(1456, 810) )
	view.Show()
	app.MainLoop()
