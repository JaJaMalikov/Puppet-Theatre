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
		self.objctrl.populate()
		self.listen = Key_listener()
		self.wireFrame = False

		self.width, self.height = ViewPortSize
		self.screen = pygame.display.set_mode(ViewPortSize, pygame.DOUBLEBUF | pygame.OPENGL)

		gluPerspective(45, (self.width/self.height), 0.1, 50.0)
		glTranslatef(0.0, 0.0, -10)
		glClearColor(0,0,0,0)
		#glEnable(GL_DEPTH_TEST)
		self.clock = pygame.time.Clock()


		self.rendering = False
		self.render_toggle = False
		self.frame = 0

		self.mouth_codes = [pygame.K_z, pygame.K_x, pygame.K_c, pygame.K_v, pygame.K_b, pygame.K_n, pygame.K_m]
		self.state_codes = [pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_r, pygame.K_t, pygame.K_y, pygame.K_u, pygame.K_i, pygame.K_o, pygame.K_p]
		self.substate_codes = [pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f, pygame.K_g, pygame.K_h, pygame.K_j, pygame.K_k, pygame.K_l]
		self.dirs_codes = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]

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
					self.objctrl.move_D(-10)
				if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
					self.objctrl.move_D(10)

			self.listen.set_mouse_pos(pygame.mouse.get_pos())

			if pygame.key.get_pressed()[pygame.K_UP]:
				self.objctrl.move_V(1)
			if pygame.key.get_pressed()[pygame.K_DOWN]:
				self.objctrl.move_V(-1)
			if pygame.key.get_pressed()[pygame.K_RIGHT]:
				self.objctrl.move_H(1)
			if pygame.key.get_pressed()[pygame.K_LEFT]:
				self.objctrl.move_H(-1)

			if pygame.key.get_pressed()[pygame.K_PAGEUP]:
				self.objctrl.move_D(-1)
			if pygame.key.get_pressed()[pygame.K_PAGEDOWN]:
				self.objctrl.move_D(1)
			if pygame.key.get_pressed()[pygame.K_HOME]:
				self.objctrl.rotn()
			if pygame.key.get_pressed()[pygame.K_END]:
				self.objctrl.rotp()

			if pygame.key.get_pressed()[pygame.K_KP_DIVIDE]:
				self.objctrl.start_recording()
				self.objctrl.places()

			if pygame.key.get_pressed()[pygame.K_KP_MULTIPLY]:
				self.objctrl.stop_recording()
			if pygame.key.get_pressed()[pygame.K_KP_MINUS]:
				self.objctrl.stop_playing()
			if pygame.key.get_pressed()[pygame.K_KP_PLUS]:
				self.objctrl.start_playing()
			if pygame.key.get_pressed()[pygame.K_KP_ENTER]:
				self.objctrl.places()
			if pygame.key.get_pressed()[pygame.K_KP_PERIOD]:
				self.objctrl.clear()

			if self.listen.get_struck(pygame.K_INSERT):
				self.objctrl.set_visible(True)
			if self.listen.get_struck(pygame.K_DELETE):
				self.objctrl.set_visible(False)

			if self.listen.get_struck(pygame.K_LEFTBRACKET):
				self.objctrl.flipX()
			if self.listen.get_struck(pygame.K_RIGHTBRACKET):
				self.objctrl.flipY()


			if self.listen.get_mouse_button(1):
				self.objctrl.set_pos(self.listen.get_mouse_pos())
			if self.listen.get_mouse_button(3):
				self.objctrl.m_rot(pygame.mouse.get_rel())

			if pygame.key.get_pressed()[pygame.K_KP0]:
				self.objctrl.set_obj(0)
			if pygame.key.get_pressed()[pygame.K_KP1]:
				self.objctrl.set_obj(1)
			if pygame.key.get_pressed()[pygame.K_KP2]:
				self.objctrl.set_obj(2)
			if pygame.key.get_pressed()[pygame.K_KP3]:
				self.objctrl.set_obj(3)
			if pygame.key.get_pressed()[pygame.K_KP4]:
				self.objctrl.set_obj(4)
			if pygame.key.get_pressed()[pygame.K_KP5]:
				self.objctrl.set_obj(5)
			if pygame.key.get_pressed()[pygame.K_KP6]:
				self.objctrl.set_obj(6)
			if pygame.key.get_pressed()[pygame.K_KP7]:
				self.objctrl.set_obj(7)
			if pygame.key.get_pressed()[pygame.K_KP8]:
				self.objctrl.set_obj(8)
			if pygame.key.get_pressed()[pygame.K_KP9]:
				self.objctrl.set_obj(9)

			if pygame.key.get_pressed()[pygame.K_EQUALS]:
				self.objctrl.zoom(1)
			if pygame.key.get_pressed()[pygame.K_MINUS]:
				self.objctrl.zoom(-1)

			if pygame.key.get_pressed()[pygame.K_F1]:
				self.objctrl.set_group("Actors")
			if pygame.key.get_pressed()[pygame.K_F2]:
				self.objctrl.set_group("Cameras")
			if pygame.key.get_pressed()[pygame.K_F3]:
				self.objctrl.set_group("Props")
			if pygame.key.get_pressed()[pygame.K_F4]:
				self.objctrl.set_group("BGs")

			if pygame.key.get_pressed()[pygame.K_F5]:
				self.objctrl.start_record_cam()
			if pygame.key.get_pressed()[pygame.K_F6]:
				self.objctrl.stop_record_cam()
			if pygame.key.get_pressed()[pygame.K_F7]:
				self.objctrl.clear_cam()
			if pygame.key.get_pressed()[pygame.K_F8]:
				self.objctrl.play_cam()
			if pygame.key.get_pressed()[pygame.K_F9]:
				self.objctrl.pause_cam()

			for control_key in self.mouth_codes:
				if pygame.key.get_pressed()[control_key]:
					self.objctrl.set_mouth(control_key)

			for control_key in self.state_codes:
				if pygame.key.get_pressed()[control_key]:
					self.objctrl.set_state(control_key)

			for control_key in self.substate_codes:
				if pygame.key.get_pressed()[control_key]:
					self.objctrl.set_substate(control_key)

			for control_key in self.dirs_codes:
				if pygame.key.get_pressed()[control_key]:
					self.objctrl.set_dir(control_key)

			self.objctrl.space_toggle(pygame.key.get_pressed()[pygame.K_SPACE])

		if pygame.key.get_pressed()[pygame.K_F12] and not self.render_toggle:
			if self.rendering:
				self.rendering = False
			else:
				self.objctrl.places()
				self.rendering = True
			self.render_toggle = True
		if not pygame.key.get_pressed()[pygame.K_F12] and self.render_toggle:
			self.render_toggle = False

		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		#glPushMatrix()

		viewport = self.objctrl.get_viewport()

		glTranslatef(viewport.data["pos"][0], viewport.data["pos"][1] , viewport.data["pos"][2])
		glRotatef(viewport.data["angle"], 0, 0, 1)
		glScalef(viewport.data["flipX"] * viewport.data["scale"],viewport.data["flipY"] * viewport.data["scale"],1.0)

		self.objctrl.set_data()

		self.objctrl.update()

		self.listen.clear_struck()

		if self.rendering:
			glReadBuffer( GL_FRONT )
			imgdata = glReadPixels(0,0,self.width,self.height,GL_RGBA,GL_UNSIGNED_BYTE)
			fin_surf = pygame.image.fromstring(imgdata, (self.width,self.height), "RGBA", True)
			pygame.image.save(fin_surf, "D:/frames/{0:05d}".format(self.frame) + ".png")
			self.frame += 1

		pygame.display.flip()

		#self.objctrl.clear_camera()
		glLoadIdentity()
		gluPerspective(45, (self.width/self.height), 0.1, 50.0)
		glTranslatef(0.0, 0.0, -10)

		#glPopMatrix()
		self.clock.tick(2000)

	def OnClose(self):
		pygame.quit()