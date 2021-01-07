#Graphical Libraries
import wx

#Other Built-in libraries
import os

#loads audio and converts to a list of data points for the waveform
import sampler

#constants to be used throughout the program
from consts import * 

import pygame

class PygamePanel(wx.Panel):
	"""
	future adjustments are to turn this into a more functional embdedded pygame panel
	with options to inherit from it maing creation of such panels easier
	"""
	def __init__(self, parent, ID, ViewPortSize, window, listener):
		"""
		the following code is modified from a post by:
			https://stackoverflow.com/users/1747037/alex-sallons
		every line is important and must be presented as-is in order to work

		first establishes pygame as a global variable for use outside the init function
		then initializes the panel ID and size
		calls Fit to shape the panel into the containing window
		sets the environmental variable "SDL_WINDOWID" to the current panel ID
			this causes the driver to draw pygame directly to the panel
		the line os.environ['SDL_VIDEODRIVER'] = 'windib' may be omitted on non-window systems
			this sets the driver to the compatible windib on windows
		only then can pygame be imported and initialized
		"""
		wx.Panel.__init__(self, parent, ID, size=ViewPortSize)
		pygame.init()
		### everything above this is completely nessesary as is

		self.listener = listener
		self.parent = parent
		self.SetBackgroundColour((10,100,10))
		self.set_clear_color((0,0,0))
		self.set_size(ViewPortSize)
		self.layout()

		self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
		self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
		self.Bind(wx.EVT_MOTION, self.OnMouseMotion)
		self.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseUp)

	def OnMouseMotion(self, event):
		self.listener.set_mouse_pos(event.GetPosition())

	def OnMouseDown(self, event):
		if event.LeftIsDown():
			self.listener.set_mouse_down(1)
		if event.MiddleIsDown():
			self.listener.set_mouse_down(2)
		if event.RightIsDown():
			self.listener.set_mouse_down(3)

	def OnMouseUp(self, event):
		self.listener.set_mouse_up(1)
		self.listener.set_mouse_up(2)
		self.listener.set_mouse_up(3)


	def set_clear_color(self, color):
		self.clear_color = color

	def set_size(self, new_size):
		#resizes the panel based on parent's parameters
		self.SetSize(new_size)
		self.size=new_size
		self.ViewPortSize = new_size
		self.length, self.height = new_size

	def layout(self):
		#resize the screen to the current ViewPortSize
		self.screen = pygame.Surface(self.ViewPortSize, 0, 32)

	def draw(self, image, pos):
		self.screen.blit(image, pos)

	def render(self):
		image_string = pygame.image.tostring(self.screen, "RGB")
		wx_img = wx.Image(self.length, self.height, image_string)
		wx_bmp = wx.Bitmap(wx_img)
		dc = wx.ClientDC(self)
		dc.DrawBitmap(wx_bmp, 0, 0, False)
		del dc

	def Update(self):
		#swaps the buffers and then clears the new buffer before drawing
		#not strictly nessesary but useful for current purposes
		self.render()
		#self.screen.fill(self.clear_color)

		if self.HasFocus():
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					self.listener.set_keydown(event.key)
				elif event.type == pygame.KEYUP:
					self.listener.set_keyup(event.key)
				elif event.type == pygame.MOUSEBUTTONDOWN:
					self.listener.set_mouse_down(event.button)
				elif event.type == pygame.MOUSEBUTTONUP:
					self.listener.set_mouse_up(event.button)
				else:
					pass
		


	def OnClose(self):
		pygame.quit()
