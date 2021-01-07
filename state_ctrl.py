#graphical libraries
import wx
import pygame

from pos_state import Pos_State
from scale_state import Scale_State
from rot_state import Rot_State
from origin_state import Origin_State
#constants used throughout the program
from consts import *
#internal data structure default implementation
import data_default

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
		self.obj_name_panel= wx.Panel(self, size=(215,30), style=wx.RAISED_BORDER)
		self.object_name_text = wx.StaticText(self.obj_name_panel, label="Camera", pos=(0,3))

		self.mainBook = wx.Notebook(self)
		self.pos_state_page = Pos_State(self.mainBook, wx.ID_ANY, self.data, self.window, self.listener)
		self.scale_state_page = Scale_State(self.mainBook, wx.ID_ANY, self.data, self.window, self.listener)
		self.rot_state_page = Rot_State(self.mainBook, wx.ID_ANY, self.data, self.window, self.listener)
		self.origin_state_page = Origin_State(self.mainBook, wx.ID_ANY, self.data, self.window, self.listener)

		self.mainBook.AddPage(self.pos_state_page, "Position")
		self.mainBook.AddPage(self.scale_state_page, "Scale")
		self.mainBook.AddPage(self.rot_state_page, "Rotation")
		self.mainBook.AddPage(self.origin_state_page, "Origin")

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
		self.origin_state_page.set_data(self.data)

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
		self.origin_state_page.Update(second)


