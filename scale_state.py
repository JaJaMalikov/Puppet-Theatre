#Graphical Libraries
import wx

#other built-in libraries
import copy

class Scale_State(wx.Panel):
	def __init__(self, parent, ID, data, window, listener):
		wx.Panel.__init__(self, parent, ID, style=wx.RAISED_BORDER)
		
		self.parent = parent
		self.data = data
		self.window = window
		self.listener = listener
		self.changed = False

		self.build()
		self.set_layout()
		self.bind_all()

	def set_data(self, data):
		self.data = data

	def build(self):
		## start pos group
		#self.pos_panel = wx.Panel(self, size=(160, 110))

		## start scale group

		#left side
		self.scale_button = wx.Button(self, label="Scale", pos=(0,5))
		self.scale_aspect_box = wx.CheckBox(self, label="Aspect", pos=(0, 33))
		self.scale_x_text = wx.StaticText(self, label="X", pos=(2, 59))
		self.scale_x_spin = wx.SpinCtrl(self, initial=100, min=0, max=2000, pos=(15, 56))

		#right side
		self.scale_keyframe_button = wx.Button(self, label="Keyframe", pos=(78, 5))
		self.scale_keyframe_text = wx.StaticText(self, label="[   ]", pos=(80, 33))
		self.scale_y_text = wx.StaticText(self, label="Y", pos=(80, 59))
		self.scale_y_spin = wx.SpinCtrl(self, initial=100, min=0, max=2000, pos=(93, 55))

		self.scale_inbetween_gen = wx.Button(self, label="Generate Inbetweens", pos=(10,80))

		self.flip_x_button = wx.Button(self, label="Flip X", pos=(0,110))
		self.flip_y_button = wx.Button(self, label="Flip Y", pos=(80,110))

		## end scale group ##########

		self.overwrite_label = wx.StaticText(self, label="Overwrite:", pos=(0,140))
		self.overwrite_all = wx.Button(self, label="All", pos=(85, 137))

		self.overwrite_last = wx.Button(self, label="Previous", pos=(0, 159))
		self.overwrite_next = wx.Button(self, label="Next", pos=(85, 159))

		self.overwrite_future = wx.Button(self, label="Subsequent", pos=(85,181))
		self.overwrite_past = wx.Button(self, label="Preceeding", pos=(0,181))

		## end pos group ############

	def set_layout(self):
		#self.pos_sizer = wx.BoxSizer(wx.VERTICAL)
		#self.pos_sizer.Add(self.pos_panel, 0)

		#self.SetSizer(self.pos_sizer)
		pass

	def bind_all(self):
		self.scale_x_spin.Bind(wx.EVT_SPINCTRL, self.On_scale_x_spin)
		self.scale_y_spin.Bind(wx.EVT_SPINCTRL, self.On_scale_y_spin)

		self.scale_button.Bind(wx.EVT_BUTTON, self.On_scale_button)
		self.scale_keyframe_button.Bind(wx.EVT_BUTTON, self.On_set_scale_keyframe)

		self.scale_inbetween_gen.Bind(wx.EVT_BUTTON, self.On_scale_inbetween_gen)

		self.overwrite_next.Bind(wx.EVT_BUTTON, self.On_overwrite_next)
		self.overwrite_last.Bind(wx.EVT_BUTTON, self.On_overwrite_last)

		self.overwrite_all.Bind(wx.EVT_BUTTON, self.On_overwrite_all)

		self.overwrite_past.Bind(wx.EVT_BUTTON, self.On_overwrite_past)
		self.overwrite_future.Bind(wx.EVT_BUTTON, self.On_overwrite_future)

		self.flip_x_button.Bind(wx.EVT_BUTTON, self.On_flip_x_button)
		self.flip_y_button.Bind(wx.EVT_BUTTON, self.On_flip_y_button)

	def On_flip_x_button(self, event):
		self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["FlipX"] *= -1.0
		self.changed = True

	def On_flip_y_button(self, event):
		self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["FlipY"] *= -1.0
		self.changed = True

	def On_overwrite_future(self, event):
		#overwrites all future images with currently select image
		box = wx.MessageDialog(None, 'Are you sure you want to overwrite all subsequent frames?',
			"Overwrite all future frames", wx.OK | wx.CANCEL | wx.ICON_WARNING)
		if box.ShowModal() == wx.ID_OK:
			refX = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["ScaleX"]
			refY = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["ScaleY"]
			refFX = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["FlipX"]
			refFY = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["FlipY"]
			for frame in range( self.data["Current Frame"], len(self.data["Frames"])):
				self.data["Frames"][frame][self.data["Current Object"]]["FlipX"] = copy.deepcopy(refFX)
				self.data["Frames"][frame][self.data["Current Object"]]["FlipY"] = copy.deepcopy(refFY)
				self.data["Frames"][frame][self.data["Current Object"]]["ScaleX"] = copy.deepcopy(refX)
				self.data["Frames"][frame][self.data["Current Object"]]["ScaleY"] = copy.deepcopy(refY)
			self.window.PushHistory()

	def On_overwrite_past(self, event):
		#overwrites all previous images with currently selected image
		box = wx.MessageDialog(None, 'Are you sure you want to overwrite all previous frames?',
			"Overwrite all previous frames", wx.OK | wx.CANCEL | wx.ICON_WARNING)
		if box.ShowModal() == wx.ID_OK:
			refX = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["ScaleX"]
			refY = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["ScaleY"]
			refFX = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["FlipX"]
			refFY = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["FlipY"]
			for frame in range(0, self.data["Current Frame"]):
				self.data["Frames"][frame][self.data["Current Object"]]["FlipX"] = copy.deepcopy(refFX)
				self.data["Frames"][frame][self.data["Current Object"]]["FlipY"] = copy.deepcopy(refFY)
				self.data["Frames"][frame][self.data["Current Object"]]["ScaleX"] = copy.deepcopy(refX)
				self.data["Frames"][frame][self.data["Current Object"]]["ScaleY"] = copy.deepcopy(refY)
			self.window.PushHistory()

	def On_overwrite_all(self, event):
		#overwrites all frames with currently selected image
		box = wx.MessageDialog(None, 'Are you sure you want to overwrite all frames?',
			"Overwrite all frames", wx.OK | wx.CANCEL | wx.ICON_WARNING)
		if box.ShowModal() == wx.ID_OK:
			refX = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["ScaleX"]
			refY = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["ScaleY"]
			refFX = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["FlipX"]
			refFY = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["FlipY"]
			for frame in range(len(self.data["Frames"])):
				self.data["Frames"][frame][self.data["Current Object"]]["FlipX"] = copy.deepcopy(refFX)
				self.data["Frames"][frame][self.data["Current Object"]]["FlipY"] = copy.deepcopy(refFY)
				self.data["Frames"][frame][self.data["Current Object"]]["ScaleX"] = copy.deepcopy(refX)
				self.data["Frames"][frame][self.data["Current Object"]]["ScaleY"] = copy.deepcopy(refY)
			self.window.PushHistory()

	def On_overwrite_last(self, event):
		#overwrites previous frame with currently selected image

		refX = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["ScaleX"]
		refY = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["ScaleY"]
		refFX = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["FlipX"]
		refFY = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["FlipY"]
		self.data["Frames"][self.data["Current Frame"]-1][self.data["Current Object"]]["FlipX"] = copy.deepcopy(refFX)
		self.data["Frames"][self.data["Current Frame"]-1][self.data["Current Object"]]["FlipY"] = copy.deepcopy(refFY)
		self.data["Frames"][self.data["Current Frame"]-1][self.data["Current Object"]]["ScaleX"] = copy.deepcopy(refX)
		self.data["Frames"][self.data["Current Frame"]-1][self.data["Current Object"]]["ScaleY"] = copy.deepcopy(refY)
		self.window.timelineCtrl.onBack(1)
		self.window.PushHistory()

	def On_overwrite_next(self, event):
		#overwrites next frame with currently selected image
		refX = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["ScaleX"]
		refY = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["ScaleY"]
		refFX = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["FlipX"]
		refFY = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["FlipY"]

		self.data["Frames"][self.data["Current Frame"]+1][self.data["Current Object"]]["FlipX"] = copy.deepcopy(refFX)
		self.data["Frames"][self.data["Current Frame"]+1][self.data["Current Object"]]["FlipY"] = copy.deepcopy(refFY)
		self.data["Frames"][self.data["Current Frame"]+1][self.data["Current Object"]]["ScaleX"] = copy.deepcopy(refX)
		self.data["Frames"][self.data["Current Frame"]+1][self.data["Current Object"]]["ScaleY"] = copy.deepcopy(refY)
		self.window.timelineCtrl.onNext(1)
		self.window.PushHistory()

		####################

	def chunks(self, lst, n):
		"""Yield successive n-sized chunks from lst."""
		for i in range(0, len(lst)-1):
			yield lst[i:i + n]

	def get_key_list(self, key):
		keys = []
		for frame in range(len(self.data["Frames"])):
			if key in self.data["Frames"][frame][self.data["Current Object"]]["Keyframes"]:
				keys.append(frame)
		pairs = list(self.chunks(keys, 2))
		return(pairs)

	def On_scale_inbetween_gen(self, event):
		pairs = self.get_key_list("Scale")

		for pair in pairs:
			start, end = pair

			total_steps = end-start

			init_x = self.data["Frames"][start][self.data["Current Object"]]["ScaleX"]
			init_y = self.data["Frames"][start][self.data["Current Object"]]["ScaleY"]

			end_x = self.data["Frames"][end][self.data["Current Object"]]["ScaleX"]
			end_y = self.data["Frames"][end][self.data["Current Object"]]["ScaleY"]

			diff_x = end_x - init_x
			diff_y = end_y - init_y

			step_x = diff_x / total_steps
			step_y = diff_y / total_steps

			for x in range((total_steps)):
				self.data["Frames"][x + start][self.data["Current Object"]]["ScaleX"] = init_x + (step_x * x)

			for y in range((total_steps)):
				self.data["Frames"][y + start][self.data["Current Object"]]["ScaleY"] = init_y + (step_y * y)
		self.window.PushHistory()


	def On_set_scale_keyframe(self, event):
		if "Scale" not in self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Keyframes"]:
			self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Keyframes"].append("Scale")
		else:
			self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Keyframes"].remove("Scale")
		self.changed = True

	def On_scale_button(self, event):
		self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["ScaleY"] = 1.0
		self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["ScaleX"] = 1.0
		self.changed = True

	def On_scale_x_spin(self, event):
		self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["ScaleX"] = self.scale_x_spin.GetValue()/100
		if self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Aspect"]:
			self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["ScaleY"] = self.scale_x_spin.GetValue()/100
		self.changed = True

	def On_scale_y_spin(self, event):
		self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["ScaleY"] = self.scale_y_spin.GetValue()/100
		if self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Aspect"]:
			self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["ScaleX"] = self.scale_y_spin.GetValue()/100
		self.changed = True

	def Update(self, second):
		if second and self.changed:
			self.changed = False
			self.window.PushHistory()

		#try:
		### pos update

		x_scale = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["ScaleX"]
		y_scale = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["ScaleY"]

		self.scale_x_spin.SetValue(int(x_scale*100))
		self.scale_y_spin.SetValue(int(y_scale*100))

		self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Aspect"] = self.scale_aspect_box.GetValue()

		if "Scale" in self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Keyframes"]:
			self.scale_keyframe_text.SetLabel("[X]")
		else:
			self.scale_keyframe_text.SetLabel("[   ]")

