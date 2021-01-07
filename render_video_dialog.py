#Graphical Libraries
import wx
import pygame

#other built-in libraries
import os
import ffmpeg
import shutil

import copy

#constants to be used throughout program
from consts import *
#canvasbase for rendering video
from canvas_base import CanvasBase

class RenderVideoDialog(wx.Dialog):
	def __init__(self, *args, **kw):
		"""
		saves the current rendered frames into a video
		adds audio if box is checked
		"""
		super(RenderVideoDialog, self).__init__(*args, **kw)

		self.InitUI()
		self.SetSize((250, 160))
		self.SetTitle("Render to Video")
		self.window = None
		self.data = None
		self.px_width = None
		self.px_height = None
		self.Image_list = None

		self.timer = wx.Timer(self)

		self.Bind(wx.EVT_TIMER, self.Update, self.timer)
		self.Bind(wx.EVT_CLOSE, self.OnClose)

	def set_window(self, window):
		"""
		creates all dialog data from window base data, only the window
		is passed as future-proofing, if another variable is needed
		then it can be created anywhere else and then a single line can be added here
		"""
		self.window = window
		self.data = self.window.data
		self.px_width = self.window.renderCtrl.px_width
		self.px_height = self.window.renderCtrl.px_height

		self.xoffset = self.window.renderCtrl.xoffset
		self.yoffset = self.window.renderCtrl.yoffset
		self.canvas = self.window.renderCtrl.canvas

		self.Image_list = self.window.Image_list
		self.frames_progress.SetRange(len(self.data["Frames"]))
		self.timer.Start()

	def InitUI(self):
		#creates objects and sets layout
		self.frames_pnl = wx.Panel(self, size=(250,60))
		self.frames_render_button = wx.Button(self.frames_pnl, label="Render", pos = (0,0))
		self.frames_render_status = wx.StaticText(self.frames_pnl, label="Ready to render", pos=(110, 3))
		self.frames_progress = wx.Gauge(self.frames_pnl, range=100, pos=(10,30), size=(180, 20))

		self.frames_render_button.Bind(wx.EVT_BUTTON, self.On_frames_render_button)

		self.video_pnl = wx.Panel(self, size=(250,60))
		self.video_render_status = wx.StaticText(self.video_pnl, label="Ready to render", pos=(110, 3))
		self.video_add_audio_box = wx.CheckBox(self.video_pnl, label="Add audio", pos=(0, 30))

		self.layout_box = wx.BoxSizer(wx.VERTICAL)
		self.layout_box.Add(self.frames_pnl)
		self.layout_box.Add(self.video_pnl)
		self.SetSizer(self.layout_box)

	######### frames dialog goes here

	def gen_draw_order(self, obj_list, parent_list = [] ):
		parents = set(obj_list)
		dict_with_only_keys = {k: v for k, v in self.data["Frames"][self.data["Current Frame"]].items() if k in parents}
		#draw_order = sorted(dict_with_only_keys , key = lambda x: dict_with_only_keys[x]["Pos"][2])

		final_list = {}

		for obj in dict_with_only_keys.keys():
			final_list[obj] = [copy.deepcopy(parent_list) , dict_with_only_keys[obj]["Pos"][2]]
			children_list = self.window.data["Object List"][obj ]["Children"]
			cur_list = self.gen_draw_order(children_list, parent_list + [obj])

			for key in cur_list.keys():
				cur_list[key][1] += final_list[obj][1]

			final_list.update(cur_list)

		return final_list

	def Update(self, event):
		if self.window.rendering:
			"""
			ticks through each frame, using similar draw order and draw functions to 
			render control panel, differences exist in order to scale it up to the proper size and render to the FBO instead
			little concern is given to effeciency since the largest bottleneck is how long it takes to save to disk
			"""

			print("drawing order")

			parents = set(self.data["Parents"])
			imglist = self.gen_draw_order(parents)
			draw_order = sorted(imglist, key=lambda x: imglist[x][1])

			print("resetting canvas")			
			self.canvas.clear()
			self.canvas.Purge([self.px_width, self.px_height] )
			self.canvas.transform(self.data["Frames"][self.data["Current Frame"]]["Camera"], False)
			#when parent tranform is added to render this must be updated accordingly
			print("drawing objects")

			for obj in draw_order:
				if obj != "Camera":
					cur_obj = self.data["Frames"][self.data["Current Frame"]][obj]
					if cur_obj["Current Image"] not in ["", "none"]:
						self.Image_list[cur_obj["Current Image"]].draw(cur_obj, parent=obj, draw_origin=False, parents=imglist[obj][0])

			cur_obj = self.data["Frames"][self.data["Current Frame"]]["Camera"]
			obj = "Camera"
			if cur_obj["Current Image"] != "Camera":
				self.Image_list[ cur_obj["Current Image"]].draw(cur_obj, parent=obj, draw_origin=False )

			print("getting image")
			imgdata = self.canvas.GetImgData([self.xoffset, self.yoffset])
			fin_surf = pygame.image.fromstring(imgdata, (self.canvas.resolution[0], self.canvas.resolution[1]), "RGBA", True)
			pygame.image.save(fin_surf, self.data["Render Dir"] + "\\Frames\\{0:06}.png".format(self.data["Current Frame"]))
			print("turning off frame buffer")
			
			self.data["Current Frame"] += 1
			self.frames_progress.SetValue(self.data["Current Frame"])
		if self.window.rendering and self.data["Current Frame"] >= len(self.data["Frames"]):
			self.canvas.FrameBufferOff()
			self.Resize()
			self.RenderVideo()

	def Resize(self):
		self.window.rendering = False
		self.canvas.OnResize(1)
		self.frames_render_status.SetLabel("Render Finished <3")

	def On_frames_render_button(self, event):
		#triggers the render function, setting the render to true so that
		#associated functions in other parts of the program disengage, such as the render box
		#and the timeline control functions
		#resets the current frame and if a frames directory already exists, removes it to make room
		#for the current render
		print("button worked")
		self.window.rendering = True
		self.data["Current Frame"] = 0
		print("setting directory")
		if os.path.isdir( self.data["Render Dir"] + "\\Frames"):
			shutil.rmtree( self.data["Render Dir"] + "\\Frames")
		print("making directory")
		os.mkdir( self.data["Render Dir"] + "\\Frames")
		print("setting label")
		self.frames_render_status.SetLabel("Rendering...")
		self.canvas.FrameBufferOn()

	######### end frames dialog


	def RenderVideo(self):
		"""
		uses ffmpeg library to render video from frames
		currently output mp4 is not compatible with twitter and must be formatted
		currently no feedback is given to the program causing it to lock up during render
		both problems to be fixed in later releases
		"""
		self.video_render_status.SetLabel("Rendering...")
		if os.path.exists(self.data["Video Name"]):
			os.remove(self.data["Video Name"])
		if self.video_add_audio_box.GetValue():
			(
				ffmpeg
				.input(self.data["Render Dir"] + "/Frames/%06d.png", framerate=self.data["FPS"])
				.output(self.data["Video Name"])
				.global_args("-i", self.data["Audio"], 
					"-f", "image2",
					"-s", "%dx%d" % (self.canvas.resolution[0], self.canvas.resolution[1]),
					"-vcodec", "libx264",
					"-crf", "25",
					"-pix_fmt", "yuv420p",
					)
				.run()
			)

		else:
			(
				ffmpeg
				.input(self.data["Render Dir"] + "/Frames/%06d.png", framerate=self.data["FPS"])
				.output(self.data["Video Name"])
				.global_args(
					"-f", "image2",
					"-s", "%dx%d" % (self.canvas.resolution[0], self.canvas.resolution[1]),
					"-vcodec", "libx264",
					"-crf", "25",
					"-pix_fmt", "yuv420p")
				.run()
			)
		self.video_render_status.SetLabel("Video rendered! <3")

	def OnClose(self, event):
		self.Resize()
		self.timer.Stop()
		self.Destroy()