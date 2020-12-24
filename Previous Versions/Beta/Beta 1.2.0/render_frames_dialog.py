#Graphical Libraries
import wx
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame

#other built-in libraries
import os
import shutil

#constants to use throughout the program
from consts import *
#canvasbase to render frames to images
from canvas_base import CanvasBase

loc = 136

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
		self.progress.SetRange(len(self.data["Frames"]))
		self.timer.Start()

	def InitUI(self):
		#creates objects and sets layout
		self.pnl = wx.Panel(self, size=(250,200))
		self.render_button = wx.Button(self.pnl, label="Render", pos = (0,0))
		self.render_status = wx.StaticText(self.pnl, label="Ready to render", pos=(110, 3))
		self.progress = wx.Gauge(self.pnl, range=100, pos=(10,30), size=(180, 20))

		self.render_button.Bind(wx.EVT_BUTTON, self.On_render_button)

	def Purge(self):
		#based on canvasbase purge, resets identity and perspective in order to
		#render to the FBO at the correct perspective and scale
		glLoadIdentity()
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		gluPerspective(45, (self.px_width/ self.px_height), 0.1, 50.0 )
		glTranslatef(0.0,0.0,-10)

	def Reset_Canvas(self):
		#resets canvas to the current camera transform
		cam = self.data["Frames"][self.data["Current Frame"]]["Camera"]
		glTranslatef(cam["Pos"][0],
					cam["Pos"][1],
					cam["Pos"][2])

		glRotatef(cam["Angle"], 0, 0, 1)
		glScalef(cam["FlipX"] * cam["ScaleX"],
				cam["FlipY"] * cam["ScaleY"], 1.0)

	def Update(self, event):
		if self.window.rendering:
			"""
			ticks through each frame, using similar draw order and draw functions to 
			render control panel, differences exist in order to scale it up to the proper size and render to the FBO instead
			little concern is given to effeciency since the largest bottleneck is how long it takes to save to disk
			"""
			draw_order = sorted(self.data["Frames"][self.data["Current Frame"]], key = lambda x: self.data["Frames"][self.data["Current Frame"]][x]["Pos"][2])
			glBindFramebuffer(GL_FRAMEBUFFER, self.FBO)
			glViewport(0,0,self.px_width, self.px_height)
			self.Purge()
			self.Reset_Canvas()
			#when parent tranform is added to render this must be updated accordingly
			for obj in draw_order:
				if obj != "Camera":
					cur_obj = self.data["Frames"][self.data["Current Frame"]][obj]
					if cur_obj["Current Image"] not in ["", "none"]:
						self.Image_list[cur_obj["Current Image"]].draw(
							cur_obj #all data related to object stats
							)

			#turns FBO render into a string of pixel data, at the offset + 1080p
			#converts that into a pygame surface
			#saves that image to a rendered frame on disk
			#pygame is used here because in future versions it can be used to smooth the video for reduced pixelation
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
		#triggers the render function, setting the render to true so that
		#associated functions in other parts of the program disengage, such as the render box
		#and the timeline control functions
		#resets the current frame and if a frames directory already exists, removes it to make room
		#for the current render
		self.window.rendering = True
		self.data["Current Frame"] = 0
		if os.path.isdir( self.data["Render Dir"] + "/Frames"):
			shutil.rmtree( self.data["Render Dir"] + "/Frames")
		os.mkdir( self.data["Render Dir"] + "/Frames")
		self.render_status.SetLabel("Rendering...")

	def OnClose(self, event):
		self.Destroy()
