# -*- coding: ascii -*-
import wx, sys, os, wx.lib.newevent, wx.stc as stc, string
from datetime import datetime
import threading, random, socket, select
from time import ctime
from sdlpanel import PygamePanel
from manager import Manager
from listener import Key_listener
from userPanels import *
from renderPanel import Renderer

class framework(wx.Frame):
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, wx.ID_ANY, title, pos=(1, 1), size=(1500, 850))

		menubar = wx.MenuBar()

		#add menu items by copying file menu and modding, no fancy stuff
		fileMenu = wx.Menu()

		importItem = fileMenu.Append(wx.ID_OPEN, 'Import image', 'Load image from file')
		loadItem = fileMenu.Append(wx.Window.NewControlId(), 'Import animation', 'Load image from file')
		fileItem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')

		#menubar.Append(loadMenu, '&load')
		menubar.Append(fileMenu, '&File')

		self.SetMenuBar(menubar)

		self.SetBackgroundColour((0, 0, 50))
		self.renderPanel = Renderer(self)
		self.sizer = wx.BoxSizer()
		self.sizer.Add(self.renderPanel, 1, wx.EXPAND)
		self.SetSizer(self.sizer)
		self.SetAutoLayout(1)
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.Bind(wx.EVT_MENU, self.OnClose, fileItem)
		self.Bind(wx.EVT_MENU, self.OnImport, importItem)
		self.Bind(wx.EVT_MENU, self.OnLoad, loadItem)
		self.Bind(wx.EVT_PAINT, self.OnPaint)

	def OnImport(self, event):
		with wx.FileDialog(self, "Import File", wildcard="PNG files (*.png)|*.png",
							style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
			if fileDialog.ShowModal() == wx.ID_CANCEL:
				return

			pathname = fileDialog.GetPath()
			#try:
			self.renderPanel.importPNG(pathname)
			#except:
			#	wx.LogError("Cannot open file '%s'." % pathname)

	def OnLoad(self, event):
		with wx.DirDialog(self, "Choose input directory", "",
							wx.DD_DEFAULT_STYLE| wx.DD_DIR_MUST_EXIST) as dirDialog:
			if dirDialog.ShowModal() == wx.ID_CANCEL:
				return

			pathname = dirDialog.GetPath()

			#try:
			self.renderPanel.importAnimation(pathname)
			#except:
			#	wx.LogError("Cannot open file '%s'." % pathname)

	def OnClose(self, event):
		self.renderPanel.OnClose()
		wx.Exit()
		exit()

	def OnPaint(self, event):
		self.renderPanel.OnPaint()

if __name__ == '__main__':
	app = wx.App()
	view = framework(parent=None, title='Finger Puppet Theatre')
	view.Show()
	app.MainLoop()
