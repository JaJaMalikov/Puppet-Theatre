#Graphical Libraries
import wx

#Other Built-in libraries
import os

#loads audio and converts to a list of data points for the waveform
import sampler

#constants to be used throughout the program
from consts import * 

loc = 74

class PygamePanel(wx.Panel):
	"""
	future adjustments are to turn this into a more functional embdedded pygame panel
	with options to inherit from it maing creation of such panels easier
	"""
	def __init__(self, parent, ID, ViewPortSize, window):
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
		global pygame
		wx.Panel.__init__(self, parent, ID, size=ViewPortSize)
		self.Fit()
		os.environ['SDL_WINDOWID'] = str(self.GetHandle())
		os.environ['SDL_VIDEODRIVER'] = 'windib'
		import pygame
		pygame.init()

		### everything above this is completely nessesary as is

		self.SetBackgroundColour((10,100,10))
		self.set_clear_color((0,0,0))
		self.set_size(ViewPortSize)
		self.layout()

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
		self.screen = pygame.display.set_mode(self.ViewPortSize, pygame.RESIZABLE)

	def draw(self, image, pos):
		self.screen.blit(image, pos)

	def Update(self):

		#swaps the buffers and then clears the new buffer before drawing
		#not strictly nessesary but useful for current purposes
		pygame.display.flip()
		self.screen.fill(self.clear_color)

	def OnClose(self):
		pygame.quit()
