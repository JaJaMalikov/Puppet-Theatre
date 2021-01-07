#Graphical Libraries
import wx

#other built-in libraries
import copy

class Origin_State(wx.Panel):
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
		## start Origin group
		#self.Origin_panel = wx.Panel(self, size=(160, 110))

		#left side
		self.Origin_button = wx.Button(self, label="Origin", pos=(0,5))

		#middle
		self.Origin_x_text = wx.StaticText(self, label="X", pos=(80, 8))
		self.Origin_y_text = wx.StaticText(self, label="Y", pos=(80, 33))

		#right side
		self.Origin_x_spin = wx.SpinCtrl(self, initial=0, min=-2000, max=2000, pos=(95, 5), size=(52,23))
		self.Origin_y_spin = wx.SpinCtrl(self, initial=0, min=-2000, max=2000, pos=(95, 30), size=(52,23))

		self.Origin_keyframe_text = wx.StaticText(self, label="[  ]", pos=(5,85))
		self.Origin_keyframe_button = wx.Button(self, label="Keyframe", pos=(30, 83))

		self.Origin_inbetween_gen = wx.Button(self, label="Generate Inbetweens", pos=(10,110))

		self.overwrite_label = wx.StaticText(self, label="Overwrite:", pos=(0,140))
		self.overwrite_all = wx.Button(self, label="All", pos=(85, 137))

		self.overwrite_last = wx.Button(self, label="Previous", pos=(0, 159))
		self.overwrite_next = wx.Button(self, label="Next", pos=(85, 159))

		self.overwrite_future = wx.Button(self, label="Subsequent", pos=(85,181))
		self.overwrite_past = wx.Button(self, label="Preceeding", pos=(0,181))

		## end Origin group ############

	def set_layout(self):
		#self.Origin_sizer = wx.BoxSizer(wx.VERTICAL)
		#self.Origin_sizer.Add(self.Origin_panel, 0)

		#self.SetSizer(self.Origin_sizer)
		pass

	def bind_all(self):
		self.Origin_button.Bind(wx.EVT_BUTTON, self.On_Origin_button)

		self.Origin_x_spin.Bind(wx.EVT_SPINCTRL, self.On_Origin_x_spin)
		self.Origin_y_spin.Bind(wx.EVT_SPINCTRL, self.On_Origin_y_spin)

		self.Origin_keyframe_button.Bind(wx.EVT_BUTTON, self.On_set_Origin_keyframe)
		self.Origin_inbetween_gen.Bind(  wx.EVT_BUTTON, self.On_Origin_inbetween_gen)

		self.overwrite_next.Bind(wx.EVT_BUTTON, self.On_overwrite_next)
		self.overwrite_last.Bind(wx.EVT_BUTTON, self.On_overwrite_last)

		self.overwrite_all.Bind(wx.EVT_BUTTON, self.On_overwrite_all)

		self.overwrite_past.Bind(wx.EVT_BUTTON, self.On_overwrite_past)
		self.overwrite_future.Bind(wx.EVT_BUTTON, self.On_overwrite_future)


	def On_overwrite_future(self, event):
		#overwrites all future images with currently select image
		box = wx.MessageDialog(None, 'Are you sure you want to overwrite all subsequent frames?',
			"Overwrite all future frames", wx.OK | wx.CANCEL | wx.ICON_WARNING)
		if box.ShowModal() == wx.ID_OK:
			ref = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Origin"]
			for frame in range( self.data["Current Frame"], len(self.data["Frames"])):
				self.data["Frames"][frame][self.data["Current Object"]]["Origin"] = copy.deepcopy(ref)
			self.window.PushHistory()

	def On_overwrite_past(self, event):
		#overwrites all previous images with currently selected image
		box = wx.MessageDialog(None, 'Are you sure you want to overwrite all previous frames?',
			"Overwrite all previous frames", wx.OK | wx.CANCEL | wx.ICON_WARNING)
		if box.ShowModal() == wx.ID_OK:
			ref = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Origin"]
			for frame in range(0, self.data["Current Frame"]):
				self.data["Frames"][frame][self.data["Current Object"]]["Origin"] = copy.deepcopy(ref)
			self.window.PushHistory()

	def On_overwrite_all(self, event):
		#overwrites all frames with currently selected image
		box = wx.MessageDialog(None, 'Are you sure you want to overwrite all frames?',
			"Overwrite all frames", wx.OK | wx.CANCEL | wx.ICON_WARNING)
		if box.ShowModal() == wx.ID_OK:
			ref = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Origin"]
			for frame in range(len(self.data["Frames"])):
				self.data["Frames"][frame][self.data["Current Object"]]["Origin"] = copy.deepcopy(ref)
			self.window.PushHistory()

	def On_overwrite_last(self, event):
		#overwrites previous frame with currently selected image

		ref = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Origin"]
		self.data["Frames"][self.data["Current Frame"]-1][self.data["Current Object"]]["Origin"] = copy.deepcopy(ref)
		self.window.timelineCtrl.onBack(1)
		self.window.PushHistory()

	def On_overwrite_next(self, event):
		#overwrites next frame with currently selected image
		ref = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Origin"]
		self.data["Frames"][self.data["Current Frame"]+1][self.data["Current Object"]]["Origin"] = copy.deepcopy(ref)
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

	def On_Origin_inbetween_gen(self, event):
		pairs = self.get_key_list("Origin")

		for pair in pairs:
			start, end = pair

			total_steps = end-start

			init_x = self.data["Frames"][start][self.data["Current Object"]]["Origin"][0]
			init_y = self.data["Frames"][start][self.data["Current Object"]]["Origin"][1]

			end_x = self.data["Frames"][end][self.data["Current Object"]]["Origin"][0]
			end_y = self.data["Frames"][end][self.data["Current Object"]]["Origin"][1]

			diff_x = end_x - init_x
			diff_y = end_y - init_y

			step_x = diff_x / total_steps
			step_y = diff_y / total_steps

			for x in range((total_steps)):
				self.data["Frames"][x + start][self.data["Current Object"]]["Origin"][0] = init_x + (step_x * x)

			for y in range((total_steps)):
				self.data["Frames"][y + start][self.data["Current Object"]]["Origin"][1] = init_y + (step_y * y)

		self.window.PushHistory()


	def On_set_Origin_keyframe(self, event):
		if "Origin" not in self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Keyframes"]:
			self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Keyframes"].append("Origin")
		else:
			self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Keyframes"].remove("Origin")
		self.changed = True

	def On_Origin_button(self, event):
		obj = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]
		obj["Origin"][0] = 0.0
		obj["Origin"][1] = 0.0
		self.changed = True

	def On_Origin_x_spin(self, event):
		Origin = self.Origin_x_spin.GetValue()/100
		self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Origin"][0] = Origin
		self.changed = True

	def On_Origin_y_spin(self, event):
		Origin = self.Origin_y_spin.GetValue()/100
		self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Origin"][1] = Origin
		self.changed = True

	def Update(self, second):
		if second and self.changed:
			self.changed = False
			self.window.PushHistory()

		#try:
		### Origin update

		x_Origin = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Origin"][0]
		y_Origin = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Origin"][1]
		dist = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Pos"][2]

		self.Origin_x_spin.SetValue(int((x_Origin) * 100))
		self.Origin_y_spin.SetValue(int((y_Origin) * 100))

		if "Origin" in self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Keyframes"]:
			self.Origin_keyframe_text.SetLabel("[X]")
		else:
			self.Origin_keyframe_text.SetLabel("[   ]")
