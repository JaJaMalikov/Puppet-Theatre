#graphical libraries
import wx

#other built in libraries
import copy
from datetime import datetime
import json

#vertex default values
import verts

#2D object class to hold the image
from OBJ2D import OBJ2D

#object list panel, holds a visual list of object
#as well as creating and deleting objects
from object_list import ObjectList

#holds list of images from current object
#also alows moving, deleting, and loading
from image_list import ImageList

#internal data structure default implementation
import data_default

from listener import Key_listener

loc = 387

version_name = "Monchy PT Object Control Panel Beta 1.0.1"

class objCtrl(wx.Panel):
	"""
	A container class for the object list and image list
	allows for per-frame control over currently selected objects
	and their currently available images
	"""
	def __init__(self, parent, data, window, Image_list):
		wx.Panel.__init__(self, parent,style = wx.RAISED_BORDER)
		self.data = data
		self.window = window
		self.Image_list = Image_list

		self.build()
		self.set_layout()
		self.bind_all()

	def bind_all(self):
		self.objList.Bind(wx.EVT_LISTBOX, self.SwitchObject)
		self.imgList.Bind(wx.EVT_LISTBOX, self.SwitchImage)

	def build(self):
		#contains both panels in a tab-based notebook for better organization
		self.mainBook = wx.Notebook(self)
		self.objList = ObjectList(self.mainBook, wx.ID_ANY, self.data, self.window, self)
		self.imgList = ImageList(self.mainBook, wx.ID_ANY, self.data, self.window, self, self.Image_list)

		self.mainBook.AddPage(self.objList , "Objects" )
		self.mainBook.AddPage(self.imgList , "Images" )

	def set_layout(self):
		mainBox = wx.BoxSizer(wx.HORIZONTAL)
		mainBox.Add(self.mainBook, 4, wx.EXPAND)
		self.SetSizer(mainBox)

	def create_menus(self):
		self.imgList.create_menus()
		self.objList.create_menus()

	def Update(self, second):
		pass

	def set_data(self, data):
		#loads data to load new or old projects
		self.data = data
		self.objList.set_data(self.data)
		self.imgList.set_data(self.data)

	def reload(self):
		#reloads all available images and objects
		self.objList.reload()
		self.imgList.reload()

	def SwitchImage(self, event):
		#changes the current image to selected image, should be moved to image list object
		self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Current Image"] = self.imgList.get_selection()
		self.LoadStatus()

	def SwitchObject(self, event):
		#changes object to currently selected object, should be in object list
		#also resets list to curren object
		#set_current_list should likely be called on update function
		self.data["Current Object"] = self.objList.get_string()
		self.imgList.set_current_list()

		self.LoadStatus()

	def LoadStatus(self):

		#sets status to indicate current object and image for confirmation of switching
		self.window.Set_First_Status(self.data["Current Object"])
		self.window.Set_Second_Status(self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Current Image"])

	def update_object(self):
		#only updates the current object
		#why do I have this?
		self.window.Set_First_Status(self.data["Current Object"])



class testFrame(wx.Frame):
	def __init__(self, parent, title, size):
		wx.Frame.__init__(self,
			parent, wx.ID_ANY, title, pos=(1,1), size=size,
			style = (wx.DEFAULT_FRAME_STYLE|wx.WANTS_CHARS))

		self.listener = Key_listener()

		#sets all data to default position for a new project
		self.new_project()

		#setting up layout
		self.mainBox = wx.BoxSizer(wx.HORIZONTAL)

		#add elements and panels here to allow them to make changes to the window
		self.objCtrl = objCtrl(self, self.data, self, self.Image_list)

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

		self.mainBox.Add(self.objCtrl, 0, wx.EXPAND)     #2

		self.SetSizer(self.mainBox)

	def bind_all(self):
		self.Bind(wx.EVT_TIMER, self.tickrate, self.timer)
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.Bind(wx.EVT_MENU, self.OnNew, self.newProj)
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

		self.closeWin = wx.MenuItem(self.fileMenu, wx.ID_EXIT, '&Quit\tCtrl+X', 'Quit Application')

		self.fileMenu.AppendSeparator()


		#creates each control panel's menus in order
		#the order these are called determines how the menus are laid out
		self.objCtrl.create_menus()

		#### end panel created menu items

		self.fileMenu.Append(self.closeWin)

		self.menubar.Append(self.fileMenu, '&File')

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

		else:
			self.ticks += 1

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
		with wx.FileDialog(self, "Load Animation", wildcard="ANI files (*.ani)|*.ani",
							style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
			if fileDialog.ShowModal() == wx.ID_CANCEL:
				return

			pathname = fileDialog.GetPath()
			tempData = open(pathname, "r")
			self.data = json.loads(tempData.read())
			tempData.close()
			self.set_data()
			self.objCtrl.reload()
			self.objCtrl.LoadStatus()
			self.pathname = pathname
			self.SetTitle("%s (%s)".format(version_name,  self.pathname.split("\\")[-1].split(".")[0]))

	def OnNew(self):
		if len(self.data["Object List"]) > 1 or self.data["Audio"] != "":
			self.SaveAsData(1)
		self.new_project()

	def new_project(self):
		#sets the animation state data into default, for more details see data_default.py
		self.data = copy.deepcopy(data_default.data)

		#dict, holds all images as opengl textures "image name":obj2d
		self.Image_list = {}
		#holds current file path to save and load the animation
		self.pathname = ""
		#signals to certain functions that the video is being rendered to disable audio syncing
		self.rendering = False
		self.ticks = 0
		#clears the project name
		self.SetTitle(version_name)
		try:
			self.set_data()
		except:
			pass

	def set_data(self):
		#calls every control panel to load the new data
		self.objCtrl.set_data(self.data)

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
		self.SetTitle("%s (%s)".format(version_name,  self.pathname.split("\\")[-1].split(".")[0]))

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