#Graphical Libraries
import wx

#Other Build in Libraries
import copy
import json

#vertex default values
import verts

#internal data structure default implementation
import data_default

#container class for 2D object texture
from OBJ2D import OBJ2D

class ParentMenu(wx.Menu):
	def __init__(self, parent, data):
		super(ParentMenu, self).__init__()

		self.parent = parent
		self.data = data

		mmi = wx.MenuItem(self, wx.NewId(), 'Set Parent')
		self.Append(mmi)
		self.Bind(wx.EVT_MENU, self.OnMakeParent, mmi)

	def OnMakeParent(self, event):
		keylist = list(self.data["Object List"].keys())
		#for key in keylist:
		#	if self.data["Object List"][key]["Parent"] != None:
		#		keylist.remove(key)
		self.dlg = wx.SingleChoiceDialog(None, "Which", "title", keylist, wx.CHOICEDLG_STYLE)
		if self.dlg.ShowModal() == wx.ID_OK:
			objname = self.dlg.GetStringSelection()

			if objname == self.data["Current Object"]:
				if objname not in self.data["Parents"]:
					self.data["Parents"].append(objname)
					for obj in self.data["Object List"]:
						if objname in self.data["Object List"][obj]["Children"]:
							self.data["Object List"][obj]["Children"].remove(objname)
			else:
				self.data["Object List"][self.data["Current Object"]]["Parent"] = objname
				self.data["Object List"][objname]["Children"].append(self.data["Current Object"])
				self.data["Parents"].remove( self.data["Current Object"])

		self.dlg.Destroy()

class ObjectList(wx.Panel):
	"""
	a basic list of object, creates and deletes them
	future update should create a menu specially for objects
	with all functions bound to the menu items
	thus allowing keyboard shortcuts to work
	"""
	def __init__(self, parent, ID, data, window, frame):
		wx.Panel.__init__(self, parent, ID)
		self.data = data
		self.window = window
		self.frame = frame
		self.Image_list = self.window.Image_list

		self.temp_data = {"Object List":{}, "Image List":[], "frame data":{}}

		self.build()
		self.set_layout()
		self.bind_all()

		#sets the displayed list of objects according to what's in self.data
		self.objList.Set(list(self.data["Object List"].keys()) )

	def create_menus(self):
		self.objMenu = wx.Menu()

		self.newObj = self.objMenu.Append(wx.ID_ANY, "&New Object\tCtrl+L", "New Object")
		self.delObj = self.objMenu.Append(wx.ID_ANY, "&Delete Object\tCtrl+U", "Delete Object")

		self.window.Bind(wx.EVT_MENU, self.CreateNewObject, self.newObj)
		self.window.Bind(wx.EVT_MENU,  self.DeleteObject, self.delObj)

		self.window.menubar.Append(self.objMenu, "&Objects")

	def bind_all(self):
		self.btn1.Bind(wx.EVT_BUTTON, self.CreateNewObject)
		self.btn2.Bind(wx.EVT_BUTTON, self.DeleteObject)
		self.btn3.Bind(wx.EVT_BUTTON, self.SaveObject)
		self.btn4.Bind(wx.EVT_BUTTON, self.LoadObject)
		self.btn5.Bind(wx.EVT_BUTTON, self.copyObject)
		self.objList.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)

	def add_saved_object(self, obj):
		self.temp_data["frame data"][obj] = copy.deepcopy(self.data["Frames"][self.data["Current Frame"]][obj])
		self.temp_data["Object List"][obj] = copy.deepcopy( self.data["Object List"][obj] )
		self.temp_data["frame data"][obj]["Keyframes"] = []
		for image in self.data["Object List"][obj]["Images"]:
			if image != "none":
				for img in self.data["Image List"]:
					if img.endswith(image):
						self.temp_data["Image List"].append( img )

		for x in self.data["Object List"][obj]["Children"]:
			self.add_saved_object(x)

	def SaveObject(self, event):
		self.add_saved_object(self.data["Current Object"])

		with wx.FileDialog(self, "Save Composite Object", wildcard="COB files (*.cob)|*.cob",
			style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

			if fileDialog.ShowModal() == wx.ID_CANCEL:
				return

			pathname = fileDialog.GetPath()
			self.writeData(pathname, self.temp_data)

		self.temp_data = {"Object List":{}, "Image List":[], "frame data":{}}

	def writeData(self, pathname, data):
		try:
			with open(pathname, 'w') as file:
				file.write(json.dumps(data))
		except IOError:
			wx.LogError("Cannot save current data in file %s" % pathname)

	def OnRightDown(self, event):
		self.PopupMenu(ParentMenu(self, self.data), event.GetPosition())

	def set_layout(self):
		self.buttonSizer = wx.BoxSizer(wx.VERTICAL)
		self.pageSizer = wx.BoxSizer(wx.VERTICAL)

		self.t_b_sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.b_b_sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.l_b_sizer = wx.BoxSizer(wx.HORIZONTAL)

		self.t_b_sizer.Add(self.btn1)
		self.t_b_sizer.Add(self.btn2)

		self.b_b_sizer.Add(self.btn3)
		self.b_b_sizer.Add(self.btn4)

		self.l_b_sizer.Add(self.btn5)

		self.buttonSizer.Add(self.t_b_sizer)
		self.buttonSizer.Add(self.b_b_sizer)
		self.buttonSizer.Add(self.l_b_sizer)
		self.pageSizer.Add(self.buttonSizer, 0)

		self.pageSizer.Add(self.objList, -1, wx.EXPAND)

		self.SetSizer(self.pageSizer)

	def build(self):
		self.btn1 = wx.Button(self, 1, "New")
		self.btn2 = wx.Button(self, 1, "Delete")
		self.btn3 = wx.Button(self, 1, "Save")
		self.btn4 = wx.Button(self, 1, "Load")
		self.btn5 = wx.Button(self, 1, "Copy")

		self.objList = wx.ListBox(self, wx.ID_ANY)

	def set_data(self, data):
		self.data = data

	def reload(self):
		self.objList.Set(list(self.data["Object List"].keys()) )

	def DeleteObject(self, event):
		self.window.PushHistory()

		#should be bound to a menu item one day with an "are you sure" box attached
		if self.data["Current Object"] != "Camera":
			box = wx.MessageDialog(None, 'Are you sure you want to delete %s' % self.data["Current Object"],
				"Delete Object", wx.OK | wx.CANCEL | wx.ICON_WARNING)
			if box.ShowModal() == wx.ID_OK:

				self.window.Set_Third_Status(self.data["Current Object"] + " deleted")

				self.remove_object(self.data["Current Object"])

				self.data["Current Object"] = list(self.data["Object List"].keys())[0]
				self.objList.Set(list(self.data["Object List"].keys()) )

				self.frame.update_object()

	def remove_object(self, cur_obj ):
		children = copy.deepcopy(self.data["Object List"][cur_obj]["Children"])
		self.data["Object List"].pop(cur_obj )
		for frame in range(len(self.data["Frames"])):
			self.data["Frames"][frame].pop(cur_obj )
		for child in children:
			self.remove_object(child)


	def CreateNewObject(self, event):
		#creates new object and names it accordingly
		#should be bound to a menu item to allow keyboard shortcuts
		box = wx.TextEntryDialog(None, "", "New Object Name", "new object")
		first = False
		if box.ShowModal() == wx.ID_OK:
			if len(self.data["Object List"]) < 1:
				first = True

			#creates empty object and copies default data values
			objValue = {"Images":[ "none" ], "Parent":None, "Children":[]}
			self.buildObject(box.GetValue(), data_default.default, objValue)
			self.window.PushHistory()

	def LoadObject(self, event):
		with wx.FileDialog(self, "Load Composite Object", wildcard="COB files (*.cob)|*.cob",
						style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
			if fileDialog.ShowModal() == wx.ID_CANCEL:
				return

			self.window.PushHistory()

			pathname = fileDialog.GetPath()
			tempData = json.loads(open(pathname, 'r').read())
			for image in tempData["Image List"]:
				self.data["Image List"].append(image)
				self.window.objCtrl.imgList.AddImg(image, False)

			for objname in tempData["Object List"].keys():
				self.buildObject(objname , tempData["frame data"][objname] , tempData["Object List"][objname])


	def copyObject(self, event):
		objValue = copy.deepcopy(self.data["Object List"][self.data["Current Object"]])
		name = self.data["Current Object"]

		new_name = name
		counter = 1

		while new_name in self.data["Object List"].keys():
			new_name = name + str(counter)
			counter += 1


		self.data["Parents"].append(new_name)
		self.data["Object List"][new_name] = objValue

		for frame in range(len(self.data["Frames"])):
			self.data["Frames"][frame][new_name] = copy.deepcopy(self.data["Frames"][frame][name])
		self.objList.Set(list(self.data["Object List"].keys() ))



	def buildObject(self, name, obj, objValue):

		self.data["Object List"][ name] = objValue
		for frame in range(len(self.data["Frames"])):
			self.data["Frames"][frame][name] = copy.deepcopy(obj)

		self.data["Current Object"] = name
		if objValue["Parent"] == None:
			self.data["Parents"].append(name )
		self.objList.Set(list(self.data["Object List"].keys()) )
		self.frame.update_object()

	def get_string(self):
		return self.objList.GetString(self.objList.GetSelection())