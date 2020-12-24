#Graphical Libraries
import wx

#other built-in libraries
import os
import ffmpeg


#constants to be used throughout program
from consts import *
#canvasbase for rendering video
from canvas_base import CanvasBase

loc = 87

class RenderVideoDialog(wx.Dialog):
	def __init__(self, *args, **kw):
		"""
		saves the current rendered frames into a video
		adds audio if box is checked
		"""
		super(RenderVideoDialog, self).__init__(*args, **kw)

		self.InitUI()
		self.SetSize((250, 200))
		self.SetTitle("Render Images to Video")
		self.window = None
		self.data = None
		self.FBO = None
		self.px_width = None
		self.px_height = None
		self.Image_list = None

	def set_window(self, window):
		"""
		creates all dialog data from window base data, only the window
		is passed as future-proofing, if another variable is needed
		then it can be created anywhere else and then a single line can be added here
		"""
		self.window = window
		self.data = self.window.data
		self.FBO = self.window.renderCtrl.FBO
		self.px_width = self.window.renderCtrl.px_width
		self.px_height = self.window.renderCtrl.px_height

		self.xoffset = self.window.renderCtrl.xoffset
		self.yoffset = self.window.renderCtrl.yoffset
		self.canvas = self.window.renderCtrl.canvas

		self.Image_list = self.window.Image_list

	def InitUI(self):
		self.pnl = wx.Panel(self, size=(250,200))
		self.render_button = wx.Button(self.pnl, label="Render", pos = (0,0))
		self.render_status = wx.StaticText(self.pnl, label="Ready to render", pos=(110, 3))
		self.add_audio_box = wx.CheckBox(self.pnl, label="Add audio", pos=(0, 30))
		self.render_button.Bind(wx.EVT_BUTTON, self.On_render_button)

	def On_render_button(self, event):
		"""
		uses ffmpeg library to render video from frames
		currently output mp4 is not compatible with twitter and must be formatted
		currently no feedback is given to the program causing it to lock up during render
		both problems to be fixed in later releases
		"""
		self.render_status.SetLabel("Rendering...")
		if os.path.exists(self.data["Video Name"]):
			os.remove(self.data["Video Name"])
		if self.add_audio_box.GetValue():
			(
				ffmpeg
				.input(self.data["Render Dir"] + "/Frames/%06d.png", framerate=self.data["FPS"])
				.output(self.data["Video Name"])
				.global_args("-i", self.data["Audio"])
				.run()
			)
		else:
			(
				ffmpeg
				.input(self.data["Render Dir"] + "/Frames/%06d.png", framerate=self.data["FPS"])
				.output(self.data["Video Name"])
				.run()
			)
		self.render_status.SetLabel("Video rendered! <3")

	def OnClose(self, event):
		self.Destroy()