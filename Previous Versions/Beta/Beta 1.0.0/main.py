
import wx

from datetime import datetime

from objectCtrl import objCtrl
from timelineCtrl import timelineCtrl
from renderCtrl import RenderCtrl
from stateCtrl import StateCtrl

from listener import Key_listener

import webbrowser

import json

import data
import copy

class mainFrame(wx.Frame):
	def __init__(self, parent, title, size):
		wx.Frame.__init__(self,
			parent, wx.ID_ANY, title, pos=(1,1), size=size,
			style = (wx.DEFAULT_FRAME_STYLE|wx.WANTS_CHARS))

		self.data = copy.deepcopy(data.data)

		self.Image_list = {}
		self.listener = Key_listener()
		self.pathname = ""
		self.rendering = False

		self.mainBox = wx.BoxSizer(wx.HORIZONTAL)


		self.menubar = wx.MenuBar()
		self.fileMenu = wx.Menu()

		self.newProj = wx.MenuItem(self.fileMenu, wx.ID_ANY, "&New Project\tCtrl+N", 'New Project')
		self.loadData = wx.MenuItem(self.fileMenu, wx.ID_ANY, '&Load Project\tCtrl+O', 'Load Animation')
		self.saveData = wx.MenuItem(self.fileMenu, wx.ID_ANY, '&Save Project\tCtrl+S', 'Save Animation')
		self.saveAsData = wx.MenuItem(self.fileMenu, wx.ID_ANY, '&Save Project As\tShift+Ctrl+S', 'Save Animation As')

		self.fileMenu.Append(self.newProj)
		self.fileMenu.Append(self.loadData)
		self.fileMenu.Append(self.saveData)
		self.fileMenu.Append(self.saveAsData)
		self.fileMenu.AppendSeparator()

		#add elements and panels here to allow them to make changes to the window
		self.timelineCtrl = timelineCtrl(self, wx.ID_ANY, self.data, self, (2000,50))
		self.renderCtrl = RenderCtrl(self, wx.ID_ANY, self.data, self, (1000,700), self.Image_list, self.listener)
		self.objCtrl = objCtrl(self, self.data, self, self.Image_list)
		self.stateCtrl = StateCtrl(self, wx.ID_ANY, self.data, self)

		self.closeWin = wx.MenuItem(self.fileMenu, wx.ID_EXIT, '&Quit\tCtrl+X', 'Quit Application')

		self.fileMenu.AppendSeparator()

		self.fileMenu.Append(self.closeWin)

		self.menubar.Append(self.fileMenu, '&File')

		self.renderCtrl.create_menus()

		self.helpMenu = wx.Menu()

		self.tutorial1 = wx.MenuItem(self.helpMenu, wx.ID_ANY, "&About All")
		self.tutorial2 = wx.MenuItem(self.helpMenu, wx.ID_ANY, "&About Objects")
		self.tutorial3 = wx.MenuItem(self.helpMenu, wx.ID_ANY, "&About Timeline")
		self.tutorial4 = wx.MenuItem(self.helpMenu, wx.ID_ANY, "&About Renderer")
		self.tutorial5 = wx.MenuItem(self.helpMenu, wx.ID_ANY, "&About States")
		self.tutorial6 = wx.MenuItem(self.helpMenu, wx.ID_ANY, "&About Creating Video")

		self.helpMenu.Append(self.tutorial1)
		self.helpMenu.Append(self.tutorial2)
		self.helpMenu.Append(self.tutorial3)
		self.helpMenu.Append(self.tutorial4)
		self.helpMenu.Append(self.tutorial5)
		self.helpMenu.Append(self.tutorial6)

		self.menubar.Append(self.helpMenu, "&Help")

		self.SetMenuBar(self.menubar)

		#####################panel list

		self.center = wx.BoxSizer(wx.VERTICAL)
		self.center.Add(wx.Panel(self, size=(2000,1)))
		self.center.Add(self.renderCtrl, 1, wx.EXPAND)
		self.center.Add(self.timelineCtrl, 0, wx.EXPAND)

		self.mainBox.Add(self.objCtrl, 0, wx.EXPAND)
		self.mainBox.Add(self.center, 1, wx.EXPAND)
		self.mainBox.Add(self.stateCtrl, 0, wx.EXPAND)

		self.SetSizer(self.mainBox)
		self.timer = wx.Timer(self)

		self.lastframe = datetime.now().second

		self.frames = 0

		#####################statusbar
		self.statusbar = self.CreateStatusBar(5)
		
		#####################bindings
		self.Bind(wx.EVT_TIMER, self.framerate, self.timer)

		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.Bind(wx.EVT_MENU, self.OnClose, self.closeWin)
		self.Bind(wx.EVT_MENU, self.LoadData, self.loadData)
		self.Bind(wx.EVT_MENU, self.SaveData, self.saveData)
		self.Bind(wx.EVT_MENU, self.SaveAsData, self.saveAsData)

		self.Bind(wx.EVT_MENU, self.On_tutorial1, self.tutorial1)
		self.Bind(wx.EVT_MENU, self.On_tutorial2, self.tutorial2)
		self.Bind(wx.EVT_MENU, self.On_tutorial3, self.tutorial3)
		self.Bind(wx.EVT_MENU, self.On_tutorial4, self.tutorial4)
		self.Bind(wx.EVT_MENU, self.On_tutorial5, self.tutorial5)
		self.Bind(wx.EVT_MENU, self.On_tutorial6, self.tutorial6)

		self.timer.Start()
		self.Maximize(True)

	def On_tutorial1(self, event):
		webbrowser.open("https://www.youtube.com/watch?v=oBAQy1D5r7o&list=PLkVdGBkhsW-WdYoTn-Uf8SouWUh3vGnGO&index=1")

	def On_tutorial2(self, event):
		webbrowser.open("https://www.youtube.com/watch?v=5L98weJKd48&list=PLkVdGBkhsW-WdYoTn-Uf8SouWUh3vGnGO&index=2")

	def On_tutorial3(self, event):
		webbrowser.open("https://www.youtube.com/watch?v=Sm7fqqMC0Ks&list=PLkVdGBkhsW-WdYoTn-Uf8SouWUh3vGnGO&index=3")

	def On_tutorial4(self, event):
		webbrowser.open("https://www.youtube.com/watch?v=ar9PjawB-qs&list=PLkVdGBkhsW-WdYoTn-Uf8SouWUh3vGnGO&index=4")

	def On_tutorial5(self, event):
		webbrowser.open("https://www.youtube.com/watch?v=rqVycueA8Tg&list=PLkVdGBkhsW-WdYoTn-Uf8SouWUh3vGnGO&index=5")

	def On_tutorial6(self, event):
		webbrowser.open("https://www.youtube.com/watch?v=15ymfD67Qbk&list=PLkVdGBkhsW-WdYoTn-Uf8SouWUh3vGnGO&index=6")

	def framerate(self, event):
		current_time = (datetime.now()-datetime(1970,1,1)).total_seconds()
		if (current_time - self.lastframe) >= 1:
			self.Set_Third_Status(str(self.frames) )
			self.lastframe = current_time
			self.frames = 0
			print(current_time)
			self.timelineCtrl.Update(True)
			self.renderCtrl.Update(True)
			self.stateCtrl.Update(True)

		else:
			self.frames += 1
			self.timelineCtrl.Update(False)
			self.renderCtrl.Update(False)
			self.stateCtrl.Update(False)


	def Set_First_Status(self, text):
		self.statusbar.SetStatusText( text , 0)

	def Set_Second_Status(self, text):
		self.statusbar.SetStatusText( text , 1)

	def Set_Third_Status(self, text):
		self.statusbar.SetStatusText( text , 2)

	def Set_Forth_Status(self, text):
		self.statusbar.SetStatusText( text , 3)

	def Set_Fifth_Status(self, text):
		self.statusbar.SetStatusText( text , 4)

	def LoadData(self, event):
		with wx.FileDialog(self, "Load Animation", wildcard="ANI files (*.ani)|*.ani",
							style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
			if fileDialog.ShowModal() == wx.ID_CANCEL:
				return

			pathname = fileDialog.GetPath()

			tempData = open(pathname, "r")
			self.data = json.loads(tempData.read())
			tempData.close()
			self.set_data()
			self.timelineCtrl.setAudio(self.data["audio"])
			self.objCtrl.reload()
			self.objCtrl.LoadStatus()
			self.pathname = pathname
			self.SetTitle("Monchy Puppet Theatre Beta 1.0.0(" + self.pathname.split("\\")[-1].split(".")[0] + ")")

	def set_data(self):
		self.timelineCtrl.set_data(self.data)
		self.objCtrl.set_data(self.data)
		self.renderCtrl.set_data(self.data)
		self.stateCtrl.set_data(self.data)


	def SaveAsData(self, event):
		with wx.FileDialog(self, "Save animation", wildcard="ANI files (*.ani)|*.ani",
			style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

			if fileDialog.ShowModal() == wx.ID_CANCEL:
				return

			pathname = fileDialog.GetPath()
			self.writeData(pathname)

	def SaveData(self, event):
		if self.pathname != "":
			self.writeData(self.pathname)			
		else:
			self.SaveAsData(event)

	def writeData(self, pathname):
		try:
			with open(pathname, 'w') as file:
				file.write(json.dumps(self.data))
		except IOError:
			wx.LogError("Cannot save current data in file %s" % pathname)
		self.pathname = pathname
		self.SetTitle("Monchy Puppet Theatre Beta 1.0.0(" + self.pathname.split("\\")[-1].split(".")[0] + ")")


	def OnClose(self, event):
		wx.Exit()
		exit()

if __name__ == '__main__':
	app = wx.App()
	view = mainFrame(parent=None, title='Monchy Puppet Theatre Beta 1.0.0', size=(1600,1000))
	view.Show()
	app.MainLoop()