#Graphical Libraries
import wx

#Other Build in Libraries
import copy

#vertex default values
import verts

#internal data structure default implementation
import data_default

#container class for 2D object texture
from OBJ2D import OBJ2D

loc = 110

class ParentMenu(wx.Menu):
	def __init__(self, parent, data):
		super(ParentMenu, self).__init__()

		self.parent = parent
		self.data = data

		mmi = wx.MenuItem(self, wx.NewId(), 'Set Parent')
		self.AppendItem(mmi)
		self.Bind(wx.EVT_MENU, self.OnMakeParent, mmi)

	def OnMakeParent(self, event):
		keylist = list(self.data["Object List"].keys())
		for key in keylist:
			if self.data["Object List"][key]["Parent"] != None:
				keylist.remove(key)
		self.dlg = wx.SingleChoiceDialog(None, "Which", "title", keylist, wx.CHOICEDLG_STYLE)
		if self.dlg.ShowModal() == wx.ID_OK:
			objname = self.dlg.GetStringSelection()
			self.data["Object List"][self.data["Current Object"]]["Parent"] = objname
			self.data["Object List"][objname]["Children"].append(self.data["Current Object"])
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
		self.objList.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)

	def OnRightDown(self, event):
		print("clicked")
		self.PopupMenu(ParentMenu(self, self.data), event.GetPosition())

	def set_layout(self):
		self.buttonSizer = wx.BoxSizer(wx.VERTICAL)
		self.pageSizer = wx.BoxSizer(wx.VERTICAL)

		self.t_b_sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.b_b_sizer = wx.BoxSizer(wx.HORIZONTAL)

		self.t_b_sizer.Add(self.btn1)
		self.t_b_sizer.Add(self.btn2)
		self.b_b_sizer.Add(self.btn3)
		self.b_b_sizer.Add(self.btn4)
		self.buttonSizer.Add(self.t_b_sizer)
		self.buttonSizer.Add(self.b_b_sizer)
		self.pageSizer.Add(self.buttonSizer, 0)

		self.pageSizer.Add(self.objList, -1, wx.EXPAND)

		self.SetSizer(self.pageSizer)

	def build(self):
		self.btn1 = wx.Button(self, 1, "New")
		self.btn2 = wx.Button(self, 1, "Delete")
		self.btn3 = wx.Button(self, 1, "Save")
		self.btn4 = wx.Button(self, 1, "Load")
		self.objList = wx.ListBox(self, wx.ID_ANY)

	def set_data(self, data):
		self.data = data

	def reload(self):
		self.objList.Set(list(self.data["Object List"].keys()) )

	def DeleteObject(self, event):
		#should be bound to a menu item one day with an "are you sure" box attached
		if self.data["Current Object"] != "Camera":
			box = wx.MessageDialog(None, 'Are you sure you want to delete %s' % self.data["Current Object"],
				"Delete Object", wx.OK | wx.CANCEL | wx.ICON_WARNING)
			if box.ShowModal() == wx.ID_OK:
				self.window.Set_Third_Status(self.data["Current Object"] + " deleted")

				self.data["Object List"].pop(self.data["Current Object"])
				for frame in range(len(self.data["Frames"])):
					self.data["Frames"][frame].pop(self.data["Current Object"])

				self.data["Current Object"] = list(self.data["Object List"].keys())[0]

				self.objList.Set(list(self.data["Object List"].keys()) )

				self.frame.update_object()


	def CreateNewObject(self, event):
		#creates new object and names it accordingly
		#should be bound to a menu item to allow keyboard shortcuts
		box = wx.TextEntryDialog(None, "", "New Object Name", "new object")
		first = False
		if box.ShowModal() == wx.ID_OK:
			if len(self.data["Object List"]) < 1:
				first = True

			#creates empty object and copies default data values
			self.data["Object List"][box.GetValue()] = {"Images":[ "none" ], "Parent":None, "Children":[]}

			for frame in range(len(self.data["Frames"])):
				self.data["Frames"][frame][box.GetValue()] = copy.deepcopy(data_default.default)

			self.data["Current Object"] = box.GetValue()
		self.objList.Set(list(self.data["Object List"].keys()) )
		self.frame.update_object()

	def get_string(self):
		return self.objList.GetString(self.objList.GetSelection())