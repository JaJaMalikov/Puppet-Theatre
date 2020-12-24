#graphical libraries
import wx
import pygame

from pos_state import Pos_State
from scale_state import Scale_State
from rot_state import Rot_State
#constants used throughout the program
from consts import *
#internal data structure default implementation
import data_default

loc = 447

class StateCtrl(wx.Panel):
	def __init__(self, parent, ID, data, window, listener):
		wx.Panel.__init__(self, parent, ID,style = wx.RAISED_BORDER)

		self.data = data
		self.window = window
		self.listener = listener
		self.changed = False

		self.build()
		self.set_layout()
		self.bind_all()

	def build(self):
		#start groups
		self.obj_name_panel= wx.Panel(self, size=(180,30), style=wx.RAISED_BORDER)
		self.object_name_text = wx.StaticText(self.obj_name_panel, label="Camera", pos=(60,3))

		self.mainBook = wx.Notebook(self)
		self.pos_state_page = Pos_State(self.mainBook, wx.ID_ANY, self.data, self.window, self.listener)
		self.scale_state_page = Scale_State(self.mainBook, wx.ID_ANY, self.data, self.window, self.listener)
		self.rot_state_page = Rot_State(self.mainBook, wx.ID_ANY, self.data, self.window, self.listener)

		self.mainBook.AddPage(self.pos_state_page, "Position")
		self.mainBook.AddPage(self.scale_state_page, "Scale")
		self.mainBook.AddPage(self.rot_state_page, "Rotation")

		## end groups

	def set_layout(self):
		self.full_sizer = wx.BoxSizer(wx.VERTICAL)

		self.full_sizer.Add(self.obj_name_panel)
		self.full_sizer.Add(self.mainBook)

		self.SetSizer(self.full_sizer)

	def bind_all(self):
		###bind all sliders and text boxes to events
		pass

		###end bind sliders

	def set_data(self, data):
		self.data = data
		self.pos_state_page.set_data(self.data)
		self.scale_state_page.set_data(self.data)
		self.rot_state_page.set_data(self.data)

	def create_menus(self):
		pass

	def Update(self, second):
		if second and self.changed:
			self.changed = False
			self.window.PushHistory()
		self.object_name_text.SetLabel(self.data["Current Object"])
		self.pos_state_page.Update(second)
		self.scale_state_page.Update(second)
		self.rot_state_page.Update(second)



class testFrame(wx.Frame):
	def __init__(self, parent, title, size):
		wx.Frame.__init__(self,
			parent, wx.ID_ANY, title, pos=(1,1), size=size,
			style = (wx.DEFAULT_FRAME_STYLE|wx.WANTS_CHARS|wx.FULL_REPAINT_ON_RESIZE))


		self.data = copy.deepcopy(data.data)
		self.Image_list = {}

		mainBox = wx.BoxSizer(wx.HORIZONTAL)


		self.menubar = wx.MenuBar()
		self.fileMenu = wx.Menu()

		#add elements and panels here to allow them to make changes to the window
		self.stateCtrl = StateCtrl(self, wx.ID_ANY, self.data, self)

		self.loadData = self.fileMenu.Append(wx.ID_ANY, 'Load', 'Load Animation')
		self.closeWin = self.fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit Application')

		self.menubar.Append(self.fileMenu, '&File')
		self.SetMenuBar(self.menubar)

		#####################panel list

		mainBox.Add(self.stateCtrl, 1, wx.EXPAND)
		#mainBox.Add(self.mainBook, 4, wx.EXPAND)

		self.SetSizer(mainBox)
		self.timer = wx.Timer(self)

		self.lastframe = datetime.now().second

		self.frames = 0
		#####################statusbar

		self.statusbar = self.CreateStatusBar(4)
		
		#####################bindings
		self.Bind(wx.EVT_TIMER, self.framerate, self.timer)

		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.Bind(wx.EVT_MENU, self.OnClose, self.closeWin)
		self.Bind(wx.EVT_MENU, self.LoadData, self.loadData)
		self.timer.Start()

	def framerate(self, event):
		self.stateCtrl.Update()
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

	def Set_Forth_Status(self, text):
		self.statusbar.SetStatusText( text , 3)

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
	#other built-in libraries
	import copy
	from datetime import datetime
	import json
	app = wx.App()
	view = testFrame(parent=None, title='Finger Pupper Theatre', size=(1500,700))
	view.Show()
	app.MainLoop()