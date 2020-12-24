#Graphical libraries
import wx
from wx import glcanvas
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame

#built-in libraries
import copy
from datetime import datetime
import json

#constants used throughout program
from consts import *

#opengl canvas basic implmentation
from canvas_base import CanvasBase
from render_frames_dialog import RenderImgsDialog
from render_video_dialog import RenderVideoDialog
import data_default
from listener import Key_listener

loc = 704

version_name = "Monchy PT Render Control Panel Beta 1.0.1"

class RenderCtrl(wx.Panel):
	"""
	Creates an opengl context and renders all the images
	all opengl functions are confined to renderCtrl, render_frames_dialog, and OBJ2D for future updates
	the render panel is centered on the project
	"""
	def __init__(self, parent, ID, data, window, ViewPortSize, Image_list, listener):
		wx.Panel.__init__(self, parent, ID)
		#setting default data and variables
		self.data = data
		self.window = window
		self.Image_list = Image_list
		self.listener = listener #future proofing for keyboard commands in render window
		self.width, self.height = ViewPortSize
		self.ViewPortSize = ViewPortSize
		self.first_pos = 0
		self.prev_frame = 0
		self.left_mouse_click = False
		self.middle_mouse_click = False
		self.right_mouse_click = False

		#builds the panel and sets layout, binds functions to actions
		self.build()
		self.set_layout()
		self.resize_viewbox()
		self.bind_all()

	def build(self):
		#creates a red, green, and blue slider to control the background color of the canvas
		self.r_slider = wx.Slider(self, value = 1, minValue = 0, maxValue = 100, 
			style=wx.ALIGN_CENTER_VERTICAL|wx.SL_HORIZONTAL)

		self.g_slider = wx.Slider(self, value = 1, minValue = 0, maxValue = 100, 
			style=wx.ALIGN_CENTER_VERTICAL|wx.SL_HORIZONTAL)

		self.b_slider = wx.Slider(self, value = 1, minValue = 0, maxValue = 100, 
			style=wx.ALIGN_CENTER_VERTICAL|wx.SL_HORIZONTAL)

		#sets the background color according to the current value of the sliders
		self.btn1 = wx.Button(self, 1, "set")
		#the drawable opengl canvas itself, implemented as canvasbase
		self.canvas = CanvasBase(self, self.ViewPortSize, self.data)

	def bind_all(self):
		self.btn1.Bind(wx.EVT_BUTTON, self.SetBackgroundColor)

		self.canvas.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseScroll)

		self.canvas.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
		self.canvas.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)

		self.canvas.Bind(wx.EVT_RIGHT_DOWN, self.OnMouseDown)
		self.canvas.Bind(wx.EVT_RIGHT_UP, self.OnMouseUp)

		self.canvas.Bind(wx.EVT_MIDDLE_DOWN, self.OnMouseDown)
		self.canvas.Bind(wx.EVT_MIDDLE_UP, self.OnMouseUp)

		self.canvas.Bind(wx.EVT_MOTION, self.OnMouseMotion)


		self.canvas.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
		self.canvas.Bind(wx.EVT_KEY_UP, self.OnKeyUp)
		#self.window.Bind(wx.EVT_CHAR, self.OnKeyDown)
		#self.window.timelineCtrl.PP.Bind(wx.EVT_CHAR, self.OnKeyDown)

	def OnKeyDown(self, event):
		self.prev_frame = self.data["Current Frame"]
		print(event.GetKeyCode())
		self.listener.set_keydown(event.GetKeyCode())
		event.Skip()

	def OnKeyUp(self, event):
		self.prev_frame = self.data["Current Frame"]
		print(event.GetKeyCode())
		self.listener.set_keyup(event.GetKeyCode())
		event.Skip()

	def set_layout(self):
		self.color_box = wx.BoxSizer(wx.HORIZONTAL)
		self.color_box.Add(self.r_slider)
		self.color_box.Add(self.g_slider)
		self.color_box.Add(self.b_slider)
		self.color_box.Add(self.btn1)

		self.mainBox = wx.BoxSizer(wx.VERTICAL)
		self.mainBox.Add(self.color_box)
		self.mainBox.Add(self.canvas, 1, wx.EXPAND)
		self.SetSizer(self.mainBox)

	def On_set_videoname(self, event):
		#sets the name of the target video file to render to
		with wx.FileDialog(self, "Save video as", wildcard="MP4 files (*.mp4)|*.mp4",
			style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

			if fileDialog.ShowModal() == wx.ID_CANCEL:
				return

			pathname = fileDialog.GetPath()
			self.data["Video Name"] = pathname

	def On_set_working_dir(self, event):
		#sets the working directory to render all frames to
		with wx.DirDialog(self, "Choose working directory:", "",
			style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST) as dirDialog:

			if dirDialog.ShowModal() == wx.ID_CANCEL:
				return

			pathname = dirDialog.GetPath()
			self.data["Render Dir"] = pathname


	def create_menus(self):
		#builds the render menu
		#select video name
		#select working directory
		#render to frames
		#render frames to video
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
		#creates the render frames dialog box
		#if no render directory has been set asks user for one
		if self.data["Render Dir"] == "":
			self.On_set_working_dir(event)
		render_dialog = RenderImgsDialog(None)#, window = self.window)
		render_dialog.set_window(self.window)
		render_dialog.ShowModal()
		render_dialog.Destroy()

	def On_render_video(self, event):
		#if no render dir has been set asks user for one
		#if no video name has been set asks user for one
		#opens the render video dialog
		if self.data["Render Dir"] == "":
			self.On_set_working_dir(event)
		if self.data["Video Name"] == "":
			self.On_set_videoname(event)
		render_dialog = RenderVideoDialog(None)#, window = self.window)
		render_dialog.set_window(self.window)
		render_dialog.ShowModal()
		render_dialog.Destroy()

	def OnMouseScroll(self, event):
		#alters the distance from the viewport that the current object is at
		#down is closer
		#up is further away
		#divides the wheel rotation by 200 to get a small float value to alter the z axis by
		obj = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]
		obj["Dist"] -= event.GetWheelRotation()/2000
		if self.data["Object List"][self.data["Current Object"]]["Parent"] != None:
			obj["Pos"][2] = obj["Dist"] + self.data["Frames"][self.data["Current Frame"]][ self.data["Object List"][self.data["Current Object"]]["Parent"] ]["Dist"]
		else:
			obj["Pos"][2] = obj["Dist"]
			if self.data["Object List"][self.data["Current Object"]]["Children"] != []:
				for child in self.data["Object List"][self.data["Current Object"]]["Children"]:
					self.data["Frames"][self.data["Current Frame"]][ child ]["Pos"][2] = obj["Dist"] + self.data["Frames"][self.data["Current Frame"]][ child ]["Dist"]
		self.window.PushHistory()

	def set_data(self, data):
		#resets all data within the control panel in order to eitehr load a project
		#or to reset to a new project
		self.data = data
		self.canvas.set_data(self.data)
		self.canvas.set_bg(self.data["Background Color"])
		self.r_slider.SetValue(self.data["Background Color"][0]*100)
		self.g_slider.SetValue(self.data["Background Color"][1]*100)
		self.b_slider.SetValue(self.data["Background Color"][2]*100)

	def OnMouseDown(self, event):
		self.prev_frame = self.data["Current Frame"]
		#gets the origin point of the mouse as is
		#uses the distance (z pos) to calculates the opengl coordinates
		#currently hard coded to work best on programmers monitor, must be updated for general use
		#after setting the origin point the canvas captures the mouse to get future events
		if event.LeftIsDown():
			self.left_mouse_click = True
		if event.RightIsDown():
			self.right_mouse_click = True
		if event.MiddleIsDown():
			self.middle_mouse_click = True
		self.canvas.SetFocus()

		dist = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Dist"]

		width = ((dist*-1.0) * .59) + 6.0
		height = ((dist*-1.0) * .4) + 4.2

		new_x_pos = ((width*2) * (event.GetPosition()[0]/self.width)) - width
		new_y_pos = (((height*2)) * (1.0-(event.GetPosition()[1]/self.height)) - height)- (self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["ScaleY"])

		self.origin_pos = (new_x_pos, new_y_pos)
		self.first_pos = event.GetPosition()

		self.canvas.CaptureMouse()

	def OnMouseUp(self, event):
		self.left_mouse_click = False
		self.middle_mouse_click = False
		self.right_mouse_click = False
		self.canvas.ReleaseMouse()
		self.window.PushHistory()

	def OnMouseMotion(self, event):
		#when mouse is moved triggers this event
		if event.Dragging() and event.LeftIsDown():
			"""
			if mouse is dragged while left mouse button is down
			calculates the new position of the mouse and compares it to the origin from the mouse click
			add difference to the x,y position accordingly in order to get a "click and drag" effect
			by checking the posision of the mouse click according to the Z axix it avoids a parralax effect
				at different distances
			resets origin position in order to avoid a cumulative effect
			"""

			pos = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Pos"]
			dist = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Dist"]

			width = ((dist*-1.0) * .59) + 6.0
			height = ((dist*-1.0) * .4) + 4.2

			new_x_pos = ((width*2) * (event.GetPosition()[0]/self.width)) - width
			new_y_pos = (((height*2)) * (1.0-(event.GetPosition()[1]/self.height)) - height)- (self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["ScaleY"])

			pos[0] += new_x_pos - self.origin_pos[0]
			pos[1] += new_y_pos - self.origin_pos[1]

			self.origin_pos = (new_x_pos, new_y_pos)

		elif event.Dragging() and event.RightIsDown():
			"""
			if dragging and right mouse button is down alters the angle based on mouse posistion
			only checks for position in pixels on screen and treats it as a percentage of the whole screen
			from it's relative starting point, rotating the object at percent * (360*2)
			multiplies it by -1 to reverse the rotation to match the direction of the mouse motion

			"""
			percent = ((event.GetPosition()[0] - self.first_pos[0])/self.width)
			mouse_pos = int(percent * (360*2)*-1)
			self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Angle"] = mouse_pos

		elif event.Dragging() and event.MiddleIsDown():
			"""
			if dragging and middle click (mouse wheel click) then alters the scale by the relative position
			of the mouse on the screen, if current object's aspect ratio is clicked then maintains aspect ratio
			needs to be updated to a relative scale from the previous scale instead of relative to the click origin
			"""
			percent = ((event.GetPosition()[0] - self.first_pos[0])/self.width)
			mouse_pos = int(percent * (360*2)*-1)
			self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["ScaleX"] = -(mouse_pos/10)
			if self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Aspect"]:
				self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["ScaleY"] = -(mouse_pos/10)
			else:
				percent = ((event.GetPosition()[1] - self.first_pos[1])/self.height)
				mouse_pos = int(percent * (360*2)*-1)
				self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["ScaleY"] = (mouse_pos/10)

		else:
			pass


	def SetBackgroundColor(self, event):
		#gets the sliders r, g, b values. divides them by 100 to get a normal value
		#sets this as the canvas' background color
		self.canvas.set_bg((self.r_slider.GetValue()/100,self.g_slider.GetValue()/100,self.b_slider.GetValue()/100, 0.0) )
		self.data["Background Color"] = [self.r_slider.GetValue()/100,self.g_slider.GetValue()/100,self.b_slider.GetValue()/100, 0.0]

	def Reset_Canvas(self):
		#sets the canvas to the camera on the current frame's pos, scale, rot
		#giving the user full control over the camera from frame to frame
		cam = self.data["Frames"][self.data["Current Frame"]]["Camera"]
		glTranslatef(cam["Pos"][0],
					cam["Pos"][1],
					cam["Pos"][2])

		glRotatef(cam["Angle"], 0, 0, 1)
		glScalef(cam["FlipX"] * cam["ScaleX"],
				cam["FlipY"] * cam["ScaleY"], 1.0)

	def Update(self, second):
		#if self.canvas.HasFocus():
		#	if self.listener.get_struck()
		#sets the window status to the current frame
		#clears the canvas of all images
		#purge loads the identity and resets the perspective of the camera
		#canvas is then reset to the camera
		#finally everything is drawn
		if self.listener.get_struck(68): #on D
			self.window.timelineCtrl.onNext(1)
		if self.listener.get_struck(65): #on A
			self.window.timelineCtrl.onBack(1)

		if self.listener.get_struck(32):
			if self.window.timelineCtrl.isPlaying():
				self.window.timelineCtrl.onPause(1)
			else:
				self.window.timelineCtrl.onPlay(1)

		if self.listener.get_struck(306) and not self.window.timelineCtrl.isPlaying():
			self.window.timelineCtrl.onPlay(1)
		if self.listener.get_keyrel(306):
			self.window.timelineCtrl.onPause(1)

		if self.left_mouse_click:
			if self.prev_frame != self.data["Current Frame"]:
				print("change")
				self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Pos"] = copy.deepcopy(self.data["Frames"][self.prev_frame ][self.data["Current Object"]]["Pos"])
				self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Dist"] = copy.deepcopy(self.data["Frames"][self.prev_frame ][self.data["Current Object"]]["Dist"])
				self.prev_frame = self.data["Current Frame"]

		if self.right_mouse_click:
			if self.prev_frame != self.data["Current Frame"]:
				self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Angle"] = copy.deepcopy(self.data["Frames"][self.prev_frame ][self.data["Current Object"]]["Angle"])
				self.prev_frame = self.data["Current Frame"]

		if self.middle_mouse_click:
			if self.prev_frame != self.data["Current Frame"]:

				self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["ScaleX"] = copy.deepcopy(self.data["Frames"][self.prev_frame ][self.data["Current Object"]]["ScaleX"])
				self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["ScaleY"] = copy.deepcopy(self.data["Frames"][self.prev_frame ][self.data["Current Object"]]["ScaleY"])

				self.prev_frame = self.data["Current Frame"]


		self.window.Set_Fifth_Status( str(self.data["Current Frame"]))
		self.canvas.clear()
		self.canvas.Purge()
		self.Reset_Canvas()
		self.Draw()

	def resize_viewbox(self):
		#canvas resize event is handled to ensure the FBO for HD rendering is constantly up-to-date

		#height_coords are constant at 4.13
		#the size of the canvas viewport after a resize is taken in pixels
		#the ratio of the height/width is then used to determine the opengl coords of the screen width
		#the ratio of the width/height is used to get the total size of the FBO with 1080p being the base
		#once the box size is determined, the offsets are generated using the difference in size of the FBO
		#and 1080p, giving a subsection of the render viewport to save as a series of images
		#the FBO is then generated using these coordinates
		self.height_coords = 4.13
		self.width_pixels, self.height_pixels = self.canvas.ViewPortSize
		self.canvas_ratio = self.width_pixels/self.height_pixels
		self.pix_ratio = self.height_pixels/self.width_pixels
		self.width_coords = self.canvas_ratio * self.height_coords
		self.box_width = self.width_coords * .8
		self.box_height = self.box_width * .5625


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
		#a draw order list is generated by sorting using a lambda by the distance
		#returned list is composed of ints who's value is the object's position in the current frame object list

		#print(list(self.data["Object List"].keys()))

		draw_order = sorted(self.data["Frames"][self.data["Current Frame"]], key = lambda x: self.data["Frames"][self.data["Current Frame"]][x]["Pos"][2])

		#objects are drawn using the draw order, camera is ignored
		#as is any object what's current image is "none"
		#for the beta 1 the parent object will be determined by checking for
		#an object name in the obj["Parent"] string, if string = "" then no parent is used
		#if parent is present then the object's status is rendered first, giving the new object a relative status
		"""
		proposed future update:"""
		for obj in draw_order:
			if obj != "Camera":
				cur_obj = self.data["Frames"][self.data["Current Frame"]][obj]
				if cur_obj["Current Image"] not in ["", "none"]:
					if self.data["Object List"][obj]["Parent"] != None:
						parent = self.data["Frames"][self.data["Current Frame"]][self.data["Object List"][obj]["Parent"]]
					else:
						parent = None
					self.Image_list[cur_obj["Current Image"]].draw(cur_obj, parent=parent)
		"""
		This method will be replaced in B2 when modern opengl is used instead
		

		for obj in draw_order:
			if obj != "Camera":
				cur_obj = self.data["Frames"][self.data["Current Frame"]][obj]
				if cur_obj["Current Image"] not in ["", "none"]:
					self.Image_list[cur_obj["Current Image"]].draw(
						cur_obj #all data related to object stats
						)"""

		#resets convas viewbox upon resize to ensure continuity
		if self.canvas.is_resized():
			self.resize_viewbox()

		#draws a box on screen with a ratio of 1.78:1
		#outlines where the actual video will be rendered from
		if not self.window.rendering:
			glBindTexture(GL_TEXTURE_2D, 0)
			glPushMatrix()
			glLineWidth(4)
			glColor4f(0.0,1.0,0.0,1.0)

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
			glColor4f(1.0,0.0,1.0,1.0)
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

			glColor4f(1.0,1.0,1.0,1.0)
			glPopMatrix()

		#renders everything by swapping the buffers
		self.canvas.Draw()

	def OnClose(self):
		#this should probably do something
		pass

class testFrame(wx.Frame):
	def __init__(self, parent, title, size):
		wx.Frame.__init__(self,
			parent, wx.ID_ANY, title, pos=(1,1), size=size,
			style = (wx.DEFAULT_FRAME_STYLE|wx.WANTS_CHARS))

		self.listener = Key_listener()

		#sets all data to default position for a new project
		self.new_project()

		#setting up layout
		self.mainBox = wx.BoxSizer(wx.HORIZONTAL)

		#add elements and panels here to allow them to make changes to the window
		self.renderCtrl = RenderCtrl(self, wx.ID_ANY, self.data, self, (1000,700), self.Image_list, self.listener)

		#creates menus and tells all control panels to set their menus as well
		self.create_menus()

		self.set_layout()

		self.timer = wx.Timer(self)

		#sets the time the last tick took place
		#tickspeed is useful in determining if the program is running at full speed
		self.lasttick = datetime.now().second

		#####################statusbar
		self.statusbar = self.CreateStatusBar(5)
		
		#####################bindings
		self.bind_all()
		self.timer.Start()
		self.Maximize(True)

	def set_layout(self):
		#organizes layout
		"""
		===================
		| |             | |
		|1|     2       |3|
		| |_____________| |
		|_|______4______|_|

		1- objCtrl
		2- renderCtrl
		3- stateCtrl
		4- timelineCtrl

		"""
		self.center = wx.BoxSizer(wx.VERTICAL)
		self.center.Add(wx.Panel(self, size=(2000,1)))
		self.center.Add(self.renderCtrl, 1, wx.EXPAND)   #2

		self.mainBox.Add(self.center, 1, wx.EXPAND)      #2, 4

		self.SetSizer(self.mainBox)

	def bind_all(self):
		self.Bind(wx.EVT_TIMER, self.tickrate, self.timer)
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.Bind(wx.EVT_MENU, self.OnNew, self.newProj)
		self.Bind(wx.EVT_MENU, self.OnClose, self.closeWin)
		self.Bind(wx.EVT_MENU, self.LoadData, self.loadData)
		self.Bind(wx.EVT_MENU, self.SaveData, self.saveData)
		self.Bind(wx.EVT_MENU, self.SaveAsData, self.saveAsData)

		self.Bind(wx.EVT_MENU, self.On_tutorial1, self.tutorial1)
		self.Bind(wx.EVT_MENU, self.On_tutorial2, self.tutorial2)
		self.Bind(wx.EVT_MENU, self.On_tutorial3, self.tutorial3)
		self.Bind(wx.EVT_MENU, self.On_tutorial4, self.tutorial4)
		self.Bind(wx.EVT_MENU, self.On_tutorial5, self.tutorial5)
		self.Bind(wx.EVT_MENU, self.On_tutorial6, self.tutorial6)

	def create_menus(self):
		self.menubar = wx.MenuBar()
		self.fileMenu = wx.Menu()

		#creates the menu items for saving/loading the current project
		self.newProj = wx.MenuItem(self.fileMenu, wx.ID_ANY, "&New Project\tCtrl+N", 'New Project')
		self.loadData = wx.MenuItem(self.fileMenu, wx.ID_ANY, '&Load Project\tCtrl+O', 'Load Animation')
		self.saveData = wx.MenuItem(self.fileMenu, wx.ID_ANY, '&Save Project\tCtrl+S', 'Save Animation')
		self.saveAsData = wx.MenuItem(self.fileMenu, wx.ID_ANY, '&Save Project As\tShift+Ctrl+S', 'Save Animation As')

		self.fileMenu.Append(self.newProj)
		self.fileMenu.Append(self.loadData)
		self.fileMenu.Append(self.saveData)
		self.fileMenu.Append(self.saveAsData)
		self.fileMenu.AppendSeparator()

		self.closeWin = wx.MenuItem(self.fileMenu, wx.ID_EXIT, '&Quit\tCtrl+X', 'Quit Application')

		self.fileMenu.AppendSeparator()

		self.fileMenu.Append(self.closeWin)

		self.menubar.Append(self.fileMenu, '&File')

		#creates each control panel's menus in order
		#the order these are called determines how the menus are laid out
		self.renderCtrl.create_menus()

		#help menu links back to youtube tutorials on how to use the program
		self.helpMenu = wx.Menu()

		self.tutorial1 = wx.MenuItem(self.helpMenu, wx.ID_ANY, "&About All")
		self.tutorial2 = wx.MenuItem(self.helpMenu, wx.ID_ANY, "&About Objects")
		self.tutorial3 = wx.MenuItem(self.helpMenu, wx.ID_ANY, "&About Timeline")
		self.tutorial4 = wx.MenuItem(self.helpMenu, wx.ID_ANY, "&About Renderer")
		self.tutorial5 = wx.MenuItem(self.helpMenu, wx.ID_ANY, "&About States")
		self.tutorial6 = wx.MenuItem(self.helpMenu, wx.ID_ANY, "&About Creating Video")

		self.helpMenu.Append(self.tutorial1)
		self.helpMenu.Append(self.tutorial2)
		self.helpMenu.Append(self.tutorial3)
		self.helpMenu.Append(self.tutorial4)
		self.helpMenu.Append(self.tutorial5)
		self.helpMenu.Append(self.tutorial6)

		self.menubar.Append(self.helpMenu, "&Help")

		self.SetMenuBar(self.menubar)


		#opens to a playlist on youtube containing the tutorials for use
		#could probably be turned into a single function
	def On_tutorial1(self, event):
		webbrowser.open("https://www.youtube.com/watch?v=oBAQy1D5r7o&list=PLkVdGBkhsW-WdYoTn-Uf8SouWUh3vGnGO&index=1")

	def On_tutorial2(self, event):
		webbrowser.open("https://www.youtube.com/watch?v=5L98weJKd48&list=PLkVdGBkhsW-WdYoTn-Uf8SouWUh3vGnGO&index=2")

	def On_tutorial3(self, event):
		webbrowser.open("https://www.youtube.com/watch?v=Sm7fqqMC0Ks&list=PLkVdGBkhsW-WdYoTn-Uf8SouWUh3vGnGO&index=3")

	def On_tutorial4(self, event):
		webbrowser.open("https://www.youtube.com/watch?v=ar9PjawB-qs&list=PLkVdGBkhsW-WdYoTn-Uf8SouWUh3vGnGO&index=4")

	def On_tutorial5(self, event):
		webbrowser.open("https://www.youtube.com/watch?v=rqVycueA8Tg&list=PLkVdGBkhsW-WdYoTn-Uf8SouWUh3vGnGO&index=5")

	def On_tutorial6(self, event):
		webbrowser.open("https://www.youtube.com/watch?v=15ymfD67Qbk&list=PLkVdGBkhsW-WdYoTn-Uf8SouWUh3vGnGO&index=6")

	def tickrate(self, event):
		"""
		monitors the tickrate of the software
		allows it to run at max speed, capped by the vsync rate
		every second it sets the current tickrate to monitor the proccessing speed of the program
		sends True signal to the control panels update function once per second
		current time is time since Jan 1, 1970
		"""
		current_time = (datetime.now()-datetime(1970,1,1)).total_seconds()
		if (current_time - self.lasttick) >= 1:
			self.Set_Third_Status(str(self.ticks) )
			self.lasttick = current_time
			self.ticks = 0
			self.renderCtrl.Update(True)
		else:
			self.ticks += 1
			self.renderCtrl.Update(False)

		#statusbar set functions, to be compressed into single function "Set_Status"
	def Set_First_Status(self, text):
		self.Set_Status(0, text)

	def Set_Second_Status(self, text):
		self.Set_Status(1, text)

	def Set_Third_Status(self, text):
		self.Set_Status(2, text)

	def Set_Forth_Status(self, text):
		self.Set_Status(3, text)

	def Set_Fifth_Status(self, text):
		self.Set_Status(4, text)

	def Set_Status(self, bar, text):
		self.statusbar.SetStatusText( text, bar)

	def LoadData(self, event):
		"""
		self.data is loaded from a json file named *.ani (short for animate)
		load data selects a file with a file dialog and loads it as self.data
		then it calls self.set_data(), which loads all the images, audio, and settings from the file
		title of the animation is added to the window title

		OnNew offers to save the current project if anything has been added
		after it calls new_project to wipe everything clean
		"""
		with wx.FileDialog(self, "Load Animation", wildcard="ANI files (*.ani)|*.ani",
							style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
			if fileDialog.ShowModal() == wx.ID_CANCEL:
				return

			pathname = fileDialog.GetPath()
			tempData = open(pathname, "r")
			self.data = json.loads(tempData.read())
			tempData.close()
			self.set_data()
			self.pathname = pathname
			self.SetTitle("%s (%s)".format(version_name,  self.pathname.split("\\")[-1].split(".")[0]))

	def OnNew(self):
		if len(self.data["Object List"]) > 1 or self.data["Audio"] != "":
			self.SaveAsData(1)
		self.new_project()

	def new_project(self):
		#sets the animation state data into default, for more details see data_default.py
		self.data = copy.deepcopy(data_default.data)

		#dict, holds all images as opengl textures "image name":obj2d
		self.Image_list = {}
		#holds current file path to save and load the animation
		self.pathname = ""
		#signals to certain functions that the video is being rendered to disable audio syncing
		self.rendering = False
		self.ticks = 0
		#clears the project name
		self.SetTitle(version_name)
		try:
			self.set_data()
		except:
			pass

	def set_data(self):
		#calls every control panel to load the new data
		self.renderCtrl.set_data(self.data)

	def SaveAsData(self, event):
		with wx.FileDialog(self, "Save animation", wildcard="ANI files (*.ani)|*.ani",
			style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

			if fileDialog.ShowModal() == wx.ID_CANCEL:
				return

			pathname = fileDialog.GetPath()
			self.writeData(pathname)

	def SaveData(self, event):
		if self.pathname != "":
			self.writeData(self.pathname)			
		else:
			self.SaveAsData(event)

	def writeData(self, pathname):
		try:
			with open(pathname, 'w') as file:
				file.write(json.dumps(self.data))
		except IOError:
			wx.LogError("Cannot save current data in file %s" % pathname)
		self.pathname = pathname
		self.SetTitle("%s (%s)".format(version_name,  self.pathname.split("\\")[-1].split(".")[0]))

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