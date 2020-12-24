import wx
import os
import copy
import pygame
from pygame.locals import Color
from collections import OrderedDict
from pygamepanel import PygamePanel
import  wx.lib.newevent, wx.stc as stc

class StatusCtrl(stc.StyledTextCtrl):
	def __init__(self, parent, style=wx.SIMPLE_BORDER, size=(1,1)):
		stc.StyledTextCtrl.__init__(self, parent, style=style, size=size)
		self._styles = [None] * 32
		self._free = 1
		self.SetWrapMode(True)
		self.SetIndent(4)
		self.SetTabIndents(True)
		self.states = OrderedDict({"FPS": "1",
									"Group":"Actors",
									"Selection": "3",
									"Speed":"1",
									"Flip H":"False",
									"Flip V":"False",
									"Pos X":"1",
									"Pos Y":"1",
									"Mouse":"Rotation",
									"Angle":"90",
									"State":"angry",
									"Substate":"running",
									"Mouth":"open",
									"Recording":"False",
									"Playback":"False",
									"MPos": "(1,1)",
									"X offset": "0",
									"Y offset": "0",
									"Animating": "False",
									})

		self.display_text = "FPS: %s\nGroup: %s\nSelection: %s\nSpeed: %s\nFlip H: %s\nFlip V: %s\nPos X: %s\nPos Y: %s\nMouse: %s\nAngle: %s\nState: %s\nSubstate: %s\nMouth: %s\nRecording: %s\nPlayback: %s\nMouse pos: %s\nX offset: %s\nY offset: %s\nAnimating: %s"

		return


	def set_group(self, group):
		self.states["Group"] = str(group)

	def set_selection(self, selection):
		self.states["Selection"] = str(selection)

	def set_Animating(self, animating):
		self.states["Animating"] = str(animating)

	def set_yoffset(self, offset):
		self.states["Y offset"] = str(offset)

	def set_xoffset(self, offset ):
		self.states["X offset"] = str(offset)

	def set_playback(self, playback):
		self.states["Playback"] = str(playback)

	def set_recording(self, recording):
		self.states["Recording"] = str(recording)

	def set_mouth(self, mouth):
		self.states["Mouth"] = str(mouth)

	def set_substate(self, substate):
		self.states["Substate"] = str(substate)

	def set_state(self, state):
		self.states["State"] = str(state)

	def set_angle(self, angle):
		self.states["Angle"] = str(angle)

	def set_mouse(self, mouse):
		self.states["Mouse"] = str(mouse)

	def set_pos(self, pos):
		self.states["Pos X"] = str(pos[0])
		self.states["Pos Y"] = str(pos[1])

	def set_FLIP_V(self, v):
		self.states["Flip V"] = str(v)

	def set_FLIP_H(self, h):
		self.states["Flip H"] = str(h)

	def set_Speed(self, speed):
		self.states["Speed"] = str(speed)

	def set_FPS(self, FPS):
		self.states["FPS"] = str(int(FPS))

	def set_MPos(self, MPos):
		self.states["MPos"] = str( MPos )

	def Update(self):
		self.SetText(self.display_text % tuple(self.states.values()) )