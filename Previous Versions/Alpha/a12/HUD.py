import wx
import os
import copy
import pygame
from pygame.locals import Color
from collections import OrderedDict
from drawable import Drawable

class HUD(Drawable):
	def __init__(self, width, height, font):
		Drawable.__init__(self, width, height)
		self.font = font
		self.state_surf = pygame.Surface((250, 600), pygame.SRCALPHA, 32).convert_alpha()
		self.profile_surf = pygame.Surface((self.width, 150), pygame.SRCALPHA, 32).convert_alpha()

		self.display_text = ["FPS: %s",
		"Group: %s",
		"Selection: %s",
		"Speed: %s",
		"Flip H: %s",
		"Flip V: %s",
		"Pos X: %s",
		"Pos Y: %s",
		"Mouse: %s",
		"Angle: %s",
		"State: %s",
		"Substate: %s",
		"Mouth: %s",
		"Recording: %s",
		"Playback: %s",
		"Mouse pos: %s",
		"X offset: %s",
		"Y offset: %s",
		"Animating: %s"
		]

		self.states = OrderedDict({"FPS": 1,
									"Group":"Actors",
									"Selection": "3",
									"Speed":1,
									"Flip H":False,
									"Flip V":False,
									"Pos X":1,
									"Pos Y":1,
									"Mouse":"Rotation",
									"Angle":90,
									"State":"angry",
									"Substate":"running",
									"Mouth":"open",
									"Recording":False,
									"Playback":False,
									"MPos": (1,1),
									"X offset": 0,
									"Y offset": 0,
									"Animating": False
									})

	def set_group(self, group):
		self.states["Group"] = group

	def set_selection(self, selection):
		self.states["Selection"] = selection

	def set_Animating(self, animating):
		self.states["Animating"] = animating

	def set_yoffset(self, offset):
		self.states["Y offset"] = offset

	def set_xoffset(self, offset ):
		self.states["X offset"] = offset

	def set_playback(self, playback):
		self.states["Playback"] = playback

	def set_recording(self, recording):
		self.states["Recording"] = recording

	def set_mouth(self, mouth):
		self.states["Mouth"] = mouth

	def set_substate(self, substate):
		self.states["Substate"] = substate

	def set_state(self, state):
		self.states["State"] = state

	def set_angle(self, angle):
		self.states["Angle"] = angle

	def set_mouse(self, mouse):
		self.states["Mouse"] = mouse

	def set_pos(self, pos):
		self.states["Pos X"] = pos[0]
		self.states["Pos Y"] = pos[1]

	def set_FLIP_V(self, v):
		self.states["Flip V"] = v

	def set_FLIP_H(self, h):
		self.states["Flip H"] = h

	def set_Speed(self, speed):
		self.states["Speed"] = speed

	def set_FPS(self, FPS):
		self.states["FPS"] = FPS

	def set_MPos(self, MPos):
		xpos, ypos = MPos
		xpos = (xpos - 250)
		ypos = (ypos - 150)
		if xpos < 0 or ypos < 0 or xpos > 960 or ypos > 540:
			pos = "offscreen"
		else:
			pos = (xpos,ypos)
		self.states["MPos"] = pos

	def update(self):
		self.state_surf.fill((100,100,100))
		self.profile_surf.fill((100,100,100))

		for line in range(len(self.display_text)):
			cur_text = self.display_text[line] % str(self.states[ list(self.states.keys())[line] ])
			text_render = self.font.render(cur_text, True, Color("black"))
			self.state_surf.blit(text_render, (20,20 + 30*line))

		self.main_surf.blit(self.state_surf, (0,150))
		self.main_surf.blit(self.profile_surf, (0, 0))

