import wx
import os
import copy

from datetime import datetime

import json

import numpy

from consts import *
import time

import data

class StateCtrl(wx.Panel):
	def __init__(self, parent, ID, data, window):
		wx.Panel.__init__(self, parent, ID,style = wx.RAISED_BORDER)
		"""
		current state = radiobutton for each value set
		value sets = sliders + textboxes, 
			slides with controlled object, 
			changes textbox onenter changes slider, 
			slider changes state and box
		keyframes = set state locations, when set. 
			each keyframe setting will be value set dependent
			generates all keyframe changes based on difference between keyframes
			divides the difference by the number of frames and adds each step to the in betweens
		"""
		self.data = data
		self.window = window
		self.full_sizer = wx.BoxSizer(wx.VERTICAL)
		#start groups

		self.obj_name_panel= wx.Panel(self, size=(160,30), style=wx.RAISED_BORDER)
		self.object_name_text = wx.StaticText(self.obj_name_panel, label="Camera", pos=(60,3))

		## start pos group
		self.pos_panel = wx.Panel(self, size=(160, 110), style=wx.RAISED_BORDER)

		#left side
		self.pos_button = wx.Button(self.pos_panel, label="Position", pos=(0,5))
		self.pos_keyframe_text = wx.StaticText(self.pos_panel, label="[  ]", pos=(5,32))
		self.pos_keyframe_button = wx.Button(self.pos_panel, label="Keyframe", pos=(0, 55))

		#middle
		self.pos_x_text = wx.StaticText(self.pos_panel, label="X", pos=(80, 8))
		self.pos_y_text = wx.StaticText(self.pos_panel, label="Y", pos=(80, 33))
		self.pos_z_text = wx.StaticText(self.pos_panel, label="Z", pos=(80, 58))

		#right side
		self.pos_x_spin = wx.SpinCtrl(self.pos_panel, initial=0, min=-2000, max=2000, pos=(95, 5), size=(52,23))
		self.pos_y_spin = wx.SpinCtrl(self.pos_panel, initial=0, min=-2000, max=2000, pos=(95, 30), size=(52,23))
		self.pos_z_spin = wx.SpinCtrl(self.pos_panel, initial=0, min=-100, max=200, pos=(95, 55), size=(52,23))

		self.pos_inbetween_gen = wx.Button(self.pos_panel, label="Generate Inbetweens", pos=(10,80))
		## end pos group ############

		## start scale group
		self.scale_panel = wx.Panel(self, size=(160, 110), style=wx.RAISED_BORDER)

		#left side
		self.scale_button = wx.Button(self.scale_panel, label="Scale", pos=(0,5))
		self.scale_aspect_box = wx.CheckBox(self.scale_panel, label="Aspect", pos=(0, 33))
		self.scale_x_text = wx.StaticText(self.scale_panel, label="X", pos=(2, 59))
		self.scale_x_spin = wx.SpinCtrl(self.scale_panel, initial=100, min=0, max=2000, pos=(15, 56))

		#right side
		self.scale_keyframe_button = wx.Button(self.scale_panel, label="Keyframe", pos=(78, 5))
		self.scale_keyframe_text = wx.StaticText(self.scale_panel, label="[   ]", pos=(80, 33))
		self.scale_y_text = wx.StaticText(self.scale_panel, label="Y", pos=(80, 59))
		self.scale_y_spin = wx.SpinCtrl(self.scale_panel, initial=100, min=0, max=2000, pos=(93, 55))

		self.scale_inbetween_gen = wx.Button(self.scale_panel, label="Generate Inbetweens", pos=(10,80))

		## end scale group ##########

		## start rot group

		self.rot_panel = wx.Panel(self, size=(160,110), style = wx.RAISED_BORDER)

		self.rot_button = wx.Button(self.rot_panel, label="rotation", pos=(0,0) )
		self.rot_spin_text = wx.StaticText(self.rot_panel, label="Degrees:", pos=(15, 33))
		self.rot_spin = wx.SpinCtrl(self.rot_panel, initial=0, min=-7200, max=7200, pos=(90, 33))
		self.rot_keyframe_button = wx.Button(self.rot_panel, label="Keyframe", pos=(0, 55))
		self.rot_keyframe_text = wx.StaticText(self.rot_panel, label="[   ]", pos=(80, 59))

		self.rot_inbetween_gen = wx.Button(self.rot_panel, label="Generate Inbetweens", pos=(10,80))

		## end rot group

		self.flip_panel = wx.Panel(self, size=(160, 110), style=wx.RAISED_BORDER)

		self.flip_x_button = wx.Button(self.flip_panel, label="Flip X", pos=(0,0))
		self.flip_y_button = wx.Button(self.flip_panel, label="Flip Y", pos=(80,0))

		## end groups
		self.full_sizer.Add(self.obj_name_panel)
		self.full_sizer.Add(self.pos_panel)
		self.full_sizer.Add(self.scale_panel)
		self.full_sizer.Add(self.rot_panel)
		self.full_sizer.Add(self.flip_panel)

		self.SetSizer(self.full_sizer)

		###bind all sliders and text boxes to events

		self.pos_button.Bind(wx.EVT_BUTTON, self.On_pos_button)

		self.pos_x_spin.Bind(wx.EVT_SPINCTRL, self.On_pos_x_spin)
		self.pos_y_spin.Bind(wx.EVT_SPINCTRL, self.On_pos_y_spin)
		self.pos_z_spin.Bind(wx.EVT_SPINCTRL, self.On_pos_z_spin)

		self.pos_keyframe_button.Bind(wx.EVT_BUTTON, self.On_set_pos_keyframe)

		self.scale_x_spin.Bind(wx.EVT_SPINCTRL, self.On_scale_x_spin)
		self.scale_y_spin.Bind(wx.EVT_SPINCTRL, self.On_scale_y_spin)

		self.scale_button.Bind(wx.EVT_BUTTON, self.On_scale_button)
		self.scale_keyframe_button.Bind(wx.EVT_BUTTON, self.On_set_scale_keyframe)

		self.rot_button.Bind(wx.EVT_BUTTON, self.On_rot_button)
		self.rot_spin.Bind(wx.EVT_SPINCTRL, self.On_rot_spin)

		self.rot_keyframe_button.Bind(wx.EVT_BUTTON, self.On_set_rot_keyframe)

		self.pos_inbetween_gen.Bind(  wx.EVT_BUTTON, self.On_pos_inbetween_gen)
		self.scale_inbetween_gen.Bind(wx.EVT_BUTTON, self.On_scale_inbetween_gen)
		self.rot_inbetween_gen.Bind(wx.EVT_BUTTON, self.On_rot_inbetween_gen)

		self.flip_x_button.Bind(wx.EVT_BUTTON, self.On_flip_x_button)
		self.flip_y_button.Bind(wx.EVT_BUTTON, self.On_flip_y_button)

		###end bind sliders

	def On_flip_x_button(self, event):
		self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["flipX"] *= -1.0

	def On_flip_y_button(self, event):
		self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["flipY"] *= -1.0

	def chunks(self, lst, n):
		"""Yield successive n-sized chunks from lst."""
		for i in range(0, len(lst)-1):
			yield lst[i:i + n]

	def get_key_list(self, key):
		keys = []
		for frame in range(len(self.data["Frames"])):
			if key in self.data["Frames"][frame][self.data["Current Object"]]["Keyframes"]:
				keys.append(frame)
		print(keys)
		pairs = list(self.chunks(keys, 2))
		return(pairs)

	def On_rot_inbetween_gen(self, event):
		print("gets here")
		pairs = self.get_key_list("rot")
		print(pairs)
		for pair in pairs:
			print(pair)
			start, end = pair

			total_steps = end-start

			init = self.data["Frames"][start][self.data["Current Object"]]["angle"]

			end = self.data["Frames"][end][self.data["Current Object"]]["angle"]

			diff = end - init

			step = diff / total_steps

			for a in range((total_steps)):
				self.data["Frames"][a + start][self.data["Current Object"]]["angle"] = init + (step * a)

	def On_scale_inbetween_gen(self, event):
		print("gets here")
		pairs = self.get_key_list("scale")

		print(pairs)

		for pair in pairs:
			start, end = pair

			total_steps = end-start

			init_x = self.data["Frames"][start][self.data["Current Object"]]["scaleX"]
			init_y = self.data["Frames"][start][self.data["Current Object"]]["scaleY"]

			end_x = self.data["Frames"][end][self.data["Current Object"]]["scaleX"]
			end_y = self.data["Frames"][end][self.data["Current Object"]]["scaleY"]

			diff_x = end_x - init_x
			diff_y = end_y - init_y

			step_x = diff_x / total_steps
			step_y = diff_y / total_steps

			for x in range((total_steps)):
				self.data["Frames"][x + start][self.data["Current Object"]]["scaleX"] = init_x + (step_x * x)

			for y in range((total_steps)):
				self.data["Frames"][y + start][self.data["Current Object"]]["scaleY"] = init_y + (step_y * y)

	def On_pos_inbetween_gen(self, event):
		print("gets here")

		pairs = self.get_key_list("pos")

		for pair in pairs:
			start, end = pair

			total_steps = end-start

			init_x = self.data["Frames"][start][self.data["Current Object"]]["pos"][0]
			init_y = self.data["Frames"][start][self.data["Current Object"]]["pos"][1]
			init_z = self.data["Frames"][start][self.data["Current Object"]]["pos"][2]

			end_x = self.data["Frames"][end][self.data["Current Object"]]["pos"][0]
			end_y = self.data["Frames"][end][self.data["Current Object"]]["pos"][1]
			end_z = self.data["Frames"][end][self.data["Current Object"]]["pos"][2]

			diff_x = end_x - init_x
			diff_y = end_y - init_y
			diff_z = end_z - init_z

			step_x = diff_x / total_steps
			step_y = diff_y / total_steps
			step_z = diff_z / total_steps

			for x in range((total_steps)):
				print(x+start)
				self.data["Frames"][x + start][self.data["Current Object"]]["pos"][0] = init_x + (step_x * x)

			for y in range((total_steps)):
				self.data["Frames"][y + start][self.data["Current Object"]]["pos"][1] = init_y + (step_y * y)

			for z in range((total_steps)):
				self.data["Frames"][z + start][self.data["Current Object"]]["pos"][2] = init_z + (step_z * z)

	def On_rot_spin(self, event):
		self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["angle"] = self.rot_spin.GetValue()


	def On_rot_button(self, event):
		self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["angle"] = 0

	def On_pos_button(self, event):
		self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["pos"][0] = 0.0
		self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["pos"][1] = 0.0
		self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["pos"][2] = 0.0

	def On_set_rot_keyframe(self, event):
		if "rot" not in self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Keyframes"]:
			self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Keyframes"].append("rot")
		else:
			self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Keyframes"].remove("rot")

	def On_set_pos_keyframe(self, event):
		if "pos" not in self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Keyframes"]:
			self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Keyframes"].append("pos")
		else:
			self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Keyframes"].remove("pos")

	def On_set_scale_keyframe(self, event):
		if "scale" not in self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Keyframes"]:
			self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Keyframes"].append("scale")
		else:
			self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Keyframes"].remove("scale")

	def On_scale_button(self, event):
		self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["scaleY"] = 1.0
		self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["scaleX"] = 1.0

	def On_scale_x_spin(self, event):
		self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["scaleX"] = self.scale_x_spin.GetValue()/100
		if self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Aspect"]:
			self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["scaleY"] = self.scale_x_spin.GetValue()/100

	def On_scale_y_spin(self, event):
		self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["scaleY"] = self.scale_y_spin.GetValue()/100
		if self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Aspect"]:
			self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["scaleX"] = self.scale_y_spin.GetValue()/100

	def On_pos_x_spin(self, event):
		dist = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["pos"][2]
		pos = self.pos_x_spin.GetValue()/100
		width = ((dist*-1.0) * .59) + 6.0
		self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["pos"][0] = ((width*2) * pos) - width

	def On_pos_y_spin(self, event):
		dist = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["pos"][2]
		pos = 1-self.pos_y_spin.GetValue()/100
		height = (((dist*-1.0) * .4) + 4.2)
		self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["pos"][1] = ((height*2) * pos) - height

	def On_pos_z_spin(self, event):
		self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["pos"][2] = 10-(self.pos_z_spin.GetValue()/2)

	def set_data(self, data):
		self.data = data



	def Update(self, second):
		#try:
		### pos update

		self.object_name_text.SetLabel(self.data["Current Object"])

		x_pos = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["pos"][0]
		y_pos = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["pos"][1]
		dist = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["pos"][2]

		x_pos += (((dist*-1.0) * .59) + 6.0)
		y_pos += (((dist*-1.0) * .4) + 4.2)

		width = (((dist*-1.0) * .59) + 6.0) * 2
		height = (((dist*-1.0) * .4) + 4.2) * 2

		self.pos_x_spin.SetValue(int((x_pos / width) * 100))
		self.pos_y_spin.SetValue(100-int((y_pos / height) * 100))
		self.pos_z_spin.SetValue(int( (10 - dist) * 2 ))

		if "pos" in self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Keyframes"]:
			self.pos_keyframe_text.SetLabel("[X] Keyframe")
		else:
			self.pos_keyframe_text.SetLabel("[   ] Keyframe")

		### scale update
		x_scale = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["scaleX"]
		y_scale = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["scaleY"]

		self.scale_x_spin.SetValue(int(x_scale*100))
		self.scale_y_spin.SetValue(int(y_scale*100))

		self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Aspect"] = self.scale_aspect_box.GetValue()

		if "scale" in self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Keyframes"]:
			self.scale_keyframe_text.SetLabel("[X] Keyframe")
		else:
			self.scale_keyframe_text.SetLabel("[   ] Keyframe")

		self.rot_spin.SetValue(self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["angle"] )

		if "rot" in self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Keyframes"]:
			self.rot_keyframe_text.SetLabel("[X] Keyframe")
		else:
			self.rot_keyframe_text.SetLabel("[   ] Keyframe")
		#except:
		#	pass

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

	app = wx.App()
	view = testFrame(parent=None, title='Finger Pupper Theatre', size=(1500,700))
	view.Show()
	app.MainLoop()