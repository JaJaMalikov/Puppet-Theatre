#!/usr/bin/env python3

import pygame
from pygame.locals import *
import pygame.gfxdraw
import pygame.font

import math, time, sys, os, random
import copy, json
from collections import OrderedDict, deque

res_prefix = "res"

##############################################utility functions############################################
def joiner(names):
	return os.path.join(*names)

def rotate(surface, angle, pivot, offset, scale):
	"""Rotate the surface around the pivot point.

	Args:
		surface (pygame.Surface): The surface that is to be rotated.
		angle (float): Rotate by this angle.
		pivot (tuple, list, pygame.math.Vector2): distance from upper left corner of the destination
		offset (pygame.math.Vector2): distance from center 0,0 being center -1,-1, being just to the upper left.
		scale (float): scale the image being rotated
	"""
	rotated_image = pygame.transform.rotozoom(surface, -angle, scale)  # Rotate the image.
	rotated_offset = offset.rotate(angle)  # Rotate the offset vector.
	# Add the offset vector to the center/pivot point to shift the rect.
	rect = rotated_image.get_rect(center=pivot+rotated_offset)
	return rotated_image, rect  # Return the rotated image and shifted rect.

def load_imageset(name):
	#loads all images in order within a file directory
	imageset = []
	filelist = os.listdir(joiner([res_prefix,name]))
	filelist.sort()
	for file in filelist:
		try:
			imageset.append(pygame.image.load( joiner([res_prefix, name, file])))
		except:
			pass
	return imageset

###########################################Utility classes #####################################################

class key_listener:
	"""
	retains static data on key states for continuous input
	"""
	def __init__(self):
		self.keymap = [False]*512
		self.struck = []
	def set_keydown(self, key):
		print(key)
		self.keymap[key] = True
	def set_keyup(self, key):
		self.keymap[key] = False
	def get_key(self, key):
		return self.keymap[key]
	def get_state(self):
		return copy.deepcopy(self.keymap)


class bounce:
	"""
	a basic mechanic which can be used within another object to create a bouncing effect on just that object
	"""
	def __init__(self):
		self.max = -24 #multiple of 1,2,3,4,6,12,24
		self.counter = 0
		self.step = 3 #divisor of 6,12,24
		self.sign = -1
		self.bouncing = False
	def start(self):
		self.bouncing = True
		self.counter = 0
		self.sign = -1
	def update(self):
		if self.bouncing:
			if self.counter == self.max and self.sign == -1:
				self.sign = 1
			else:
				self.counter += (self.step * self.sign)
				if self.counter == 0:
					self.sign = -1
					self.bouncing = False
	def get_scale(self):
		return (1.0 + (self.counter/100))
	def is_bouncing(self):
		return self.bouncing

###########################################################Object classes##################################

class Entity(pygame.sprite.Sprite):
	"""
	displayable entity with recordable actions via the data dict
	data is recorded by deepcopying into a list called record
	the data is numerical and string only, data which is static does not need to be saved
	self.data = {}
		pos - x, y coordinates on the stage frame NOT ABSOLUTE POSITION (int, int)
		size - w,h on the stage NOT ABSOLUTE POSITION (int,int)
		draw_order - draw order in the form of a float from 0.0 - 1.0
		current_frame - current animated frame, int 0 - max length of frames
	self.record = [self.data,self.data]
	self.instructions -> set of instructions, static or otherwise which tells the objects how to change

	update() -> update all data by instructions
	"""
	def __init__(self, x_pos, y_pos, w, h, draw_order, framerate, len_frames, speed):
		pygame.sprite.Sprite.__init__(self)

		self.record = []
		self.is_recording = False
		self.is_playback = False
		self.cur_playback_frame = 0


		self.data = OrderedDict()
		self.data["rect"] = pygame.Rect(w,h,x_pos,y_pos)

		self.data["draw_order"] = draw_order
		self.data["current_animation_frame"] = 0

		#set of currently depressed keys to prevent single-activation keys from being used over and over
		self.keys_down = [False]*512
		self.IMG_width = 0
		self.IMG_height = 0
		self.animating = False

		self.count = 0

		self.animation_framerate = framerate
		self.len_frames = len_frames
		self.sprite_sheet = None
		self.speed = speed

	def reset_playback(self):
		self.cur_playback_frame = 0

	def record(self):
		self.recording = True
		self.record = []
		self.reset_playback()

	def append(self):
		self.recording = True

	def get_rect(self):
		return self.data["rect"]

	def set_pos(self, x_pos, y_pos):
		self.data["rect"] = pygame.Rect(self.data["rect"].w, self.data["rect"].h, x_pos, y_pos)

	def get_center(self):
		return self.data["rect"].center

	def set_center(self, center):
		self.data["rect"].center = center

	def update(self):
		if self.is_recording:
			self.record.append(copy.deepcopy(self.data))

		if self.is_playback:
			self.cur_playback_frame += 1
			if self.cur_playback_frame >= len(self.record):
				self.cur_playback_frame = 0
			self.data = self.record[self.cur_playback_frame]

	def next_frame(self):
		self.count += 1
		if self.count >= self.framerate:
			self.count = 0
			self.data["current_animation_frame"] += 1
			if self.data["current_animation_frame"] == self.len_frames:
				self.data["current_animation_frame"] = 0

	def prev_frame(self):
		self.count += 1
		if self.count >= self.framerate:
			self.count = 0
			self.data["current_animation_frame"] -= 1
			if self.data["current_animation_frame"] == -1:
				self.data["current_animation_frame"] = self.len_frames-1


class Background(Entity):
	def __init__(self, name, framerate, draw_order):
		self.imageset = load_imageset(name)
		Entity.__init__(self, 0,0,0,0, draw_order, framerate, len(self.imageset))
		self.data["rect"] = self.imageset[0].get_rect()

	def update(self):
		self.next_frame()

	def get_image(self):
		return self.imageset[self.data["frame"]]

	def reset_playback(self):
		self.data["current_animation_frame"] = 0


class Mob(Entity):
	#gonna have multiple functions to create motion and animation
	#move up, down, left, and right - changes the x and y positions relitive to the stage
	#move close/far - changes the scale (reletive to the stage) and draw order so that close objects are drawn last
	#change direction - changes which way the character/object is facing, useful in creating moonwalking or push effects
	#change state - alters which imageset is used, all imagesets will be loaded dynamically by name, stored in dict
	#animate - cycles frames of current state, allowing static objects to animate, gives charcters ability to dance etc
	#be stil - stop all animation and movement

	#record - toggles on and off, if recording exists append new recording, allows to cut between actions smoothly

	#input - to be overriden so that characters and props have different movement instruction sets
	def __init__(self, x_pos, y_pos, w, h, draw_order, framerate, len_frames):
		Entity.__init__(self, x_pos, y_pos, w, h, draw_order, framerate, len_frames)
		self.data["dir"] = 0
		self.data["ver_dir"] = 0 #either 0 or 2
		self.data["hor_dir"] = 0 #either 0 or 1
		#hor + vert = 0,1,2,3 

		self.data["scale"] = 1.0
		self.data["state"] = "default"
		self.data["mouth"] = "closed"
		self.prev_state = "default"
		self.animating = False


		self.advance_frame = False
		self.scale_speed = .01 * self.speed

	def move_up(self):
		self.data["rect"].move(0,-1)

	def move_down(self):
		self.data["rect"].move(0,1)

	def move_left(self):
		self.data["rect"].move(-1,0)

	def move_right(self):
		self.data["rect"].move(1,0)

	def increase_scale(self):
		self.data["scale"] += self.scale_speed

	def reduce_scale(self):
		self.data["scale"] -= self.scale_speed

	def increase_draw_order(self):
		self.data["draw_order"] += self.scale_speed

	def reduce_draw_order(self):
		self.data["draw_order"] -= self.scale_speed

	def face_up(self):
		self.data["ver_dir"] = 2

	def face_down(self):
		self.data["ver_dir"] = 0

	def face_right(self):
		self.data["hor_dir"] = 0

	def face_left(self):
		self.data["hor_dir"] = 1

	def change_state(self, state):
		self.data["state"] = state

	def animate(self):
		if self.advance_frame:
			self.next_frame()
		else:
			self.prev_frame()

	def be_still(self):
		self.data["current_animation_frame"] = 0
		self.advance_frame = False

	def start_record(self):
		self.is_recording = True
		self.record = []

	def append_recording(self):
		self.is_recording = True

	def stop_recording(self):
		self.is_recording = False

	def input(self, listener):
		pass

	def get_image(self):
		#return image as reletive to the size of the stage
		return self.imageset[self.data["state"]]

class Actor(Mob):
	#composite characters - optional, static characters can be created by feeding a single layer in
	#create composites of the movement and animation controls
	#up - reduce scale + reduce draw order + dir(back) + animate
	#down - increase scale + increase draw order + dir(fore) + animate
	#left - reduce X_pos + dir(left) + animate
	#right - increase X_pos + dir(right) + animate
	#[ - decrease Y_pos (flying characters?)
	#] - increase Y_pos
	#q = state("default")
	#w = state("happy")
	#e = state("angry")
	#r = state("sad")
	#t = state("laugh")
	#y = state("dance")
	#a = state("mouth_open") (toggle)
	#s = state("mouth_open") (on then off when let go)
	#z = toggle animate

	def __init__(self, x_pos, y_pos, w, h, draw_order, framerate, len_frames):
		Mob.__init__(self, x_pos, y_pos, w, h, draw_order, framerate, len_frames)

	def input(self, listener):
		if listener.get_key(pygame.K_UP):
			self.reduce_scale()
			self.reduce_draw_order()
			self.face_up()
			self.animate()

		elif listener.get_key(pygame.K_DOWN):
			self.increase_scale()
			self.increase_draw_order()
			self.face_down()
			self.animate()

		elif listener.get_key(pygame.K_LEFT):
			self.move_left()
			self.face_left()
			self.animate()

		elif listener.get_key(pygame.K_RIGHT):
			self.move_right()
			self.face_right()
			self.animate()

		elif listener.get_key(pygame.K_LEFTBRACKET):
			self.move_up()

		elif listener.get_key(pygame.K_RIGHTBRACKET):
			self.move_down()

		elif listener.get_key(pygame.K_q):
			self.change_state("default")

		elif listener.get_key(pygame.K_w):
			self.change_state("happy")

		elif listener.get_key(pygame.K_e):
			self.change_state("angry")

		elif listener.get_key(pygame.K_r):
			self.change_state("sad")

		elif listener.get_key(pygame.K_t):
			self.change_state("dance")

		elif listener.get_key(pygame.K_a):
			if self.data["mouth"] == "open":
				self.data["mouth"] = "closed"
			else:
				self.data["mouth"] = "open"

		elif listener.get_key(pygame.K_z):
			if self.animating:
				self.animating = False
			else:
				self.animating = True

		else:
			if self.animating:
				self.animate()
			else:
				self.be_still()

		if keys_down(pygame.K_s) and not listener.get_key(pygame.K_s):
			self.data["mouth"] = "closed"
			keys_down(pygame.K_s) = False
		elif listener.get_key(pygame.K_s) and not keys_down(pygame.K_s):
			self.data["mouth"] = "open"
			keys_down(pygame.K_s) = True
		else:
			pass

		#render state = dir + frame + (state + "_" + mouth)

class Prop(Mob):
	#animated or static objects
	#create composites of the movement and animation controls
	#up - reduce scale + reduce draw order + dir(back) + animate
	#down - increase scale + increase draw order + dir(fore) + animate
	#left - reduce X_pos + dir(left) + animate
	#right - increase X_pos + dir(right) + animate
	#[ - decrease Y_pos (flying characters?)
	#] - increase Y_pos
	#q = state("default")
	#w = state("broken")
	#e = state("fire")
	#r = state("open")
	def __init__(self, x_pos, y_pos, w, h, draw_order, framerate, len_frames):
		Mob.__init__(self, x_pos, y_pos, w, h, draw_order, framerate, len_frames)


