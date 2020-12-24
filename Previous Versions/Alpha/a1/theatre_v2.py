import pygame
import time
import sys
import os
import random
from collections import OrderedDict
from collections import deque
import json
import copy

###########################################################Design Doc###############################################
"""

#####################################################################
#   FPS   #    Chr1 Chr2 Chr3 Chr4 Chr5 Chr6 Chr7 Chr8 Chr9 Chr10   #
#####################################################################
# record X#                                                         #
# play   X#                                                         #
# render X#                                                         #
#         #                                                         #
#         #                                                         #
#         #                                                         #
#         #                                                         #
#         #                                                         #
#         #                                                         #
#         #                                                         #
#         #                                                         #
#####################################################################
#                                                                   #
#                                                                   #
#                                                                   #
#####################################################################

objective: to create a theatre like environment wherein the characters within a "stage" environment are directed to act
	inactive characters will remain "offstage", so that they can be selected and brought in at a moment's notice using 
	commands up to ten controllable characters can be on or off stage at one time.
	an icon of them with a number will be at the top of the screen so that one can see which character is selected.

Implementation:
	entities on the stage record their current state internally while recording is true, while being manipulated
	once recording is not true they keep that record until manipulated again, playback sends the update signal
	to each entity, if the entity has nothing recorded they do nothing

	if they do then the internal framecount is set to 0 and each frame the update function is called, setting the frame
	+1 so that they move through every programmed motion, once all actors have their instructions the render function
	can be called.

keys:
	the  keys at the top of the keyboard select the actor
	the arrow keys control movement, left and right for horizontal movement, up and down control distance to "camera"
	numpad controls angle
	qwerty controls emotional state: q=default, w=happy, e=angry, r=sad, t=surprise
	a opens mouth, down is open-up is closed
	s toggles the mouth open
	d causes animated action based on current emotional state
	\ key tabs between props
	- key previous frame of current prop
	= key next frame of current prop
	/ record
	. playback
	, render (ask are you sure?)
	
	==to do==
	control camera as seperate entity
	center camera on actor
	zoom camera (distinct states or numerical?)

structure:
	theatre:
		holds the camera, stage, off stage, character selector, framerate control, key listener

	key listener:
		keeps the current set of key states for every entity to reference (0-255)

	camera(entity):
		keeps a 1080p frame aimed at the stage, can zoom in or out, can lock onto a character or be driven by hand
		locking on a character while animating can givethe impression of the background moving

	stage:
		collection of all active entities on stage
			background(entity)
			foreground(entity)
			props(entity)
			actors(entity)

	off stage:
		inactive entities are stored here, mearly for reference

	character selector:
		bar at the top which shows each character with currently active characters high lighted

	framerate control:
		entity which displays framerate and sets it for the game, turns red if framerate drops

	entity:
		class which all playable objects are based on
		takes input controls and can record it's current state
		if recorded frames are present then when not recording it will cycle through them starting at playback
		recorded content is cleared when recording is turned on again
		recording is only active when hitting record during selected entity
		only records frames during update -> playback
	
"""

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


##########################################################utility functions ########################################

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
	imageset = []
	filelist = os.listdir("res/" + name)
	print(filelist)
	filelist.sort()
	print(filelist)
	for file in filelist:
		try:
			imageset.append(pygame.image.load("res/" + name + "/" + file))
		except:
			pass
	return imageset


###########################################################Object classes ##########################################

"""
entity -> sprite
	self.data = {}
		pos - x, y coordinates on the stage frame NOT ABSOLUTE POSITION (int, int)
		size - w,h on the stage NOT ABSOLUTE POSITION (int,int)
		draw_order - draw order in the form of a float from 0.0 - 1.0
		current_frame - current animated frame, int 0 - max length of frames
	self.record = [self.data,self.data]
	self.instructions -> set of instructions, static or otherwise which tells the objects how to change

	update() -> update all data by instructions

background -> entity
	self.images = [animated frames in linear slideshow form] [pygame.Surface]

mob -> entity
	direction controls - control x,y post on screen
	dist control - control the distance to the screen
	invert direction - gives moonwalk and retreating ability
	strafing - move without changing direction, perhaps a boolean
	animated - bool, is currently animated no matter what
	next frame 
	prev frame

	input(listener) -> if listener is None skip input

	self.data{}
		dir - currently facing direction, int
		dist - distance from camera, linked to draw_order and scale, float
		scale - size of the image reletive to the size of the stage, linked to dist and draw order, float
		state - current state of the entity (emotion, broken etc), string
	self.images = {"state" : [[animated frames in linear slidesho form], direction array ]} dict of arrays of arrays

actor -> mob
	compositor from instructions to generate unique characters	
	
prop -> mob
	static objects which can take any input, movement does not trigger animation
	no composition, only takes static image sets from premade sets, each animation is taken from still images
		name of the states is the name of the sprite sheets, ALL SPRITE SHEETS MUST BE IDENTICAL IN SIZE

"""

class Entity(pygame.sprite.Sprite):
	def __init__(self, name, char_imgs, layer_colors, layers, width, height, x_pos, y_pos, frames, framerate, speed, scale, angle):
		pygame.sprite.Sprite.__init__(self)
		self.record = []
		self.is_recording = False
		self.cur_frame = 0

		self.data = OrderedDict()
		self.data["scale"] = scale
		self.data["angle"] = angle
		self.data["layer_colors"] = layer_colors
		self.data["char_imgs"] = char_imgs
		self.data["layers"] = layers
		self.data["rect"] = pygame.Rect(0,0, width, height)
		self.data["rect"].center = (x_pos, y_pos)
		self.data["dir"] = 0
		self.data["frame"] = 0
		self.data["counter"] = 0
		self.data["cur_frame"] = 0

		self.speed = speed

		self.rec_key_down = False
		self.ret_surf = None
		self.name = name
		self.width = width
		self.height = height
		self.frame = 0
		self.frames = frames
		self.framerate = framerate
		self.ss = None
		self.portrait = None
		self.composite()
		self.change_scale()
		self.playback = False

	#get and set methods:

	def reset_playback(self):
		self.frame = 0

	def record(self):
		self.recording = True
		self.record = []
		self.reset_playback()

	def get_playback(self):
		return self.playback

	def get_rect(self):
		return self.data["rect"]

	def set_pos(self, x_pos, y_pos):
		self.data["rect"] = pygame.Rect(x_pos, y_pos, self.width, self.height)

	def get_portrait(self):
		#return self.portrait
		port_surf = pygame.Surface([int(self.width/2), int(self.width/2)], pygame.SRCALPHA, 32).convert_alpha()
		port_surf.blit(self.get_image()[0], (int(self.width/4),0))
		return port_surf

	def get_image(self):
		#return rotate(
		#	self.ss.subsurface(
		#		pygame.Rect(self.data["frame"] * self.width, self.data["dir"] * self.height, self.width, self.height)),
		#		self.data["angle"],
		#		self.data["rect"].center, pygame.math.Vector2((0,0)),  self.data["scale"])
		#return pygame.transform.rotozoom(, self.data["angle"], self.data["scale"])
		#self.ret_surf.fill
		self.ret_surf.set_alpha(255)

		pygame.transform.smoothscale(
			self.ss.subsurface(
				pygame.Rect(
					self.data["frame"]*self.width,
					self.data["dir"]*self.height,
					self.width,self.height)),
				(int(self.width*self.data["scale"]), 
				int(self.height*self.data["scale"])),
					self.ret_surf)

		#new_rect = pygame.Rect(self.data["rect"].x *self.data["scale"], self.data["rect"].y *self.data["scale"], self.data["rect"].w, self.data["rect"].h)

		return self.ret_surf, self.data["rect"]

	def get_center(self):
		return self.rect.center

	#image manipulation methods

	def composite(self):
		"""
		open sprite sheets as layers, each with transparent body parts/clothing
		create surface with color according to provided key
		merge all colored layers onto main surface using key to make background transparent
		"""
		self.ss = pygame.Surface([self.frames*self.width, self.height*4], pygame.SRCALPHA, 32).convert_alpha()
		#self.portrait = pygame.image.load("res/char_res/" + name + "_port.png").convert_alpha()
		color_sheet = pygame.Surface([self.frames*self.width, self.height*4], 32)
		color_sheet.set_colorkey((255,255,255))
		layers = self.data["layers"]
		for layer in range(len(layers)):
			color_sheet.fill(self.data["layer_colors"][layer])
			color_sheet.blit(pygame.image.load("res/char_res/" + layers[layer] + "/" + str(self.data["char_imgs"][layer])+ ".png" ), (0,0))
			self.ss.blit(color_sheet, (0,0))

	def change_scale(self):
		self.ret_surf = pygame.Surface((int(self.width*self.data["scale"]), int(self.height*self.data["scale"])),pygame.SRCALPHA, 32).convert_alpha()
		center = self.data["rect"].center
		self.data["rect"].size = (int(self.width*self.data["scale"]),int(self.height*self.data["scale"]))
		self.data["rect"].center = center

	#update methods

	def update(self):
		if self.is_recording:
			self.record.append(copy.deepcopy(self.data))
		elif len(self.record) > 0:
			print("record len " + str(len(self.record)) + ": current frame " + str(self.frame))

			self.frame += 1
			if self.frame >= len(self.record):
				self.frame = 0
			self.data = self.record[self.frame]
			self.change_scale()
			self.playback = True
		else:
			pass

	def next_frame(self):
		self.data["frame"] += 1
		if self.data["frame"] == self.frames:
			self.data["frame"] = 0

	def prev_frame(self):
		self.data["frame"] -= 1
		if self.data["frame"] < 0:
			self.data["frame"] = self.frames-1

	def change_dir(self, dir):
		self.data["dir"] = dir

	def render_frame(self):
		self.data["counter"] += 1
		if self.data["counter"] == self.framerate:
			self.data["counter"] = 0
			self.next_frame()

	def move_up(self):
		self.data["dir"] = 2
		self.data["scale"] *= .98
		self.change_scale()
		#self.data["rect"] = self.data["rect"].move(0,-self.speed)
		self.render_frame()
	def move_left(self):
		self.data["dir"] = 1
		self.data["rect"] = self.data["rect"].move(-int(self.speed*self.data["scale"]),0)
		self.render_frame()
	def move_down(self):
		self.data["dir"] = 0
		self.data["scale"] *= 1.02
		#self.data["rect"] = self.data["rect"].move(0,self.speed)
		self.change_scale()
		self.render_frame()
	def move_right(self):
		self.data["dir"] = 3
		self.data["rect"] = self.data["rect"].move(int(self.speed*self.data["scale"]),0)
		self.render_frame()
	def be_still(self):
		self.data["frame"] = 0

	def input(self, listener):
		#movement key strokes only
		if listener.get_key(pygame.K_UP):
			self.move_up()
		elif listener.get_key(pygame.K_LEFT):
			self.move_left()
		elif listener.get_key(pygame.K_DOWN):
			self.move_down()
		elif listener.get_key(pygame.K_RIGHT):
			self.move_right()
		else:
			self.be_still()

		#use as template for toggle keys
		if listener.get_key(96):
			if not self.rec_key_down:
				self.is_recording = not self.is_recording
				self.rec_key_down = True
		else:
			self.rec_key_down = False


class Mob(Entity):
	def __init__(self, name, char_imgs, layer_colors, layers, width, height, x_pos, y_pos, frames, framerate, speed, scale, angle):
		Entity.__init__(self, name, char_imgs, layer_colors, layers, width, height, x_pos, y_pos, frames, framerate, scale, angle)


"""
object class functions
sprite:
	update
	add
	remove
	kill
	alive
	groups
entity(sprite):
	update
	get_rect
	set_pos
	get_image
	next_frame
	change_dir
Mob(entity):
	move_up
	move_left
	move_down
	move_right
	be_still
Player(Mob):
	input
NPC(Mob):
	random_walk
"""
class Actor(Mob):
	def __init__(self, name, x_pos, y_pos, char_imgs, layer_colors, scale, angle):
		Mob.__init__(self, name, char_imgs, layer_colors, ["body","eyes","fhair"],64,64,x_pos, y_pos,4, 2, 4, scale, angle)

class Background:
	def __init__(self, name, x_pos, y_pos, counter):
		self.data = {}
		self.data["name"] = name
		self.data["x_pos"] = x_pos
		self.data["y_pos"] = y_pos
		self.data["frame"] = 0
		self.imageset = load_imageset(name)
		self.data["rect"] = self.imageset[0].get_rect()
		self.count = 0
		self.counter = counter

	def get_rect(self):
		return self.data["rect"]

	def update(self):
		self.count += 1
		if self.count == self.counter:
			self.count  = 0
			self.data["frame"] += 1
			if self.data["frame"] == len(self.imageset):
				self.data["frame"] = 0

	def get_image(self):
		return self.imageset[self.data["frame"]]#, self.data["rect"]

	def reset_playback(self):
		self.data["frame"] = 0

class Prop:
	def __init__(self, name, x_pos, y_pos, speed):
		self.data = {}
		self.data["name"] = name
		self.data["x_pos"] = x_pos
		self.data["y_pos"] = y_pos
		self.data["frame"] = 0
		self.imageset = load_imageset(name)
		self.data["rect"] = self.imageset[0].get_rect()
		self.data["rect"].x = self.data["x_pos"]
		self.data["rect"].y = self.data["y_pos"]
		self.toggle_keys = {pygame.K_RIGHTBRACKET:False, pygame.K_LEFTBRACKET:False, 96:False}
		self.recording = False
		self.record = []
		self.cur_frame = 0
		self.speed = speed

	def reset_playback(self):
		self.cur_frame = 0

	def get_image(self):
		return self.imageset[self.data["frame"]], self.data["rect"]

	def update(self, listener):
		if not self.recording and len(self.record) > 0:
			self.data=self.record[self.cur_frame]
			self.cur_frame += 1
			if self.cur_frame == len(self.record):
				self.cur_frame = 0
		else:
			#advance one frame
			if (self.toggle_keys[pygame.K_RIGHTBRACKET]) and not listener.get_key(pygame.K_RIGHTBRACKET):
				self.toggle_keys[pygame.K_RIGHTBRACKET] = False
			if listener.get_key(pygame.K_RIGHTBRACKET) and not self.toggle_keys[pygame.K_RIGHTBRACKET]:
				self.data["frame"] += 1
				if self.data["frame"] == len(self.imageset):
					self.data["frame"] = 0
				self.toggle_keys[pygame.K_RIGHTBRACKET] = True		
			#back one frame
			if (self.toggle_keys[pygame.K_LEFTBRACKET]) and not listener.get_key(pygame.K_LEFTBRACKET):
				self.toggle_keys[pygame.K_LEFTBRACKET] = False
			if listener.get_key(pygame.K_LEFTBRACKET) and not self.toggle_keys[pygame.K_LEFTBRACKET]:
				self.data["frame"] -= 1
				if self.data["frame"] < 0:
					self.data["frame"] = len(self.imageset)-1
				self.toggle_keys[pygame.K_LEFTBRACKET] = True

			if listener.get_key(pygame.K_w):
				self.data["rect"].y -= self.speed
			elif listener.get_key(pygame.K_a):
				self.data["rect"].x -= self.speed
			elif listener.get_key(pygame.K_s):
				self.data["rect"].y += self.speed
			elif listener.get_key(pygame.K_d):
				self.data["rect"].x += self.speed
			else:
				pass

			if (self.toggle_keys[96]) and not listener.get_key(96):
				self.toggle_keys[96] = False
			if listener.get_key(96) and not self.toggle_keys[96]:
				if self.recording:
					self.recording = False
				else:
					self.recording = True
					self.record = []
				self.toggle_keys[96] = True	

		if self.recording:
			self.record.append(copy.deepcopy(self.data))


#########################################################stage class
""" host for all background images, actors, and props """
"""note: create props, import background"""



class Stage:
	def __init__(self, bg_color, width, height, horizon, scale, speed):
		self.data = {}
		self.data["selected"] = 0
		self.data["X_offset"] = 0
		self.data["Y_offset"] = 0
		self.data["zoom"] = 1

		self.record = []
		self.render = False

		self.camera_control = True
		##toggle keys:
		self.toggle_keys = {pygame.K_KP_ENTER:False, 96:False, 111:False}

		self.speed = speed
		self.scale = scale
		self.horizon = int(horizon)
		self.background_colour = bg_color
		(self.width, self.height) = width, height
		#self.background = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32).convert_alpha()
		#self.background = pygame.image.load("bg.png").convert()
		self.background = Background("bg_sunny", 0,0,10)
		self.dots = Prop("dots", 400, int(self.horizon*scale), 10)
		self.camera = pygame.Surface((int(self.width*self.scale), int(self.height*self.scale)), pygame.SRCALPHA, 32).convert_alpha()

		self.data["bg_rect"] = self.background.get_rect()
		self.data["cam_rect"] = self.camera.get_rect()


		self.actors = []
		self.actor_guild = pygame.sprite.Group()
		self.default_order = [x for x in range(0,10)]
		self.draw_order = [x for x in range(0,10)]

		self.frame = 0
		self.num_actors = 1

		for x in range(self.num_actors):
			self.actors.append(Entity(
				"Actor", 
				[0,0,0], 
				[(200,100,100),(100,100,200),(100,200,100)], 
				["body","eyes","fhair"],
				64,
				64,
				300,
				0,
				4, 
				2, 
				4,
				self.scale,
				0))
			self.actor_guild.add(self.actors[x])



	def get_portaits(self):
		return [act.get_portrait() for act in self.actors]

	def set_controlled(self, selected):
		self.data["selected"] = selected

	def get_controlled(self):
		return self.data["selected"]

	def update(self, listener):

		for key in [48,49,50,51,52,53,54,55,56,57]:
			if listener.get_key(key):
				self.data["selected"] = key-48
		if listener.get_key(pygame.K_p):
			for actor in self.actors: actor.reset_playback()

		#toggles recording playback
		if (self.toggle_keys[96]) and not listener.get_key(96):
			self.toggle_keys[96] = False
		if listener.get_key(96) and not self.toggle_keys[96]:
			for actor in self.actors: actor.reset_playback()
			self.toggle_keys[96] = True

		#toggles render playback
		if (self.toggle_keys[111]) and not listener.get_key(111):
			self.toggle_keys[111] = False
		if listener.get_key(111) and not self.toggle_keys[111]:
			#self.scale = 1
			for actor in self.actors: actor.reset_playback()
			#for actor in self.actors: actor.data["scale"] = self.scale
			#for actor in self.actors: actor.change_scale()
			self.render = True
			self.frame = 0
			#self.camera = pygame.Surface((int(self.width*self.scale), int(self.height*self.scale)), pygame.SRCALPHA, 32).convert_alpha()
			self.toggle_keys[111] = True

		#toggles camera controls
		if (self.toggle_keys[pygame.K_KP_ENTER]) and not listener.get_key(pygame.K_KP_ENTER):
			self.toggle_keys[pygame.K_KP_ENTER] = False
		if listener.get_key(pygame.K_KP_ENTER) and not self.toggle_keys[pygame.K_KP_ENTER]:
			self.camera_control = (not self.camera_control)
			self.toggle_keys[pygame.K_KP_ENTER] = True

		self.dots.update(listener)
		self.actor_guild.update()
		self.background.update()

		if (not self.actors[self.data["selected"]].get_playback()):
			self.actors[self.data["selected"]].input(listener)

		#self.bg_rect.center = self.actors[self.selected].data["rect"].center

		self.draw_order = [x for _, x in sorted(zip(self.actors,self.default_order), key=lambda x: x[0].data["scale"] )]

		if self.camera_control:
			if listener.get_key(pygame.K_KP_MINUS):
				self.data["X_offset"] -= self.speed
			elif listener.get_key(pygame.K_KP_PLUS):
				self.data["X_offset"] += self.speed
			elif listener.get_key(pygame.K_KP_DIVIDE):
				self.data["Y_offset"] -= self.speed
				#self.data["zoom"] -= .01
			elif listener.get_key(pygame.K_KP_MULTIPLY):
				self.data["Y_offset"] += self.speed
				#self.data["zoom"] += .01
			else:
				pass
		else:
			self.data["X_offset"] = self.actors[self.data["selected"]].data["rect"].centerx

	def get_camera(self):
		#self.full_stage.fill(self.background_colour)

		#background size and position data
		self.frame += 1

		bg_w = int(self.data["bg_rect"].w * self.scale)
		bg_h = int(self.data["bg_rect"].h * self.scale)
		bg_x_pos = self.data["cam_rect"].x-int(self.data["X_offset"])
		bg_y_pos = self.data["cam_rect"].y#-int(self.data["Y_offset"])  + int(self.height*self.scale/2)
		cam_w = self.data["cam_rect"].w
		cam_h = self.data["cam_rect"].h

		self.camera.blit(pygame.transform.smoothscale(self.background.get_image(),( bg_w, bg_h )), 
						pygame.Rect(bg_x_pos, bg_y_pos, cam_w, cam_h))

		for x in range(self.num_actors):
			image, rect = self.actors[self.draw_order[x]].get_image()

			#character size and position data
			char_w = int(rect.w)
			char_h = int(rect.h)
			char_x_pos = (rect.x-int(self.data["X_offset"]/self.data["zoom"])) + int(self.width*self.scale/2)
			char_y_pos = rect.y + self.horizon * self.scale

			self.camera.blit(pygame.transform.smoothscale(image, ( char_w, char_h )),
			pygame.Rect(char_x_pos, char_y_pos, char_w , char_h))

		image, rect = self.dots.get_image()
		print(rect)
		self.camera.blit(image, rect)

		#if self.scale == 1:
		if self.render:
			pygame.image.save(pygame.transform.smoothscale(self.camera, (1920,1080)), "D:/frames/{0:05d}".format(self.frame) + ".png")
		return self.camera
		#else:
		#	return pygame.transform.scale(self.camera, (int(self.data["cam_rect"].w*self.scale),int(self.data["cam_rect"].h*self.scale)) )

class Editor:
	def __init__(self):
		pygame.init()
		self.white = pygame.Color('white')
		self.black = pygame.Color('black')
		self.blue = pygame.Color('blue')
		self.green = (0,119,5,255)
		self.font_size = 24
		self.font = pygame.font.Font('freesansbold.ttf', self.font_size)

		self.bg_color = (255,255,255)
		self.name = "Laughware Finger Puppet Theatre"
		self.icon = "icon.png"
		self.width, self.height = 960,540
		self.off_x = 200
		self.off_y = 100
		self.win_width = self.width + (self.off_x*2)
		self.win_height = self.height + (self.off_y * 2)
		self.screen = pygame.display.set_mode((self.win_width, self.win_height))
		pygame.display.set_caption(self.name)
		pygame.display.set_icon(pygame.image.load(self.icon))

		self.running = True
		self.clock = pygame.time.Clock()
		self.framerate = 30

		self.listener = key_listener()
		self.stage = Stage(self.bg_color, 1920, 1080, 700, .5, 10)
		self.port_disp = None
		self.port_center = (0,0)
		self.port_w = 0
		self.cur_actor = 0
		self.gen_portraits()

	def gen_portraits(self):
		portraits = self.stage.get_portaits()
		h = int(portraits[0].get_height())
		w = int(portraits[0].get_height()*10)
		self.port_center = portraits[0].get_rect().center
		self.port_w = h
		self.port_disp = pygame.Surface( (w, h), pygame.SRCALPHA, 32).convert_alpha()
		for port in range(len(portraits)):
			self.port_disp.blit(portraits[port], (int(portraits[0].get_height()*port), 0))


	def run(self):
		while self.running:
			self.clock.tick(self.framerate)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
				if event.type == pygame.KEYDOWN:
					self.listener.set_keydown(event.key)
				if event.type == pygame.KEYUP:
					self.listener.set_keyup(event.key)
			self.stage.update(self.listener)
			self.screen.fill(self.bg_color)

			self.screen.blit(self.font.render("FPS:" + str(int(self.clock.get_fps())), True, self.black),(0,0))
			self.screen.blit(self.stage.get_camera(), (self.off_x,self.off_y))
			self.screen.blit(self.port_disp, (self.off_x, 0))
			pygame.draw.circle(self.screen, self.blue, (self.port_center[0] + (self.port_w * self.stage.get_controlled()) + self.off_x, self.port_center[1]), self.port_center[0])

			pygame.display.flip()
		pygame.display.quit()
		pygame.quit()
		sys.exit()


if __name__ == "__main__":
	editor = Editor()
	editor.run()
	#rungame()
	#game = game("game.json")
	#game.run()
