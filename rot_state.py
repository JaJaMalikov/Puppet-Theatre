#Graphical Libraries
import wx

#other built-in libraries
import copy

class Rot_State(wx.Panel):
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

		## start rot group

		self.rot_button = wx.Button(self, label="rotation", pos=(0,0) )
		self.rot_spin_text = wx.StaticText(self, label="Degrees:", pos=(15, 33))
		self.rot_spin = wx.SpinCtrl(self, initial=0, min=-7200, max=7200, pos=(90, 33))
		self.rot_keyframe_button = wx.Button(self, label="Keyframe", pos=(20, 57))
		self.rot_keyframe_text = wx.StaticText(self, label="[   ]", pos=(0, 61))

		self.rot_inbetween_gen = wx.Button(self, label="Generate Inbetweens", pos=(10,80))

		## end rot group


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
		self.rot_button.Bind(wx.EVT_BUTTON, self.On_rot_button)
		self.rot_spin.Bind(wx.EVT_SPINCTRL, self.On_rot_spin)

		self.rot_keyframe_button.Bind(wx.EVT_BUTTON, self.On_set_rot_keyframe)

		self.rot_inbetween_gen.Bind(wx.EVT_BUTTON, self.On_rot_inbetween_gen)

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
			ref = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Angle"]
			for frame in range( self.data["Current Frame"], len(self.data["Frames"])):
				self.data["Frames"][frame][self.data["Current Object"]]["Angle"] = copy.deepcopy(ref)
			self.window.PushHistory()

	def On_overwrite_past(self, event):
		#overwrites all previous images with currently selected image
		box = wx.MessageDialog(None, 'Are you sure you want to overwrite all previous frames?',
			"Overwrite all previous frames", wx.OK | wx.CANCEL | wx.ICON_WARNING)
		if box.ShowModal() == wx.ID_OK:
			ref = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Angle"]
			for frame in range(0, self.data["Current Frame"]):
				self.data["Frames"][frame][self.data["Current Object"]]["Angle"] = copy.deepcopy(ref)
			self.window.PushHistory()

	def On_overwrite_all(self, event):
		#overwrites all frames with currently selected image
		box = wx.MessageDialog(None, 'Are you sure you want to overwrite all frames?',
			"Overwrite all frames", wx.OK | wx.CANCEL | wx.ICON_WARNING)
		if box.ShowModal() == wx.ID_OK:
			ref = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Angle"]
			for frame in range(len(self.data["Frames"])):
				self.data["Frames"][frame][self.data["Current Object"]]["Angle"] = copy.deepcopy(ref)
			self.window.PushHistory()

	def On_overwrite_last(self, event):
		#overwrites previous frame with currently selected image

		ref = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Angle"]
		self.data["Frames"][self.data["Current Frame"]-1][self.data["Current Object"]]["Angle"] = copy.deepcopy(ref)
		self.window.timelineCtrl.onBack(1)
		self.window.PushHistory()

	def On_overwrite_next(self, event):
		#overwrites next frame with currently selected image
		ref = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Angle"]
		self.data["Frames"][self.data["Current Frame"]+1][self.data["Current Object"]]["Angle"] = copy.deepcopy(ref)
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

	def On_rot_inbetween_gen(self, event):
		pairs = self.get_key_list("Rot")
		for pair in pairs:
			start, end = pair

			total_steps = end-start

			init = self.data["Frames"][start][self.data["Current Object"]]["Angle"]

			end = self.data["Frames"][end][self.data["Current Object"]]["Angle"]

			diff = end - init

			step = diff / total_steps

			for a in range((total_steps)):
				self.data["Frames"][a + start][self.data["Current Object"]]["Angle"] = init + (step * a)
		self.window.PushHistory()

	def On_rot_spin(self, event):
		self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Angle"] = self.rot_spin.GetValue()
		self.changed = True


	def On_rot_button(self, event):
		self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Angle"] = 0
		self.changed = True

	def On_set_rot_keyframe(self, event):
		if "Rot" not in self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Keyframes"]:
			self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Keyframes"].append("Rot")
		else:
			self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Keyframes"].remove("Rot")
		self.changed = True



	def Update(self, second):
		if second and self.changed:
			self.changed = False
			self.window.PushHistory()

		#try:
		### pos update

		self.rot_spin.SetValue(self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Angle"] )

		if "Rot" in self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Keyframes"]:
			self.rot_keyframe_text.SetLabel("[X]")
		else:
			self.rot_keyframe_text.SetLabel("[   ]")
