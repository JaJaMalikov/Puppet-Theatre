#graphical Libraries
import wx

#built-in libraries
from datetime import datetime
import webbrowser
import json
import copy
import sys

#Control panels
from object_ctrl import objCtrl
from timeline_ctrl import TimelineCtrl
from render_ctrl import RenderCtrl
from state_ctrl import StateCtrl

from listener import Key_listener

#internal data structure default implementation
import data_default

"""
Main window of the program
loads and organizes the control panels


"""

"""

outline images when empty/blank
create 'blank' 
sequence generator/macro creator
non-linear interpolations for inbetweens w/selector
drawing shapes on images


"""

version_name = "Monchy Puppet Theatre Beta 1.8.5"

class MainFrame(wx.Frame):
	def __init__(self, parent, title, size):
		wx.Frame.__init__(self,
			parent, wx.ID_ANY, title, pos=(1,1), size=size,
			style = (wx.DEFAULT_FRAME_STYLE|wx.WANTS_CHARS))

		self.listener = Key_listener()

		#sets all data to default position for a new project
		self.new_project(True)

		#setting up layout
		self.mainBox = wx.BoxSizer(wx.HORIZONTAL)

		#add elements and panels here to allow them to make changes to the window
		self.timelineCtrl = TimelineCtrl(self, wx.ID_ANY, self.data, self, self.listener)
		self.renderCtrl = RenderCtrl(self, wx.ID_ANY, self.data, self, (1000,700), self.Image_list, self.listener)
		self.objCtrl = objCtrl(self, self.data, self, self.Image_list, self.listener)
		self.stateCtrl = StateCtrl(self, wx.ID_ANY, self.data, self, self.listener)
		#creates menus and tells all control panels to set their menus as well
		self.create_menus()

		self.set_layout()

		self.timer = wx.Timer(self)

		#sets the time the last tick took place
		#tickspeed is useful in determining if the program is running at full speed
		self.lasttick = datetime.now().second

		#####################statusbar
		self.statusbar = self.CreateStatusBar(5)
		
		#####################bindings
		self.bind_all()
		self.timer.Start()
		self.Maximize(True)

		self.helpDict = {
		"&About All":"https://www.youtube.com/watch?v=oBAQy1D5r7o&list=PLkVdGBkhsW-WdYoTn-Uf8SouWUh3vGnGO&index=1",
		"&About Objects":"https://www.youtube.com/watch?v=5L98weJKd48&list=PLkVdGBkhsW-WdYoTn-Uf8SouWUh3vGnGO&index=2",
		"&About Timeline":"https://www.youtube.com/watch?v=Sm7fqqMC0Ks&list=PLkVdGBkhsW-WdYoTn-Uf8SouWUh3vGnGO&index=3",
		"&About Renderer":"https://www.youtube.com/watch?v=ar9PjawB-qs&list=PLkVdGBkhsW-WdYoTn-Uf8SouWUh3vGnGO&index=4",
		"&About States":"https://www.youtube.com/watch?v=rqVycueA8Tg&list=PLkVdGBkhsW-WdYoTn-Uf8SouWUh3vGnGO&index=5",
		"&About Creating Video":"https://www.youtube.com/watch?v=15ymfD67Qbk&list=PLkVdGBkhsW-WdYoTn-Uf8SouWUh3vGnGO&index=6"
		}

	def set_layout(self):
		#organizes layout
		"""
		===================
		| |             | |
		|1|     2       |3|
		| |_____________| |
		|_|______4______|_|

		1- objCtrl
		2- renderCtrl
		3- stateCtrl
		4- timelineCtrl

		"""
		self.center = wx.BoxSizer(wx.VERTICAL)
		self.center.Add(wx.Panel(self, size=(2000,1)))
		self.center.Add(self.renderCtrl, 1, wx.EXPAND)   #2
		self.center.Add(self.timelineCtrl, 0, wx.EXPAND) #4

		self.mainBox.Add(self.objCtrl, 0, wx.EXPAND)     #2
		self.mainBox.Add(self.center, 1, wx.EXPAND)      #2, 4
		self.mainBox.Add(self.stateCtrl, 0, wx.EXPAND)   #3

		self.SetSizer(self.mainBox)

	def bind_all(self):
		self.Bind(wx.EVT_TIMER, self.tickrate, self.timer)
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.Bind(wx.EVT_MENU, self.OnNew, self.newProj)
		self.Bind(wx.EVT_MENU, self.OnClose, self.closeWin)
		self.Bind(wx.EVT_MENU, self.LoadData, self.loadData)
		self.Bind(wx.EVT_MENU, self.SaveData, self.saveData)
		self.Bind(wx.EVT_MENU, self.SaveAsData, self.saveAsData)

		self.Bind(wx.EVT_MENU, self.UndoHistory, self.undoItem)
		self.Bind(wx.EVT_MENU, self.RedoHistory, self.redoItem)

		self.Bind(wx.EVT_MENU, self.On_tutorial, self.tutorial1)
		self.Bind(wx.EVT_MENU, self.On_tutorial, self.tutorial2)
		self.Bind(wx.EVT_MENU, self.On_tutorial, self.tutorial3)
		self.Bind(wx.EVT_MENU, self.On_tutorial, self.tutorial4)
		self.Bind(wx.EVT_MENU, self.On_tutorial, self.tutorial5)
		self.Bind(wx.EVT_MENU, self.On_tutorial, self.tutorial6)


	def create_menus(self):
		self.menubar = wx.MenuBar()
		self.fileMenu = wx.Menu()
		#creates the menu items for saving/loading the current project
		self.newProj = wx.MenuItem(self.fileMenu, wx.ID_ANY, "&New Project\tCtrl+N", 'New Project')
		self.loadData = wx.MenuItem(self.fileMenu, wx.ID_ANY, '&Load Project\tCtrl+O', 'Load Animation')
		self.saveData = wx.MenuItem(self.fileMenu, wx.ID_ANY, '&Save Project\tCtrl+S', 'Save Animation')
		self.saveAsData = wx.MenuItem(self.fileMenu, wx.ID_ANY, '&Save Project As\tShift+Ctrl+S', 'Save Animation As')

		self.fileMenu.Append(self.newProj)
		self.fileMenu.Append(self.loadData)
		self.fileMenu.Append(self.saveData)
		self.fileMenu.Append(self.saveAsData)
		self.fileMenu.AppendSeparator()

		self.menubar.Append(self.fileMenu, '&File')

		self.editMenu = wx.Menu()

		self.undoItem = wx.MenuItem(self.editMenu, wx.ID_ANY, "&Undo\tCtrl+Z", "Undo Action")
		self.redoItem = wx.MenuItem(self.editMenu, wx.ID_ANY, "&Redo\tCtrl+Y", "Redo Action")

		self.editMenu.Append(self.undoItem)
		self.editMenu.Append(self.redoItem)

		self.menubar.Append(self.editMenu, "&Edit")

		#creates each control panel's menus in order
		#the order these are called determines how the menus are laid out
		self.timelineCtrl.create_menus()
		self.renderCtrl.create_menus()
		self.objCtrl.create_menus()
		self.stateCtrl.create_menus()

		self.closeWin = wx.MenuItem(self.fileMenu, wx.ID_EXIT, '&Quit\tCtrl+X', 'Quit Application')

		self.fileMenu.AppendSeparator()

		self.fileMenu.Append(self.closeWin)



		#help menu links back to youtube tutorials on how to use the program
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


		#opens to a playlist on youtube containing the tutorials for use
		#could probably be turned into a single function
	def On_tutorial(self, event):
		helplink = self.GetMenuBar().FindItemById(event.GetId()).GetItemLabel()
		webbrowser.open(self.helpDict[helplink])


	def tickrate(self, event):

		"""
		Controls the tickrate of the software
		allows it to run at max speed, capped by the vsync rate
		every second it sets the current tickrate to monitor the proccessing speed of the program
		sends True signal to the control panels update function once per second
		current time is time since Jan 1, 1970
		"""
		current_time = (datetime.now()-datetime(1970,1,1)).total_seconds()
		if (current_time - self.lasttick) >= 1:
			self.Set_Third_Status(str(self.ticks) )
			self.lasttick = current_time
			self.ticks = 0
			self.timelineCtrl.Update(True)
			self.renderCtrl.Update(True)
			self.stateCtrl.Update(True)
			self.objCtrl.Update(True)

		else:
			self.ticks += 1
			self.timelineCtrl.Update(False)
			self.renderCtrl.Update(False)
			self.stateCtrl.Update(False)
			self.objCtrl.Update(False)
		self.listener.clear_struck()

		#statusbar set functions, to be compressed into single function "Set_Status"
	def Set_First_Status(self, text):
		self.Set_Status(0, text)

	def Set_Second_Status(self, text):
		self.Set_Status(1, text)

	def Set_Third_Status(self, text):
		self.Set_Status(2, text)

	def Set_Forth_Status(self, text):
		self.Set_Status(3, text)

	def Set_Fifth_Status(self, text):
		self.Set_Status(4, text)

	def Set_Status(self, bar, text):
		self.statusbar.SetStatusText( text, bar)

	def LoadData(self, event):
		"""
		self.data is loaded from a json file named *.ani (short for animate)
		load data selects a file with a file dialog and loads it as self.data
		then it calls self.set_data(), which loads all the images, audio, and settings from the file
		title of the animation is added to the window title

		OnNew offers to save the current project if anything has been added
		after it calls new_project to wipe everything clean
		"""

		if self.savedIndex != self.historyIndex:
			box = wx.MessageDialog(None, 'Would you like to save the current project?',
				"Unsaved work", wx.OK | wx.CANCEL | wx.ICON_WARNING)
			if box.ShowModal() == wx.ID_OK:
				self.SaveData(1)

		with wx.FileDialog(self, "Load Animation", wildcard="ANI files (*.ani)|*.ani",
							style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
			if fileDialog.ShowModal() == wx.ID_CANCEL:
				return

			pathname = fileDialog.GetPath()
			tempData = open(pathname, "r")
			self.data = json.loads(tempData.read())
			tempData.close()
			self.set_data()

			if self.data["Audio"] != "":
				self.timelineCtrl.setAudio(self.data["Audio"])

			self.objCtrl.reload(True)
			self.objCtrl.LoadStatus()
			self.pathname = pathname
			self.SetTitle(("%s (%s)" % (version_name,  self.pathname.split("\\")[-1].split(".")[0])) )
			self.ResetHistory()

	def OnNew(self, event):
		if len(self.data["Object List"]) > 1 or self.data["Audio"] != "":
			self.SaveAsData(1)
		self.new_project(False)
		self.timelineCtrl.setAudio(self.data["Audio"])
		self.objCtrl.reload(False)
		self.objCtrl.LoadStatus()

	def ResetHistory(self):
		self.editHistory = []
		self.historyIndex = 0
		self.savedIndex = 0
		self.editHistory.append(copy.deepcopy(self.data))

		"""
		hist_back = [self.data["Current Object"], []]
		print(hist_back)
		for frame in self.data["Frames"]:
			hist_back[1].append(copy.deepcopy(frame[self.data["Current Object"]]))

		print(hist_back)
		self.editHistory.append(hist_back )
		print(len(self.editHistory))
		print(self.historyIndex)"""

	def PushHistory(self):
		pass
		#if self.historyIndex < (len(self.editHistory) - 1):
		#	print("truncated history")
		#	self.editHistory = self.editHistory[:self.historyIndex+1]
		#self.editHistory.append(copy.deepcopy(self.data))
		#self.historyIndex += 1
		#if len(self.editHistory) > 50:
		#	self.editHistory.pop(0)
		#	self.historyIndex = (len(self.editHistory) - 1)
		#print(len(self.editHistory))
		#print(self.historyIndex)

		"""		
		print("hello?")
		if self.historyIndex < (len(self.editHistory) - 1):
			print("truncated history")
			self.editHistory = self.editHistory[:self.historyIndex+1]

		hist_back = [self.data["Current Object"], []]
		print(hist_back)
		for frame in self.data["Frames"]:
			hist_back[1].append(copy.deepcopy(frame[self.data["Current Object"]]))

		print(hist_back)
		self.editHistory.append(hist_back )

		print(hist_back)

		self.historyIndex += 1
		if len(self.editHistory) > 150:
			self.editHistory.pop(0)
			self.historyIndex = (len(self.editHistory) - 1)
		print(len(self.editHistory))
		print(self.historyIndex)
		print(self.editHistory)"""

	def UndoHistory(self, event):
		print("undoing")
		self.historyIndex -= 1
		if self.historyIndex < 0:
			self.historyIndex = 0
		else:
			self.data = copy.deepcopy(self.editHistory[self.historyIndex])
			print(len(self.editHistory))
			print(self.historyIndex)
			#for key in self.editHistory[self.historyIndex].keys():
			self.set_data()
			#	#self.data[key] = copy.deepcopy(self.editHistory[self.historyIndex][key])
			print("data loaded")
			self.objCtrl.reload(False)
			self.objCtrl.LoadStatus()
		"""
		print("undoing")
		self.historyIndex -= 1
		if self.historyIndex < 0:
			self.historyIndex = 0
		else:
			#self.data = copy.deepcopy(self.editHistory[self.historyIndex])

			for frame in range(len(self.data["Frames"])):
				print(frame)
				self.data["Frames"][frame][ self.editHistory[self.historyIndex][0] ] = copy.deepcopy(self.editHistory[self.historyIndex][1][frame])

			print(len(self.editHistory))
			print(self.historyIndex)
			#for key in self.editHistory[self.historyIndex].keys():
			self.set_data()
			#	#self.data[key] = copy.deepcopy(self.editHistory[self.historyIndex][key])
			print("data loaded")
			self.objCtrl.reload(False)
			self.objCtrl.LoadStatus()"""

	def RedoHistory(self, event):
		print("redoing")
		self.historyIndex += 1
		if self.historyIndex >= len(self.editHistory):
			self.historyIndex -= 1
		else:
			self.data = copy.deepcopy(self.editHistory[self.historyIndex])
		print(len(self.editHistory))
		print(self.historyIndex)
		self.set_data()
		self.objCtrl.reload(False)
		self.objCtrl.LoadStatus()
		"""
		print("redoing")
		self.historyIndex += 1
		if historyIndex >= len(self.editHistory):
			self.historyIndex -= 1
		else:

			#self.data = copy.deepcopy(self.editHistory[self.historyIndex])
			for frame in range(len(self.data["Frames"])):
				self.data["Frames"][frame][ self.editHistory[self.historyIndex][0] ] = copy.deepcopy(self.editHistory[self.historyIndex][1][frame])


		print(len(self.editHistory))
		print(self.historyIndex)
		self.set_data()
		self.objCtrl.reload(False)
		self.objCtrl.LoadStatus()"""

	def new_project(self, startup):
		#sets the animation state data into default, for more details see data_default.py
		self.data = copy.deepcopy(data_default.data)
		self.savedIndex = 0
		self.ResetHistory()

		#dict, holds all images as opengl textures "image name":obj2d
		self.Image_list = {}
		#holds current file path to save and load the animation
		self.pathname = ""
		#signals to certain functions that the video is being rendered to disable audio syncing
		self.rendering = False
		self.ticks = 0
		#clears the project name
		self.SetTitle(version_name)
		#try:
		if not startup:
			self.set_data()
		#except:
		#	pass

	def set_data(self):
		#calls every control panel to load the new data
		self.objCtrl.set_data(self.data)
		self.renderCtrl.set_data(self.data)
		self.stateCtrl.set_data(self.data)
		self.timelineCtrl.set_data(self.data)

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
		self.SetTitle(("%s (%s)" % (version_name,  self.pathname.split("\\")[-1].split(".")[0])))
		self.savedIndex = self.historyIndex

	def OnClose(self, event):
		#add "would you like to save"
		if self.savedIndex != self.historyIndex:
			box = wx.MessageDialog(None, 'Would you like to save the current project?',
				"Unsaved work", wx.OK | wx.CANCEL | wx.ICON_WARNING)
			if box.ShowModal() == wx.ID_OK:
				self.SaveData(1)
		self.timer.Stop()
		self.timelineCtrl.OnClose()
		wx.Exit()
		sys.exit()

if __name__ == '__main__':
	app = wx.App()
	view = MainFrame(parent=None, title=version_name, size=(1600,1000))
	view.Show()
	app.MainLoop()