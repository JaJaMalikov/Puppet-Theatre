import wx
import os
import copy
import pygame
from pygame.locals import Color
from collections import OrderedDict
from pygamepanel import PygamePanel
import  wx.lib.newevent, wx.stc as stc
from statusctrl import StatusCtrl
from objctrl import objCtrl
from listener import Key_listener
from plane import OBJ2D as plane
from model import OBJ3D as massObj
import numpy as np

from OpenGL.GL import *
from OpenGL.GLU import *
"""
Laughware Finger Puppet Theatre
purpose: to easily control characters and props in an animated environment in real time
methods: using pygame's sprite system to group, control, and render sprites as in a videogame
		using wxpython's widgets to access controls and windows to make file loading dramatically easier

custom file formats:
	script:
		rendering of all used sprites, their position, type, recorded actions(if any), and location of object file

	object file:
		detailed list of all resources and their corrisponding keys, as well as the sprite's name

UI:
##################################################################################
# File________________________________________________________________________10?#
#                    #        |       |       |       |       |        |         #
# FPS: 30            #        |       |       |       |       |        |      200#
# group: Actors      #        |       |       |       |       |        |         #
# selection: jack    #________|_______|_______|_______|_______|________|___200___#
# speed: 10          #                                                           #
# Flip H: True       #                                                           #
# Flip V: False      #                                                           #750
# Pos X: 100         #                                                           #
# Pos Y: 100         #                                                           #
# Mouse: rotate/pos  #                                                        540#
# Angle: 30 degrees  #                                                           #
# State: angry       #                                                           #
# substate: running  #                                                           #
# Mouth: Open        #                                                           #
# Recording: False   #                                                           #
# Playback: False    #                                                           #
#        300         #                            960                            #
##################################################################################
		                             1260


"""

def reshape(lst, n):
    return [lst[i*n:(i+1)*n] for i in range(len(lst)//n)]

class PygamePanel(wx.Panel):
	def __init__(self, parent, ID, ViewPortSize, HUD, objctrl):
		#in the name of god do not touch this part
		global pygame
		wx.Panel.__init__(self, parent, ID, size=ViewPortSize, style=wx.WANTS_CHARS)
		self.Fit()
		os.environ['SDL_WINDOWID'] = str(self.GetHandle())
		os.environ['SDL_VIDEODRIVER'] = 'windib'
		import pygame # this has to happen after setting the environment variables.
		pygame.init()
		#seriously do not fuck with anything between these lines

		self.HUD = HUD
		self.objctrl = objctrl
		self.listen = Key_listener()
		self.wireFrame = True

		self.width, self.height = ViewPortSize
		self.screen = pygame.display.set_mode(ViewPortSize, pygame.DOUBLEBUF | pygame.OPENGL | pygame.OPENGLBLIT)

		gluPerspective(45, (self.width/self.height), 0.1, 50.0)
		glTranslatef(0.0, 0.0, -10)
		glClearColor(0,0,0,1)
		#glEnable(GL_DEPTH_TEST)
		self.clock = pygame.time.Clock()

		#self.head = plane("kaiju")
		"""self.sky = plane("sky")
		self.scape = plane("scape")
		self.fore = plane("fore")"""
		self.alan = plane("alan", self.HUD)
		self.moog = plane("moog", self.HUD)
		self.doov = plane("doov", self.HUD)
		self.cube = massObj()
		self.entities = [self.alan, self.moog, self.doov, self.cube]
		self.default_order = [0,1,2,3]
		self.rendering = False
		self.frame = 0


	def Update(self, evt):
		self.objctrl.update()
		self.HUD.set_MPos(self.listen.get_mouse_pos())
		self.HUD.set_FPS(self.clock.get_fps())
		self.HUD.Update()

		if not self.rendering:
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					self.listen.set_keydown(event.key)
				if event.type == pygame.KEYUP:
					self.listen.set_keyup(event.key)
				if event.type == pygame.MOUSEBUTTONDOWN:
					self.listen.set_mouse_down(event.button)
				if event.type == pygame.MOUSEBUTTONUP:
					self.listen.set_mouse_up(event.button)
				if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
					self.entities[self.objctrl.get_cur()].move_D(-10)
				if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
					self.entities[self.objctrl.get_cur()].move_D(10)

			self.listen.set_mouse_pos(pygame.mouse.get_pos())

			if pygame.key.get_pressed()[pygame.K_UP]:
				self.entities[self.objctrl.get_cur()].move_V(1)
			if pygame.key.get_pressed()[pygame.K_DOWN]:
				self.entities[self.objctrl.get_cur()].move_V(-1)
			if pygame.key.get_pressed()[pygame.K_RIGHT]:
				self.entities[self.objctrl.get_cur()].move_H(1)
			if pygame.key.get_pressed()[pygame.K_LEFT]:
				self.entities[self.objctrl.get_cur()].move_H(-1)

			if pygame.key.get_pressed()[pygame.K_PAGEUP]:
				self.entities[self.objctrl.get_cur()].move_D(-1)
			if pygame.key.get_pressed()[pygame.K_PAGEDOWN]:
				self.entities[self.objctrl.get_cur()].move_D(1)
			if pygame.key.get_pressed()[pygame.K_HOME]:
				self.entities[self.objctrl.get_cur()].rotn()
			if pygame.key.get_pressed()[pygame.K_END]:
				self.entities[self.objctrl.get_cur()].rotp()

			if pygame.key.get_pressed()[pygame.K_KP_DIVIDE]:
				self.entities[self.objctrl.get_cur()].start_recording()
				for x in range(len(self.entities)):
					self.entities[x].places()

			if pygame.key.get_pressed()[pygame.K_KP_MULTIPLY]:
				self.entities[self.objctrl.get_cur()].stop_recording()
			if pygame.key.get_pressed()[pygame.K_KP_MINUS]:
				self.entities[self.objctrl.get_cur()].stop_playing()
			if pygame.key.get_pressed()[pygame.K_KP_PLUS]:
				self.entities[self.objctrl.get_cur()].start_playing()
			if pygame.key.get_pressed()[pygame.K_KP_ENTER]:
				self.entities[self.objctrl.get_cur()].places()

			if pygame.key.get_pressed()[pygame.K_F12]:
				self.entities[self.objctrl.get_cur()].places()
				self.rendering = True
			if self.listen.get_struck(pygame.K_INSERT):
				self.entities[self.objctrl.get_cur()].flipX()
			if self.listen.get_struck(pygame.K_DELETE):
				self.entities[self.objctrl.get_cur()].flipY()


			if self.listen.get_mouse_button(1):
				self.entities[self.objctrl.get_cur()].set_pos(self.listen.get_mouse_pos())
			if self.listen.get_mouse_button(3):
				self.entities[self.objctrl.get_cur()].m_rot(pygame.mouse.get_rel())

			if pygame.key.get_pressed()[pygame.K_KP0]:
				self.objctrl.set_obj(0)
			if pygame.key.get_pressed()[pygame.K_KP1]:
				self.objctrl.set_obj(1)
			if pygame.key.get_pressed()[pygame.K_KP2]:
				self.objctrl.set_obj(2)
			if pygame.key.get_pressed()[pygame.K_KP3]:
				self.objctrl.set_obj(3)

			if pygame.key.get_pressed()[pygame.K_EQUALS]:
				self.entities[self.objctrl.get_cur()].zoom(1)
			if pygame.key.get_pressed()[pygame.K_MINUS]:
				self.entities[self.objctrl.get_cur()].zoom(-1)

			if pygame.key.get_pressed()[pygame.K_p]:
				for x in range(len(self.entities)):
					self.entities[x].places()

		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

		draw_order = [x for _, x in sorted(zip( self.entities , self.default_order), key=lambda x: x[0].data["pos"][2] )]
		for x in draw_order:
			self.entities[x].update()
			self.entities[x].draw_entity()
			if self.wireFrame:
				self.entities[x].draw_wire()

		self.entities[self.objctrl.get_cur()].set_data()

		self.listen.clear_struck()

		if self.rendering:
			glReadBuffer( GL_FRONT )
			imgdata = glReadPixels(0,0,self.width,self.height,GL_RGBA,GL_UNSIGNED_BYTE)
			fin_surf = pygame.image.fromstring(imgdata, (self.width,self.height), "RGBA", True)
			pygame.image.save(fin_surf, "D:/frames/{0:05d}".format(self.frame) + ".png")#pygame.transform.smoothscale(fin_surf, (1920,1080)), "D:/frames/{0:05d}".format(self.frame) + ".png")
			self.frame += 1

		pygame.display.flip()

		self.clock.tick(2000)

	def OnClose(self):
		pygame.quit()

class PuppetTheatre(wx.Frame):
	def __init__(self, parent, title, size):
		#main frame, sets up menu bar and SDL frame where the animation happens
		wx.Frame.__init__(self, parent, wx.ID_ANY, title, pos=(1,1), size=size, style= (wx.DEFAULT_FRAME_STYLE|wx.WANTS_CHARS) ^ (wx.RESIZE_BORDER|wx.MAXIMIZE_BOX) )

		#setting up the icon
		icon = wx.Icon()
		icon.CopyFromBitmap(wx.Bitmap("icon.bmp", wx.BITMAP_TYPE_ANY))
		self.SetIcon(icon)

		##########Begin menubar setup
		#menu bar contains loading and saving of script files
		menubar = wx.MenuBar()

		#file menu contains load script, save script, and close window
		#will also contain help menu at a later date
		fileMenu = wx.Menu()

		loadScript = fileMenu.Append(wx.ID_OPEN, 'Load Script', 'Load Script from File')
		saveScript = fileMenu.Append(wx.ID_SAVE, 'Save Script', 'Save Script to File')
		closeWin = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit Application')

		#adding menus to the menu bar
		menubar.Append(fileMenu, '&File')

		#adds the menu bar to the window
		self.SetMenuBar(menubar)
		#########End MenuBar setup

		############# inset useful panels here

		self.topBox = wx.BoxSizer(wx.HORIZONTAL)
		self.HUD = StatusCtrl(self, size= (300,600) )
		self.ObjCtrl = objCtrl(self, wx.ID_ANY, self.HUD)
		self.topBox.Add(self.ObjCtrl, 1)

		self.botBox = wx.BoxSizer(wx.HORIZONTAL)

		self.timer = wx.Timer(self)

		self.botBox.Add(self.HUD, 0, wx.EXPAND)

		self.gamePanel = PygamePanel(self, -1, (1140, 640), self.HUD, self.ObjCtrl)
		self.botBox.Add(self.gamePanel, 0, wx.EXPAND)

		self.mainBox = wx.BoxSizer(wx.VERTICAL)		
		self.mainBox.Add(self.topBox, 0, wx.EXPAND)
		self.mainBox.Add(self.botBox, 0, wx.EXPAND)

		self.SetSizer(self.mainBox)
		self.SetAutoLayout(1)

		############# end useful panels

		############# bindings

		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.Bind(wx.EVT_MENU, self.OnClose, closeWin)
		self.Bind(wx.EVT_MENU, self.OnLoad, loadScript)
		self.Bind(wx.EVT_MENU, self.OnSave, saveScript)
		self.Bind(wx.EVT_TIMER, self.gamePanel.Update, self.timer)

		############# end bindings


		############# Timers
		self.timer.Start(20)

		############# End Timers

	##################event methods

	def OnLoad(self, event):
		with wx.FileDialog(self, "Load Script File", wildcard="Script files (*.tscr)|*.tscr",
							style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
			if fileDialog.ShowModal() == wx.ID_CANCEL:
				return

			pathname = fileDialog.GetPath()
			print(pathname)
			try:
				with open(pathname, 'r') as file:
					print(file.read())
			except IOError:
				wx.LogError("Cannot Open file %s" % pathname)


	def OnSave(self, event):
		with wx.FileDialog(self, "Save Script File", wildcard="Script files (*.tscr)|*.tscr",
							style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
			if fileDialog.ShowModal() == wx.ID_CANCEL:
				return

			pathname = fileDialog.GetPath()

			try:
				with open(pathname, 'w') as file:
					file.write("this is a test")
			except IOError:
				wx.LogError("Cannot save current data in file %s" % pathname)

	def OnClose(self, event):
		self.gamePanel.OnClose()
		wx.Exit()
		exit()	

if __name__ == '__main__':
	app = wx.App()
	view = PuppetTheatre(parent=None, title='Finger Puppet Theatre', size=(1456, 810) )
	view.Show()
	app.MainLoop()
