#Graphical libraries
import wx
import pygame

#built-in libraries
import copy
from datetime import datetime
import json

#constants used throughout program
from consts import *

#opengl canvas basic implmentation
from canvas_base import CanvasBase
from render_video_dialog import RenderVideoDialog
import data_default
from listener import Key_listener

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
		self.changed = False
		self.draw_origin = False

		self.resolutions = {
			"8K":[8192,4320],
			"4K":[4096,2160],
			"1080p":[1920,1080],
			"720p":[1280,720],
			"VGA":[640,480],

			"8Kp":[4320,8192],
			"4Kp":[2160,4096],
			"1080pp":[1080,1920],
			"720pp":[720,1280],
			"VGAp":[480,640],
			}

		#builds the panel and sets layout, binds functions to actions
		self.build()
		self.set_layout()
		self.resize_viewbox()
		self.bind_all()

	def build(self):
		self.mainBook = wx.Notebook(self)
		self.canvasPage = wx.Panel(self.mainBook, wx.ID_ANY)
		self.settingPage = wx.Panel(self.mainBook, wx.ID_ANY)

		#creates a red, green, and blue slider to control the background color of the canvas
		self.r_slider = wx.Slider(self.settingPage, value = 0, minValue = 0, maxValue = 100, 
			style=wx.ALIGN_CENTER_VERTICAL|wx.SL_HORIZONTAL, size=(300,25))

		self.g_slider = wx.Slider(self.settingPage, value = 0, minValue = 0, maxValue = 100, 
			style=wx.ALIGN_CENTER_VERTICAL|wx.SL_HORIZONTAL, size=(300,25))

		self.b_slider = wx.Slider(self.settingPage, value = 0, minValue = 0, maxValue = 100, 
			style=wx.ALIGN_CENTER_VERTICAL|wx.SL_HORIZONTAL, size=(300,25))

		self.r_textbox = wx.TextCtrl(self.settingPage, value="0", style=wx.TE_PROCESS_ENTER)
		self.g_textbox = wx.TextCtrl(self.settingPage, value="0", style=wx.TE_PROCESS_ENTER)
		self.b_textbox = wx.TextCtrl(self.settingPage, value="0", style=wx.TE_PROCESS_ENTER)

		#sets the background color according to the current value of the sliders
		self.btn1 = wx.Button(self.settingPage, 1, "set")
		#the drawable opengl canvas itself, implemented as canvasbase
		self.canvas = CanvasBase(self.canvasPage, self.ViewPortSize, self.data)

		self.res_selector = wx.ComboBox(self.settingPage, style=wx.CB_DROPDOWN, choices=list(self.resolutions.keys()))
		self.res_selector.SetValue("1080p")

		self.angle_selector = wx.Slider(self.settingPage, value=45, minValue=10, maxValue=180,
			style=wx.ALIGN_CENTER_VERTICAL|wx.SL_HORIZONTAL|wx.SL_LABELS)

		self.canvas.set_resolution(self.resolutions["1080p"])

		self.res_button = wx.Button(self.settingPage, 1, "Change Resolution")

	def bind_all(self):
		self.r_slider.Bind(wx.EVT_SLIDER, self.OnColorSlide)
		self.g_slider.Bind(wx.EVT_SLIDER, self.OnColorSlide)
		self.b_slider.Bind(wx.EVT_SLIDER, self.OnColorSlide)

		self.btn1.Bind(wx.EVT_BUTTON, self.SetBackgroundColor)
		self.res_button.Bind(wx.EVT_BUTTON, self.OnRes_button)

		self.canvas.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseScroll)

		self.canvas.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
		self.canvas.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)

		self.canvas.Bind(wx.EVT_RIGHT_DOWN, self.OnMouseDown)
		self.canvas.Bind(wx.EVT_RIGHT_UP, self.OnMouseUp)

		self.canvas.Bind(wx.EVT_MIDDLE_DOWN, self.OnMouseDown)
		self.canvas.Bind(wx.EVT_MIDDLE_UP, self.OnMouseUp)

		self.canvas.Bind(wx.EVT_MOTION, self.OnMouseMotion)

		self.angle_selector.Bind(wx.EVT_SLIDER, self.OnAngleChange)

		self.canvas.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
		self.canvas.Bind(wx.EVT_KEY_UP, self.OnKeyUp)
		#self.window.Bind(wx.EVT_CHAR, self.OnKeyDown)
		#self.window.timelineCtrl.PP.Bind(wx.EVT_CHAR, self.OnKeyDown)

		self.r_textbox.Bind(wx.EVT_TEXT_ENTER, self.OnTextColor)
		self.g_textbox.Bind(wx.EVT_TEXT_ENTER, self.OnTextColor)
		self.b_textbox.Bind(wx.EVT_TEXT_ENTER, self.OnTextColor)

	def OnAngleChange(self, event):
		self.canvas.set_view_angle(self.angle_selector.GetValue())
		self.window.PushHistory()

	def OnRes_button(self, event):
		self.canvas.set_resolution(self.resolutions[self.res_selector.GetStringSelection()])
		self.resize_viewbox()

	def OnTextColor(self, event):
		print("hit enter")
		self.r_slider.SetValue(int(int(self.r_textbox.GetValue())/2.55))
		self.g_slider.SetValue(int(int(self.g_textbox.GetValue())/2.55))
		self.b_slider.SetValue(int(int(self.b_textbox.GetValue())/2.55))

	def OnColorSlide(self, event):
		#multiply slider value by 3.65 to get rgb
		self.r_textbox.SetValue(str(int(self.r_slider.GetValue()*2.555)))
		self.g_textbox.SetValue(str(int(self.g_slider.GetValue()*2.555)))
		self.b_textbox.SetValue(str(int(self.b_slider.GetValue()*2.555)))

	def OnKeyDown(self, event):
		self.prev_frame = self.data["Current Frame"]
		self.listener.set_keydown(event.GetKeyCode())
		event.Skip()

	def OnKeyUp(self, event):
		self.prev_frame = self.data["Current Frame"]
		self.listener.set_keyup(event.GetKeyCode())
		event.Skip()

	def set_layout(self):

		self.color_box = wx.BoxSizer(wx.VERTICAL)

		self.color_box.Add(self.r_slider)
		self.color_box.Add(self.g_slider)
		self.color_box.Add(self.b_slider)
		self.color_box.Add(self.btn1)

		self.color_box.Add(self.res_selector)
		self.color_box.Add(self.res_button)

		self.color_box.Add(self.angle_selector)

		self.text_box = wx.BoxSizer(wx.VERTICAL)
		self.text_box.Add(self.r_textbox)
		self.text_box.Add(self.g_textbox)
		self.text_box.Add(self.b_textbox)

		self.settingbox = wx.BoxSizer(wx.HORIZONTAL)

		self.settingbox.Add(self.color_box)
		self.settingbox.Add(self.text_box)

		self.settingPage.SetSizer(self.settingbox)

		self.canvasBox = wx.BoxSizer(wx.VERTICAL)
		self.canvasBox.Add(self.canvas, 1, wx.EXPAND)
		self.canvasPage.SetSizer(self.canvasBox)

		self.mainBook.AddPage(self.canvasPage, "Canvas")
		self.mainBook.AddPage(self.settingPage, "Settings")

		self.mainBox = wx.BoxSizer(wx.HORIZONTAL)
		self.mainBox.Add(self.mainBook, 4, wx.EXPAND)
		self.SetSizer(self.mainBox)

	def On_set_videoname(self, event):
		#sets the name of the target video file to render to
		with wx.FileDialog(self, "Save video as", wildcard="MP4 files (*.mp4)|*.mp4",
			style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

			if fileDialog.ShowModal() == wx.ID_CANCEL:
				return

                        pathname = fileDialog.GetPath()
                        self.data["Video Name"] = pathname
                        import os
                        self.data["Render Dir"] = os.path.dirname(pathname)

	def create_menus(self):
		#builds the render menu
		#select video name
		#select working directory
		#render to frames
		#render frames to video
		self.renderMenu = wx.Menu()

		self.set_videoname = wx.MenuItem(self.renderMenu, wx.ID_ANY, "&Video name", "Choose name for output video")
		self.renderMenu.Append(self.set_videoname)

		self.render_video = wx.MenuItem(self.renderMenu, wx.ID_ANY, "&Render Video", "Render frames as video")
		self.renderMenu.Append(self.render_video)

		self.window.menubar.Append(self.renderMenu, '&Render')

		self.window.Bind(wx.EVT_MENU, self.On_render_video, self.render_video)

		self.window.Bind(wx.EVT_MENU, self.On_set_videoname, self.set_videoname)

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
		obj["Pos"][2] -= event.GetWheelRotation()/2000
		#if self.data["Object List"][self.data["Current Object"]]["Parent"] != None:
		#	obj["Pos"][2] = obj["Dist"] + self.data["Frames"][self.data["Current Frame"]][ self.data["Object List"][self.data["Current Object"]]["Parent"] ]["Dist"]
		#else:
		#	obj["Pos"][2] = obj["Dist"]
		#	if self.data["Object List"][self.data["Current Object"]]["Children"] != []:
		#		for child in self.data["Object List"][self.data["Current Object"]]["Children"]:
		#			self.data["Frames"][self.data["Current Frame"]][ child ]["Pos"][2] = obj["Dist"] + self.data["Frames"][self.data["Current Frame"]][ child ]["Dist"]
		self.changed = True

	def set_data(self, data):
		#resets all data within the control panel in order to eitehr load a project
		#or to reset to a new project
		self.data = data
		self.canvas.set_data(self.data)
		self.canvas.set_bg(self.data["Background Color"])
		self.r_slider.SetValue(self.data["Background Color"][0]*100)
		self.g_slider.SetValue(self.data["Background Color"][1]*100)
		self.b_slider.SetValue(self.data["Background Color"][2]*100)
		print("data set")

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
		self.origin_rot = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Angle"]
		self.origin_scale_x = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["ScaleX"]
		self.origin_scale_y = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["ScaleY"]

		self.canvas.CaptureMouse()


	def OnMouseUp(self, event):
		self.left_mouse_click = False
		self.middle_mouse_click = False
		self.right_mouse_click = False
		self.canvas.ReleaseMouse()
		self.window.PushHistory()

	def OnMouseMotion(self, event):
		#when mouse is moved triggers this event
		if event.LeftIsDown() and self.listener.get_key(79):
			"""
			if mouse is dragged while left mouse button is down
			calculates the new position of the mouse and compares it to the origin from the mouse click
			add difference to the x,y position accordingly in order to get a "click and drag" effect
			by checking the posision of the mouse click according to the Z axix it avoids a parralax effect
				at different distances
			resets origin position in order to avoid a cumulative effect
			"""

			pos = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Origin"]
			dist = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Dist"]

			width = ((dist*-1.0) * .59) + 6.0
			height = ((dist*-1.0) * .4) + 4.2

			new_x_pos = ((width*2) * (event.GetPosition()[0]/self.width)) - width
			new_y_pos = (((height*2)) * (1.0-(event.GetPosition()[1]/self.height)) - height)- (self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["ScaleY"])

			pos[0] += new_x_pos - self.origin_pos[0]
			pos[1] += new_y_pos - self.origin_pos[1]

			self.origin_pos = (new_x_pos, new_y_pos)

		elif event.LeftIsDown():
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

		elif event.RightIsDown():
			"""
			if dragging and right mouse button is down alters the angle based on mouse posistion
			only checks for position in pixels on screen and treats it as a percentage of the whole screen
			from it's relative starting point, rotating the object at percent * (360*2)
			multiplies it by -1 to reverse the rotation to match the direction of the mouse motion

			"""
			percent = ((event.GetPosition()[0] - self.first_pos[0])/self.width)
			mouse_pos = int(percent * (360)*-1)
			cur_angle = self.origin_rot + mouse_pos
			self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Angle"] = cur_angle

		elif event.MiddleIsDown():
			"""
			if dragging and middle click (mouse wheel click) then alters the scale by the relative position
			of the mouse on the screen, if current object's aspect ratio is clicked then maintains aspect ratio
			needs to be updated to a relative scale from the previous scale instead of relative to the click origin
			"""
			percent = ((event.GetPosition()[0] - self.first_pos[0])/self.width)
			mouse_pos = int(percent * (360*2)*-1)
			cur_x_scale = self.origin_scale_x + -(mouse_pos/10)

			self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["ScaleX"] = cur_x_scale
			if self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["Aspect"]:
				self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["ScaleY"] = cur_x_scale
			else:
				percent = ((event.GetPosition()[1] - self.first_pos[1])/self.height)
				mouse_pos = int(percent * (360*2)*-1)
				cur_y_scale = self.origin_scale_y + (mouse_pos/10)
				self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]["ScaleY"] = cur_y_scale

		else:
			pass


	def SetBackgroundColor(self, event):
		#gets the sliders r, g, b values. divides them by 100 to get a normal value
		#sets this as the canvas' background color
		self.canvas.set_bg((self.r_slider.GetValue()/100,self.g_slider.GetValue()/100,self.b_slider.GetValue()/100, 0.0) )
		self.data["Background Color"] = [self.r_slider.GetValue()/100,self.g_slider.GetValue()/100,self.b_slider.GetValue()/100, 0.0]

	def Update(self, second):
		#if self.canvas.HasFocus():
		#	if self.listener.get_struck()
		#sets the window status to the current frame
		#clears the canvas of all images
		#purge loads the identity and resets the perspective of the camera
		#canvas is then reset to the camera
		#finally everything is drawn
		if self.changed and second:
			self.window.PushHistory()
			self.changed = False

		if self.listener.get_struck(68): #on D
			self.window.timelineCtrl.onNext(1)
		if self.listener.get_struck(65): #on A
			self.window.timelineCtrl.onBack(1)

		self.draw_origin = self.listener.get_key(79)

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

		if not self.window.rendering:
			self.canvas.clear()
			self.canvas.Purge(self.canvas.ViewPortSize)
			self.canvas.transform(self.data["Frames"][self.data["Current Frame"]]["Camera"], False)
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

		if self.canvas.resolution[1] > self.canvas.resolution[0]:
			print("portrait")
			self.height_coords = 4.13
			self.width_pixels, self.height_pixels = self.canvas.ViewPortSize
			self.canvas_ratio = self.width_pixels/self.height_pixels
			self.pix_ratio = self.height_pixels/self.width_pixels
			self.width_coords = self.canvas_ratio * self.height_coords
			self.canvas.box_height = self.height_coords * .9
			self.canvas.box_width = self.canvas.box_height * ( self.canvas.resolution[0] / self.canvas.resolution[1])


			self.px_ratio = self.width_pixels / self.height_pixels
			print(self.px_ratio)

			self.px_height = int(self.canvas.resolution[1] * 1.111)
			self.px_width = int(self.px_height * self.px_ratio)
			#self.px_width = int(self.canvas.resolution[0] * 1.25)
			#self.px_height = int(self.px_width * self.px_ratio)

			print(self.px_width, self.px_height)

			self.yoffset = int((self.px_height * .1) / 2)
			self.xoffset = int((self.px_width * (1-(self.canvas.resolution[0]/self.px_width) )/2 ))

			#self.xoffset = int((self.px_width * .2) / 2)
			#self.yoffset = int((self.px_height * (1-(self.canvas.resolution[1]/self.px_height) )/2 ))

			self.canvas.gen_fbo(self.px_width, self.px_height)
		else:
			print("landscape")
			self.height_coords = 4.13
			self.width_pixels, self.height_pixels = self.canvas.ViewPortSize
			self.canvas_ratio = self.width_pixels/self.height_pixels
			self.pix_ratio = self.height_pixels/self.width_pixels
			self.width_coords = self.canvas_ratio * self.height_coords
			self.canvas.box_width = self.width_coords * .8
			self.canvas.box_height = self.canvas.box_width * (self.canvas.resolution[1] / self.canvas.resolution[0])


			self.px_ratio = self.height_pixels / self.width_pixels

			self.px_width = int(self.canvas.resolution[0] * 1.25)
			self.px_height = int(self.px_width * self.px_ratio)

			print(self.px_width, self.px_height)

			self.xoffset = int((self.px_width * .2) / 2)
			self.yoffset = int((self.px_height * (1-(self.canvas.resolution[1]/self.px_height) )/2 ))

			self.canvas.gen_fbo(self.px_width, self.px_height)

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


	def Draw(self):

		parents = set(self.data["Parents"])

		imglist = self.gen_draw_order(parents)

		draw_order = sorted(imglist , key = lambda x: imglist[x][1])


		for obj in draw_order:
			if obj != "Camera":
				cur_obj = self.data["Frames"][self.data["Current Frame"]][obj]
				if cur_obj["Current Image"] not in ["", "none"]:
					self.Image_list[cur_obj["Current Image"]].draw(cur_obj, parent=obj, draw_origin=self.draw_origin, parents=imglist[obj][0])


		cur_obj = self.data["Frames"][self.data["Current Frame"]]["Camera"]
		obj = "Camera"

		if cur_obj["Current Image"] != "Camera":
			self.Image_list[ cur_obj["Current Image"]].draw(cur_obj, parent=obj, draw_origin=self.draw_origin)

		if self.draw_origin:
			thisobj = self.data["Frames"][self.data["Current Frame"]][self.data["Current Object"]]
			#self.Image_list[ thisobj["Current Image"] ].transform(imglist[self.data["Current Object"]][0], thisobj)
			self.Image_list[ thisobj["Current Image"] ].draw_origin(thisobj, imglist[self.data["Current Object"]][0])


		#resets convas viewbox upon resize to ensure continuity
		if self.canvas.is_resized():
			self.resize_viewbox()

		#draws a box on screen with a ratio of 1.78:1
		#outlines where the actual video will be rendered from
		if not self.window.rendering:
			self.canvas.draw_box()

		#renders everything by swapping the buffers
		self.canvas.Draw()

	def OnClose(self):
		#this should probably do something
		pass

