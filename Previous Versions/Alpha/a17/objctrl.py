import wx
import os
import copy
import pygame
from pygame.locals import Color
from collections import OrderedDict
from pygamepanel import PygamePanel
import  wx.lib.newevent, wx.stc as stc
from statusctrl import StatusCtrl
from plane import OBJ2D
from record import Record
from camera import camera
from background import Background

class objCtrl(wx.Panel):
	def __init__(self, parent, ID, HUD):
		wx.Panel.__init__(self, parent, ID)
		self.cur_obj_size = 31990
		self.HUD = HUD
		self.cur_obj = 0
		self.data = {}
		self.data["cur_cam"] = 0
		self.cur_group = "Actors" # Actors, Cameras, BGs, Props
		self.wireFrame = False
		self.record = Record()

		#this contains the actual entities within the program
		#not to be loaded until opengl is called
		self.entities = {}
		self.entities["Actors"] = []
		self.entities["Props"] = []
		self.entities["Cameras"] = []
		self.entities["BGs"] = []
		self.visible = []

		self.default_order = list(range(30))

		self.buttons = []
		self.selector = wx.BoxSizer(wx.HORIZONTAL)

		#selection buttons
		pic = wx.Bitmap("defport.png", wx.BITMAP_TYPE_ANY)

		for x in range(10):
			self.buttons.append(wx.BitmapButton(self, -1, pic, name=str(x)))

		for x in range(10):
			self.selector.Add(self.buttons[x], 0, wx.EXPAND)

		self.groups = wx.BoxSizer(wx.VERTICAL)
		self.tgroup = wx.BoxSizer(wx.HORIZONTAL)
		self.bgroup = wx.BoxSizer(wx.HORIZONTAL)

		self.Actors_button = wx.Button(self, label="Actors")
		self.Cameras_button = wx.Button(self, label="Cameras")
		self.Props_button = wx.Button(self, label="Props")
		self.BGs_button = wx.Button(self, label="BGs")

		self.tgroup.Add(self.Actors_button, 0, wx.EXPAND)
		self.tgroup.Add(self.Cameras_button, 0, wx.EXPAND)
		self.groups.Add(self.tgroup, 0, wx.EXPAND)

		self.bgroup.Add(self.Props_button, 0, wx.EXPAND)
		self.bgroup.Add(self.BGs_button, 0, wx.EXPAND)
		self.groups.Add(self.bgroup, 0, wx.EXPAND)

		self.selector.Add(self.groups, 0, wx.EXPAND)

		self.SetSizer(self.selector)
		self.SetAutoLayout(1)

		for x in range(10):
			self.Bind(wx.EVT_BUTTON, self.OnLoad, self.buttons[x])

	def OnLoad(self, event):
		with wx.DirDialog(self, "Choose input directory", "",
							wx.DD_DEFAULT_STYLE| wx.DD_DIR_MUST_EXIST) as dirDialog:
			if dirDialog.ShowModal() == wx.ID_CANCEL:
				return

			pathname = dirDialog.GetPath()
			self.entities[self.cur_group][(event.GetId()+self.cur_obj_size)].load_all(pathname)
			port = self.entities[self.cur_group][(event.GetId()+self.cur_obj_size)].get_portrait()
			if port != None:
				pic = wx.Bitmap(port, wx.BITMAP_TYPE_ANY)
				event.GetEventObject().SetBitmap(pic)
				self.refresh()

	def places(self):
		for x in range(10):
			for key in self.entities.keys():
				self.entities[key][x].places()

	def boil(self):
		self.entities[self.cur_group][self.cur_obj].boil()

	def scale(self):
		self.entities[self.cur_group][self.cur_obj].scale()

	def draw_wire(self):
		self.wireFrame = (not self.wireFrame)

	def set_mouth(self, mouth):
		self.entities[self.cur_group][self.cur_obj].set_mouth(mouth)

	def set_state(self, state):
		self.entities[self.cur_group][self.cur_obj].set_state(state)

	def set_substate(self, substate):
		self.entities[self.cur_group][self.cur_obj].set_substate(substate)

	def set_dir(self, Dir):
		self.entities[self.cur_group][self.cur_obj].set_dir(Dir)

	def space_toggle(self, toggle):
		self.entities[self.cur_group][self.cur_obj].space_toggle(toggle)

	def start_record_cam(self):
		self.record.start()

	def stop_record_cam(self):
		self.record.pause()

	def clear_cam(self):
		self.record.clear()

	def play_cam(self):
		self.record.playback()

	def pause_cam(self):
		self.record.stop()

	def zoom(self, factor):
		self.entities[self.cur_group][self.cur_obj].zoom(factor)

	def flipX(self):
		self.entities[self.cur_group][self.cur_obj].flipX()

	def flipY(self):
		self.entities[self.cur_group][self.cur_obj].flipY()

	def set_visible(self, vis):
		self.entities[self.cur_group][self.cur_obj].set_visible(vis)		

	def start_recording(self):
		self.entities[self.cur_group][self.cur_obj].start_recording()

	def stop_recording(self):
		self.entities[self.cur_group][self.cur_obj].stop_recording()

	def start_playing(self):
		self.entities[self.cur_group][self.cur_obj].start_playing()

	def stop_playing(self):
		self.entities[self.cur_group][self.cur_obj].stop_playing()

	def clear(self):
		self.entities[self.cur_group][self.cur_obj].clear()		

	def m_rot(self, m_rel):
		self.entities[self.cur_group][self.cur_obj].m_rot(m_rel)

	def rotp(self):
		self.entities[self.cur_group][self.cur_obj].rotp()

	def rotn(self):
		self.entities[self.cur_group][self.cur_obj].rotn()

	def set_pos(self,pos):
		self.entities[self.cur_group][self.cur_obj].set_pos(pos)

	def move_H(self, delta):
		self.entities[self.cur_group][self.cur_obj].move_H(delta)

	def move_V(self, delta):
		self.entities[self.cur_group][self.cur_obj].move_V(delta)

	def move_D(self, delta):
		self.entities[self.cur_group][self.cur_obj].move_D(delta)

	def get_cur(self):
		return self.cur_obj

	def set_obj(self, obj):
		self.cur_obj = obj
		if self.cur_group == "Cameras":
			self.data["cur_cam"] = obj
			print(self.data["cur_cam"])

	def get_viewport(self):
		return self.entities["Cameras"][self.data["cur_cam"]]

	def set_group(self, group):
		self.cur_group = group

	def set_data(self):
		self.HUD.set_group(self.cur_group)
		self.HUD.set_selection(self.cur_obj)
		self.entities[self.cur_group][self.cur_obj].set_data()

	def populate(self):
		for x in range(10):
			for key in self.entities.keys():
				if key == "Actors":
					ent = OBJ2D(None, self.HUD)
					self.entities[key].append(ent)
					self.visible.append(ent)

				elif key == "Cameras":
					ent = camera(None, self.HUD)
					self.entities[key].append(ent)

				elif key == "Props":
					ent = OBJ2D(None, self.HUD)
					self.entities[key].append(ent)
					self.visible.append(ent)

				else:
					ent = Background(None, self.HUD)
					self.entities[key].append(ent)
					self.visible.append(ent)


	def clear_camera(self):
		for cam in self.entities["Cameras"]:
			cam.clear_cam()

	def update(self):

		for x in range(10):
			for key in self.entities.keys():
				self.entities[key][x].update()

		draw_order = [x for _, x in sorted(zip( self.visible , self.default_order), key=lambda x: x[0].data["pos"][2] )]

		for x in draw_order:
			self.visible[x].draw_entity()
			if self.wireFrame:
				self.visible[x].draw_wire()
