# -*- coding: ascii -*-
import wx, sys, os, wx.lib.newevent, wx.stc as stc, string
from datetime import datetime
import threading, random, socket, select
from time import ctime
from sdlpanel import PygamePanel
from manager import Manager
from listener import Key_listener
from userPanels import *

class Renderer(wx.Panel):

	def __init__(self, *args, **kwargs):
		wx.Panel.__init__(self, *args, **kwargs)

		self.SetBackgroundColour((0, 0, 50))
		#menu and status bars

		#user interface components
		self.text2 = SyntaxControl(self)
		self.text3 = SyntaxControl(self)
		self.text4 = SyntaxControl(self)

		#selection buttons
		pic = wx.Bitmap("defport.png", wx.BITMAP_TYPE_ANY)

		self.buttons = []
		for x in range(10):
			self.buttons.append(wx.BitmapButton(self, -1, pic))

		self.gamePanel = PygamePanel(self, -1, (1152,648), "animator")#SyentaxControl(self)
		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.gamePanel.update, self.timer)
		self.timer.Start(20)

		#sorting of user interface
		self.mainbox = wx.BoxSizer(wx.VERTICAL)

		self.selection = wx.BoxSizer(wx.HORIZONTAL)

		for x in range(10):
			self.selection.Add(self.buttons[x],0)

		self.mainbox.Add(self.selection, 0, wx.EXPAND)

		self.mainpanel = wx.BoxSizer(wx.HORIZONTAL)

		self.stats = wx.BoxSizer(wx.VERTICAL)
		self.stats.Add(self.text2,1, wx.EXPAND)
		self.mainpanel.Add(self.stats, 1, wx.EXPAND)

		self.gamePanels = wx.BoxSizer(wx.VERTICAL)
		self.viewport = wx.BoxSizer(wx.HORIZONTAL)
		self.viewport.Add(self.gamePanel, 0)
		self.capHold = wx.BoxSizer(wx.VERTICAL)
		self.capHold.Add(self.text3,1, wx.EXPAND)
		self.gamePanels.Add(self.viewport, 0)
		self.gamePanels.Add(self.capHold, 1, wx.EXPAND)
		self.mainpanel.Add(self.gamePanels, 3, wx.EXPAND)

		self.vars = wx.BoxSizer(wx.VERTICAL)
		self.vars.Add(self.text4,1, wx.EXPAND)
		self.mainpanel.Add(self.vars, 1, wx.EXPAND)

		self.mainbox.Add(self.mainpanel, 5, wx.EXPAND)

		self.SetSizer(self.mainbox)
		self.SetAutoLayout(1)

		for x in range(10):
			self.Bind(wx.EVT_BUTTON, self.loadObject, self.buttons[x])

	def loadObject(self, event):
		with wx.DirDialog(self, "Choose input directory", "",
							wx.DD_DEFAULT_STYLE| wx.DD_DIR_MUST_EXIST) as dirDialog:
			if dirDialog.ShowModal() == wx.ID_CANCEL:
				return

			pathname = dirDialog.GetPath()

			#try:
			print(event.GetId())
			self.gamePanel.importObject(pathname,event.GetId())
			event.GetEventObject().SetBitmap(wx.Bitmap(pathname + "/portrait.png", wx.BITMAP_TYPE_ANY))
			#except:
			#	wx.LogError("Cannot open file '%s'." % pathname)

	def importPNG(self, name):
		#try:
		self.gamePanel.importPNG(name)
		#except IOError:
		#	raise 

	def importAnimation(self, name):
		#try:
		self.gamePanel.importAnimation(name)
		#except IOError:
		#	raise 

	def OnClose(self):
		self.gamePanel.OnClose()

	def OnPaint(self):
		self.gamePanel.resize()