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

class objCtrl(wx.Panel):
	"""
	A container class for the object list and image list
	allows for per-frame control over currently selected objects
	and their currently available images
	"""
	def __init__(self, parent, data, window, Image_list, listener):
		wx.Panel.__init__(self, parent,style = wx.RAISED_BORDER)
		self.data = data
		self.window = window
		self.Image_list = Image_list
		self.listener = listener

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
		self.imgList = ImageList(self.mainBook, wx.ID_ANY, self.data, self.window, self, self.Image_list, self.listener)

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
		self.imgList.Update(second)

	def set_data(self, data):
		#loads data to load new or old projects
		self.data = data
		self.objList.set_data(self.data)
		self.imgList.set_data(self.data)

	def reload(self, load_from_file):
		#reloads all available images and objects
		self.objList.reload()
		self.imgList.reload(load_from_file)

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



