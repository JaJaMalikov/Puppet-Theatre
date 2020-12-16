import wx
import os
import copy

import ffmpeg

from wx import glcanvas

from OpenGL.GL import *
from OpenGL.GLU import *

import OpenGL.GL.shaders
from pyrr import Matrix44

from datetime import datetime
import pygame

import json

import numpy

from consts import *
import time

from CanvasBase import CanvasBase

import shutil

class RenderVideoDialog(wx.Dialog):
	def __init__(self, *args, **kw):
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
		self.render_status.SetLabel("Rendering...")
		if os.path.exists(self.data["video name"]):
			os.remove(self.data["video name"])
		if self.add_audio_box.GetValue():
			(
				ffmpeg
				.input(self.data["Render Dir"] + "/Frames/%06d.png", framerate=self.data["fps"])
				.output(self.data["video name"])
				.global_args("-i", self.data["audio"])
				.run()
			)
		else:
			(
				ffmpeg
				.input(self.data["Render Dir"] + "/Frames/%06d.png", framerate=self.data["fps"])
				.output(self.data["video name"])
				.run()
			)
		self.render_status.SetLabel("Video rendered! <3")

	def OnClose(self, event):
		self.Destroy()

class RenderImgsDialog(wx.Dialog):
	def __init__(self, *args, **kw):
		super(RenderImgsDialog, self).__init__(*args, **kw)

		self.InitUI()
		self.SetSize((250, 200))
		self.SetTitle("Render Frames to Images")
		self.window = None
		self.data = None
		self.FBO = None
		self.px_width = None
		self.px_height = None
		self.Image_list = None

		self.timer = wx.Timer(self)

		self.Bind(wx.EVT_TIMER, self.Update, self.timer)

	def set_window(self, window):
		self.window = window
		self.data = self.window.data
		self.FBO = self.window.renderCtrl.FBO
		self.px_width = self.window.renderCtrl.px_width
		self.px_height = self.window.renderCtrl.px_height

		self.xoffset = self.window.renderCtrl.xoffset
		self.yoffset = self.window.renderCtrl.yoffset
		self.canvas = self.window.renderCtrl.canvas

		self.Image_list = self.window.Image_list
		self.progress.SetRange(len(self.data["Frames"]))
		self.timer.Start()

	def InitUI(self):
		self.pnl = wx.Panel(self, size=(250,200))
		self.render_button = wx.Button(self.pnl, label="Render", pos = (0,0))
		self.render_status = wx.StaticText(self.pnl, label="Ready to render", pos=(110, 3))
		self.progress = wx.Gauge(self.pnl, range=100, pos=(10,30), size=(180, 20))

		self.render_button.Bind(wx.EVT_BUTTON, self.On_render_button)

	def Purge(self):
		glLoadIdentity()
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		gluPerspective(45, (self.px_width/ self.px_height), 0.1, 50.0 )
		glTranslatef(0.0,0.0,-10)

	def Reset_Canvas(self):
		cam = self.data["Frames"][self.data["Current Frame"]]["Camera"]
		glTranslatef(cam["pos"][0],
					cam["pos"][1],
					cam["pos"][2])

		glRotatef(cam["angle"], 0, 0, 1)
		glScalef(cam["flipX"] * cam["scaleX"],
				cam["flipY"] * cam["scaleY"], 1.0)

	def Update(self, event):
		if self.window.rendering:
			draw_order = sorted(self.data["Frames"][self.data["Current Frame"]], key = lambda x: self.data["Frames"][self.data["Current Frame"]][x]["pos"][2])
			glBindFramebuffer(GL_FRAMEBUFFER, self.FBO)
			glViewport(0,0,self.px_width, self.px_height)
			self.Purge()
			self.Reset_Canvas()
			for obj in draw_order:
				if obj != "Camera":
					cur_obj = self.data["Frames"][self.data["Current Frame"]][obj]
					if cur_obj["Current Image"] not in ["", "none"]:
						self.Image_list[cur_obj["Current Image"]].draw(
							cur_obj #all data related to object stats
							)

			imgdata = glReadPixels(self.xoffset,self.yoffset,1920, 1080, GL_RGBA, GL_UNSIGNED_BYTE)
			fin_surf = pygame.image.fromstring(imgdata, (1920, 1080), "RGBA", True)
			pygame.image.save(fin_surf, self.data["Render Dir"] + "/Frames/{0:06}.png".format(self.data["Current Frame"]))
			glBindFramebuffer(GL_FRAMEBUFFER, 0)

			self.data["Current Frame"] += 1
			self.progress.SetValue(self.data["Current Frame"])
		if self.data["Current Frame"] >= len(self.data["Frames"]):
			self.window.rendering = False
			self.canvas.OnResize(1)
			self.render_status.SetLabel("Render Finished <3")


	def On_render_button(self, event):
		self.window.rendering = True
		self.data["Current Frame"] = 0
		if os.path.isdir( self.data["Render Dir"] + "/Frames"):
			shutil.rmtree( self.data["Render Dir"] + "/Frames")
		os.mkdir( self.data["Render Dir"] + "/Frames")
		self.render_status.SetLabel("Rendering...")

	def OnClose(self, event):
		self.Destroy()

class RenderCtrl(wx.Panel):
	def __init__(self, parent, ID, data, window, ViewPortSize, Image_list, listener):
		wx.Panel.__init__(self, parent, ID)
		self.data = data
		self.window = window
		self.Image_list = Image_list
		self.listener = listener
		self.frame = 0
		self.keys_down = [False]*512
		self.width, self.height = ViewPortSize
		self.first_pos = 0

		self.r_slider = wx.Slider(self, value = 1, minValue = 0, maxValue = 100, 
			style=wx.ALIGN_CENTER_VERTICAL|wx.SL_HORIZONTAL)

		self.g_slider = wx.Slider(self, value = 1, minValue = 0, maxValue = 100, 
			style=wx.ALIGN_CENTER_VERTICAL|wx.SL_HORIZONTAL)

		self.b_slider = wx.Slider(self, value = 1, minValue = 0, maxValue = 100, 
			style=wx.ALIGN_CENTER_VERTICAL|wx.SL_HORIZONTAL)

		self.btn1 = wx.Button(self, 1, "set")

		self.color_box = wx.BoxSizer(wx.HORIZONTAL)
		self.color_box.Add(self.r_slider)
		self.color_box.Add(self.g_slider)
		self.color_box.Add(self.b_slider)
		self.color_box.Add(self.btn1)
		self.canvas = CanvasBase(self, ViewPortSize, self.data)

		self.mainBox = wx.BoxSizer(wx.VERTICAL)
		self.mainBox.Add(self.color_box)
		self.mainBox.Add(self.canvas, 1, wx.EXPAND)
		self.SetSizer(self.mainBox)

		self.resize_viewbox()

		self.btn1.Bind(wx.EVT_BUTTON, self.SetBackgroundColor)

		self.canvas.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseScroll)

		self.canvas.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
		self.canvas.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)

		self.canvas.Bind(wx.EVT_RIGHT_DOWN, self.OnMouseDown)
		self.canvas.Bind(wx.EVT_RIGHT_UP, self.OnMouseUp)

		self.canvas.Bind(wx.EVT_MIDDLE_DOWN, self.OnMouseDown)
		self.canvas.Bind(wx.EVT_MIDDLE_UP, self.OnMouseUp)

		self.canvas.Bind(wx.EVT_MOTION, self.OnMouseMotion)

	def On_set_videoname(self, event):
		with wx.FileDialog(self, "Save video as", wildcard="MP4 files (*.mp4)|*.mp4",
			style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

			if fileDialog.ShowModal() == wx.ID_CANCEL:
				return

			pathname = fileDialog.GetPath()
			self.data["video name"] = pathname

	def On_set_working_dir(self, event):
		with wx.DirDialog(self, "Choose working directory:", "",
			style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST) as dirDialog:

			if dirDialog.ShowModal() == wx.ID_CANCEL:
				return

			pathname = dirDialog.GetPath()
			self.data["Render Dir"] = pathname


	def create_menus(self):
		self.renderMenu = wx.Menu()

		self.set_videoname = wx.MenuItem(self.renderMenu, wx.ID_ANY, "&Video name", "Choose name for output video")
		self.renderMenu.Append(self.set_videoname)

		self.set_working_dir = wx.MenuItem(self.renderMenu, wx.ID_ANY, "&Choose Directory", "Choose output directory")
		self.renderMenu.Append(self.set_working_dir)

		self.render_imgs = wx.MenuItem(self.renderMenu, wx.ID_ANY, "&Render Frames", "Render project as frames")
		self.renderMenu.Append(self.render_imgs)

		self.render_video = wx.MenuItem(self.renderMenu, wx.ID_ANY, "&Render Video", "Render frames as video")
		self.renderMenu.Append(self.render_video)

		self.window.menubar.Append(self.renderMenu, '&Render')

		self.window.Bind(wx.EVT_MENU, self.On_render_imgs, self.render_imgs)
		self.window.Bind(wx.EVT_MENU, self.On_render_video, self.render_video)

		self.window.Bind(wx.EVT_MENU, self.On_set_videoname, self.set_videoname)
		self.window.Bind(wx.EVT_MENU, self.On_set_working_dir, self.set_working_dir)

	def On_render_imgs(self, event):
		if self.data["Render Dir"] == "":
			self.On_set_working_dir(event)
		render_dialog = RenderImgsDialog(None)#, window = self.window)
		render_dialog.set_window(self.window)
		render_dialog.ShowModal()
		render_dialog.Destroy()

	def On_render_video(self, event):
		print(self.data["video name"])
		if self.data["Render Dir"] == "":
			self.On_set_working_dir(event)
		if self.data["video name"] == "":
			self.On_set_videoname(event)
		render_dialog = RenderVideoDialog(None)#, window = self.window)
		render_dialog.set_window(self.window)
		render_dialog.ShowModal()
		render_dialog.Destroy()

	def OnMouseScroll(self, event):
		self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["pos"][2] -= event.GetWheelRotation()/200

	def set_data(self, data):
		self.data = data
		self.canvas.set_data(self.data)
		self.canvas.set_bg(self.data["Background Color"])
		self.r_slider.SetValue(self.data["Background Color"][0]*100)
		self.g_slider.SetValue(self.data["Background Color"][1]*100)
		self.b_slider.SetValue(self.data["Background Color"][2]*100)

	def OnMouseDown(self, event):
		dist = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["pos"][2]

		width = ((dist*-1.0) * .59) + 6.0
		height = ((dist*-1.0) * .4) + 4.2

		new_x_pos = ((width*2) * (event.GetPosition()[0]/self.width)) - width
		new_y_pos = (((height*2)) * (1.0-(event.GetPosition()[1]/self.height)) - height)- (self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["scaleY"])

		self.origin_pos = (new_x_pos, new_y_pos)
		self.first_pos = event.GetPosition()

		self.canvas.CaptureMouse()

	def OnMouseUp(self, event):
		self.canvas.ReleaseMouse()

	def OnMouseMotion(self, event):
		if event.Dragging() and event.LeftIsDown():
			dist = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["pos"][2]

			width = ((dist*-1.0) * .59) + 6.0
			height = ((dist*-1.0) * .4) + 4.2

			new_x_pos = ((width*2) * (event.GetPosition()[0]/self.width)) - width
			new_y_pos = (((height*2)) * (1.0-(event.GetPosition()[1]/self.height)) - height)- (self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["scaleY"])

			self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["pos"][0] += new_x_pos - self.origin_pos[0]
			self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["pos"][1] += new_y_pos - self.origin_pos[1]

			self.origin_pos = (new_x_pos, new_y_pos)

		elif event.Dragging() and event.RightIsDown():
			percent = ((event.GetPosition()[0] - self.first_pos[0])/self.width)
			mouse_pos = int(percent * (360*2)*-1)
			self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["angle"] = mouse_pos

		elif event.Dragging() and event.MiddleIsDown():
			percent = ((event.GetPosition()[0] - self.first_pos[0])/self.width)
			mouse_pos = int(percent * (360*2)*-1)
			self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["scaleX"] = -(mouse_pos/10)
			if self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Aspect"]:
				self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["scaleY"] = -(mouse_pos/10)
			else:
				percent = ((event.GetPosition()[1] - self.first_pos[1])/self.height)
				mouse_pos = int(percent * (360*2)*-1)
				self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["scaleY"] = (mouse_pos/10)

		else:
			pass


	def SetBackgroundColor(self, event):
		self.canvas.set_bg((self.r_slider.GetValue()/100,self.g_slider.GetValue()/100,self.b_slider.GetValue()/100, 0.0) )
		self.data["Background Color"] = [self.r_slider.GetValue()/100,self.g_slider.GetValue()/100,self.b_slider.GetValue()/100, 0.0]

	def set_Frame(self, frame):
		self.frame = frame

	def Reset_Canvas(self):
		cam = self.data["Frames"][self.data["Current Frame"]]["Camera"]
		glTranslatef(cam["pos"][0],
					cam["pos"][1],
					cam["pos"][2])

		glRotatef(cam["angle"], 0, 0, 1)
		glScalef(cam["flipX"] * cam["scaleX"],
				cam["flipY"] * cam["scaleY"], 1.0)

	def Update(self, second):
		"""
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				print("pressed")
				self.listener.set_keydown(event.key)
			elif event.type == pygame.KEYUP:
				self.listener.set_keyup(event.key)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				self.listener.set_mouse_down(event.button)
			elif event.type == pygame.MOUSEBUTTONUP:
				self.listener.set_mouse_up(event.button)
			else:
				pass"""


		self.window.Set_Fifth_Status( str(self.data["Current Frame"]))
		self.canvas.clear()
		self.canvas.Purge()
		self.Reset_Canvas()
		self.Draw()

	def resize_viewbox(self):
		self.height_coords = 4.13
		self.width_pixels, self.height_pixels = self.canvas.ViewPortSize
		self.canvas_ratio = self.width_pixels/self.height_pixels
		self.pix_ratio = self.height_pixels/self.width_pixels
		self.width_coords = self.canvas_ratio * self.height_coords
		self.box_width = self.width_coords * .8
		self.box_height = self.box_width * .5625

		print(self.width_pixels, self.height_pixels)

		self.px_ratio = self.height_pixels / self.width_pixels

		self.px_width = int(1920 * 1.25)
		self.px_height = int(self.px_width * self.px_ratio)

		self.xoffset = int((self.px_width * .2) / 2)
		self.yoffset = int((self.px_height * (1-(1080/self.px_height) )/2 ))

		plane_texture = glGenTextures(1)
		glBindTexture(GL_TEXTURE_2D, plane_texture)

		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.px_width, self.px_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, None)
		glBindTexture(GL_TEXTURE_2D, 0)

		self.FBO = glGenFramebuffers(1)
		glBindFramebuffer(GL_FRAMEBUFFER, self.FBO)
		glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, plane_texture, 0)
		glBindFramebuffer(GL_FRAMEBUFFER, 0)

	def Draw(self):
		#draw all objects here

		draw_order = sorted(self.data["Frames"][self.data["Current Frame"]], key = lambda x: self.data["Frames"][self.data["Current Frame"]][x]["pos"][2])

		#for obj in draw_order:
		#	if self.data["Frames"][self.data["Current Frame"]][obj][]

		for obj in draw_order:
			if obj != "Camera":
				cur_obj = self.data["Frames"][self.data["Current Frame"]][obj]
				if cur_obj["Current Image"] not in ["", "none"]:
					self.Image_list[cur_obj["Current Image"]].draw(
						cur_obj #all data related to object stats
						)

		if self.canvas.is_resized():
			self.resize_viewbox()

		#1.78:1
		if not self.window.rendering:
			glLineWidth(4)
			glColor3f(0.0,1.0,0.0)
			inData = self.data["Frames"][self.data["Current Frame"]]["Camera"]

			self.canvas.Purge()

			glBegin(GL_LINE_LOOP)

			glVertex3f(-self.box_width, 
				self.box_height, 0.0)
			glVertex3f(self.box_width, 
				self.box_height, 0.0)
			glVertex3f(self.box_width, 
				-self.box_height, 0.0)
			glVertex3f(-self.box_width, 
				-self.box_height, 0.0)

			glEnd()

			glLineWidth(2)
			glColor3f(1.0,0.0,1.0)
			glBegin(GL_LINE_LOOP)

			glVertex3f(-self.box_width, 
				self.box_height, 0.0)
			glVertex3f(self.box_width, 
				self.box_height, 0.0)
			glVertex3f(self.box_width, 
				-self.box_height, 0.0)
			glVertex3f(-self.box_width, 
				-self.box_height, 0.0)


			glEnd()

			glColor3f(1.0,1.0,1.0)

		self.canvas.Draw()

	def OnClose(self):
		pass

class testFrame(wx.Frame):
	def __init__(self, parent, title, size):
		wx.Frame.__init__(self,
			parent, wx.ID_ANY, title, pos=(1,1), size=size,
			style = (wx.DEFAULT_FRAME_STYLE|wx.WANTS_CHARS|wx.FULL_REPAINT_ON_RESIZE))


		self.data = {}

		self.data["Object List"] = {"Camera":{"Images":["Camera"]}}
		self.data["Background Color"] = [0.0,0.0,0.0,0.0]
		self.data["Current Frame"] = 0
		self.data["Current Object"] = ""
		self.data["imgs"] = []
		self.data["image list"] = []
		self.data["selection"] = 0
		self.data["fps"] = 24
		self.data["audio"] = ""
		self.data["Current State"] = "position"
		self.data["Frames"] = []
		self.data["Frames"].append(
				{
				"Camera":{
					"Current Image": "Camera",
					"pos":[0,0,0],
					"scaleX":1,
					"scaleY":1,
					"angle":0,
					"flipX":1.0,
					"flipY":1.0,
					"visible":True,
					"keyframe":False
					}
				}
			)
		self.Image_list = {}

		mainBox = wx.BoxSizer(wx.HORIZONTAL)


		self.menubar = wx.MenuBar()
		self.fileMenu = wx.Menu()

		#add elements and panels here to allow them to make changes to the window
		self.renderCtrl = RenderCtrl(self, wx.ID_ANY, self.data, self, (1000,700), self.Image_list)

		self.loadData = self.fileMenu.Append(wx.ID_ANY, 'Load', 'Load Animation')
		self.closeWin = self.fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit Application')

		self.menubar.Append(self.fileMenu, '&File')
		self.SetMenuBar(self.menubar)

		#####################panel list

		mainBox.Add(self.renderCtrl, 1, wx.EXPAND)
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
		self.renderCtrl.set_Frame(self.frames/10)
		self.renderCtrl.Update()
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
	import pygame
	w,h = 10,10
	screen = pygame.display.set_mode((w,h))

	app = wx.App()
	view = testFrame(parent=None, title='Finger Pupper Theatre', size=(1500,700))
	view.Show()
	app.MainLoop()