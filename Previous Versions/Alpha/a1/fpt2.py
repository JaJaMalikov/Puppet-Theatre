#!/usr/bin/env python2

import pygame
from pygame.locals import *
#import pygame.gfdraw
import pygame.font
import math
import time
import copy
import sys
import os
from collections import OrderedDict

from pygame.locals import Color

######################primitive functions####################
def parse_settings(file_name):
	settings_text = open(file_name,"r").read()

	settings_text = settings_text.split("\n")
	settings_data = {}
	for setting in settings_text:
		key,value = setting.split("=")
		try:
			settings_data[key] = int(value)
		except:
			settings_data[key] = value
	return settings_data

def rotate(surface, angle, pivot, offset):
	"""Rotate the surface around the pivot point.

	Args:
		surface (pygame.Surface): The surface that is to be rotated.
		angle (float): Rotate by this angle.
		pivot (tuple, list, pygame.math.Vector2): distance from upper left corner of the destination
		offset (pygame.math.Vector2): distance from center 0,0 being center -1,-1, being just to the upper left.
	"""
	rotated_image = pygame.transform.rotozoom(surface, -angle, 1)  # Rotate the image.
	rotated_offset = offset.rotate(angle)  # Rotate the offset vector.
	# Add the offset vector to the center/pivot point to shift the rect.
	rect = rotated_image.get_rect(center=pivot+rotated_offset)
	return rotated_image, rect  # Return the rotated image and shifted rect.

#########################classes##########################

class stage:
	def __init__(self, production, objects):
		self.production = production
		self.background = OrderedDict()
		self.props = OrderedDict()
		self.actors = OrderedDict()
	def update(self):
		for key in background.keys():
			background[key].update()
		for key in props.keys():
			props[key].update()
		for key in actors.keys():
			actors[key].update()
	def add_background(self, name, back_object):
		self.background[name] = back_object
	def add_prop(self, name, prop):
		self.props[name] = prop
	def add_actor(self, name, actor):
		self.props[name] = actor

class entity:
	def __init__(self, production, screensize, name, x, y, on_count, horizon, dist):
		self.name = name
		self.production = production
		self.horizon = horizon
		self.dist = dist
		self.X_offset = 0
		self.Y_offset = 0
		self.set_pos(x,y)
		self.get_array()
		self.cur_frame = 0
		self.on_count = on_count
		self.cur_count = 0
		self.screensize = screensize
		self.start()

	def set_pos(self,X, Y):
		self.X = X
		self.Y = Y
	def get_pos(self):
		return [self.X-self.X_offset, self.Y-self.Y_offset]
	def update(self):
		pass
	def get_array(self):
		pass
	def get_surf(self):
		pass
	def get_settings(self):
		pass #return all settings of entity
	def set_settings(self):
		pass #return all possible settings of entity

class stat(entity):
	def start(self):
		self.shift = 0
		self.plane = 0
		self.dist = 0

	def get_array(self):
		self.rig = parse_settings("%s/%s/rig" % (self.production, self.name))
		self.main_surface = pygame.Surface((self.rig["width"], self.rig["height"]),pygame.SRCALPHA, 32)
		self.main_rect = self.main_surface.get_rect()
		self.array = []
		for img in range(self.rig["frames"]):
			self.array.append(pygame.image.load("%s/%s/%s.png" % (self.production, self.name, str(img))))
		self.X_offset = self.rig["width"]/2
		self.Y_offset = self.rig["height"]/2

	def update(self):
		self.check_pos()
		self.main_surface.fill((0,0,0,1))
		self.cur_count += 1
		if self.cur_count == self.on_count:
			self.cur_count = 0
			self.cur_frame += 1
			if self.cur_frame == self.rig["frames"]:
				self.cur_frame = 0

		temp_rect = self.array[self.cur_frame].get_rect(center = self.main_rect.center)
		self.main_surface.blit(self.array[self.cur_frame], temp_rect)

	def get_surf(self):
		return self.array[self.cur_frame]

class background(stat):
	def check_pos():
		pass
	def set_pan_x(self,offset):
		self.X_offset = offset
	def set_pan_y(self,offset):
		self.Y_offset = offset

class prop(stat):
	def check_pos():
		#self.
		pass
	def set_dist(self, offset):
		self.dist = offset
		#self.plane = 
	def set_shift(self, offset):
		self.shift = offset
		self.X_offset = self.screensize
	def set_plane(self, offset):
		self.plane = offset
	def next_frame(self):
		self.cur_frame += 1
	def prev_frame(self):
		self.cur_frame -= 1

class mob(entity):
	def start(self):
		self.width = self.rig["width"]
		self.height = self.rig["height"]
		self.mood = "default"
		self.flip = False
		self.angle = 0

	def update(self):
		pass

	def get_surf(self):
		return pygame.transform.smoothscale(display, ())


#################################settings#################

title = "Laughware Finger Puppet Theatre"
height = 1080
width = 1920

scrw_chunk = int(width/20)
scrh_chunk = int(height/20)

scrw = scrw_chunk*14
scrh = scrh_chunk*14

fps = 30
font = "freesansbold.ttf"
horizon = 600

#####consts

white = Color('white')
black = Color('black')
blue = Color('blue')
green = (0,119,5,255)


########################setup pygame#######################

pygame.init()
pygame.display.set_caption(title)
screen = pygame.display.set_mode((scrw,scrh),DOUBLEBUF|HWSURFACE)
main_surface = pygame.Surface((width,height), pygame.SRCALPHA,32)
stage_surface = None

font=pygame.font.Font('freesansbold.ttf',12)
clock = pygame.time.Clock()
frame = 0

entities = OrderedDict()
#entities["sky"] = background("test", (width, height), "sky", width/2,height/2, 2, horizon,1)
#entities["grass"] = background("test",(width, height), "grass", width/2,height/2, 1, horizon,1)
#entities["vase"] = prop("test",(width, height), "vase", width/2,height/2, 1, horizon,1)

while True:
	clock.tick(fps)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.display.quit()
			pygame.quit()
			sys.exit()

	for key in entities.keys():
		entities[key].update()

	for key in entities.keys():
		main_surface.blit(entities[key].get_surf(), entities[key].get_pos())

	screen.blit(main_surface,(0,0))
	pygame.display.flip()
	frame += 1

############################end new###################
###########################begin old##################

chars = {"atlas":atlas.model}#, "bee":bee.model}


pygame.init()

width = 1920
height = 1080

scrw_chunk = int(width/20)
scrh_chunk = int(height/20)

scrw = scrw_chunk*14
scrh = scrh_chunk*14

font = pygame.font.Font('freesansbold.ttf', 12)
clock = pygame.time.Clock()
frame = 0

#consts

pos_block = width/7
scale = 2
sprite_h = 822 * scale
sprite_w = 500 * scale

eye_shapes = {"default": [0,0],
				"happy": [170,70],
				"confused": [290,170],
				"angry":[20,250],
				"bored":[340,200]
}
moods = {pygame.K_q:"default",
		pygame.K_w:"angry",
		pygame.K_e:"confused",
		pygame.K_r:"happy",
		pygame.K_t:"bored"
}
sizes = {
	pygame.K_z:0.08,
	pygame.K_x:0.16,
	pygame.K_c:0.2,
	pygame.K_v:0.3,
	pygame.K_b:0.8
}
char_pos = {
	pygame.K_a:pos_block*1,
	pygame.K_s:pos_block*2,
	pygame.K_d:pos_block*3,
	pygame.K_f:pos_block*4,
	pygame.K_g:pos_block*5,
	pygame.K_h:pos_block*6,
}
angles = {pygame.K_KP8:0.0,
		pygame.K_KP7:45.0,
		pygame.K_KP4:90.0,
		pygame.K_KP1:135.0,
		pygame.K_KP2:180.0,
		pygame.K_KP3:225.0,
		pygame.K_KP6:270.0,
		pygame.K_KP9:315.0
}

#rendering functions

def degree_map(degree):
	if degree < 180:
		return 90 - (degree-90)
	elif degree > 180:
		return 270 + (270-degree)
	else: return 0

slideshow_visible = True
slideshow = []
slide= 0
filelist = os.listdir("res/slides")
filelist.sort()
for file in filelist:
	try:
		slideshow.append(pygame.image.load("res/slides/" + file))
	except:
		pass

objects = {}
images = {}

objects["atlas"] = {}
objects["bee"] = {}

images["atlas"] = {}
images["bee"] = {}

objects["slide"] = 0
objects["slideshow_visible"] = True

current_char = 0

for obj in chars.keys():
	images[obj]["sprite"] = {}
	objects[obj]["mood"] = "default"
	objects[obj]["pos"] = pos_block
	objects[obj]["flip"] = False
	objects[obj]["size"] = sizes[pygame.K_x]
	objects[obj]["angle"] = 0
	for mood in eye_shapes.keys():
		images[obj]["sprite"][mood] = pygame.Surface((sprite_w, sprite_h), pygame.SRCALPHA,32)
		images[obj]["sprite"][mood] = images[obj]["sprite"][mood].convert_alpha()
		render_image(images[obj]["sprite"][mood], chars[obj])
		render_eyes(images[obj]["sprite"][mood], eye_shapes[mood][0], eye_shapes[mood][1])

folder = 0
for obj in chars.keys():
	for mood in eye_shapes.keys():
		for size in sizes.keys():
			display = images[obj]["sprite"][mood]
			display.blit(display,(0,0))
			current_h = int(display.get_height() * sizes[size])
			current_w = int(display.get_width() * sizes[size])


			pygame.image.save(pygame.transform.smoothscale(display, ( current_w, current_h)), str(folder) + "/" + mood + ".png") 
			folder += 1
		folder = 0


log = []
playback = False
recording = False


while True:
	clock.tick(21)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.display.quit()
			pygame.quit()
			sys.exit()

		#keydown states, gotta package these into some kind of dictionary
		#this group conveys mood
		#key: q = normal, w = angry, e = confused, r = happy, t = bored
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_l:
				playback = not playback
				frame = 0
			if event.key == pygame.K_SEMICOLON:
				if recording:
					recording = False
				else:
					log = []
					recording = True

			if event.key == pygame.K_UP:
				objects["slideshow_visible"] = True
			if event.key == pygame.K_DOWN:
				objects["slideshow_visible"] = False
			if event.key == pygame.K_LEFT:
				objects["slide"] -= 1
			if event.key == pygame.K_RIGHT:
				objects["slide"] += 1

			if event.key in moods:
				objects[chars.keys()[current_char]]["mood"] = moods[event.key]

			#zoom states, z = tiny, x = indicating, c = lecture, v = emphasis, b = pleading
			if event.key in sizes:
				objects[chars.keys()[current_char]]["size"] = sizes[event.key]

			#position states, asdfgh each yeild 1/7 position each
			if event.key in char_pos:
				objects[chars.keys()[current_char]]["pos"] = char_pos[event.key]

			if event.key in angles:
				objects[chars.keys()[current_char]]["angle"] = angles[event.key]


			#misc instructions, left bracket flips the current character, -= shrink and grow character
			if event.key == pygame.K_LEFTBRACKET:
				objects[chars.keys()[current_char]]["flip"] = not objects[chars.keys()[current_char]]["flip"]

			if event.key == pygame.K_EQUALS:
				objects[chars.keys()[current_char]]["size"] += 0.1
			if event.key == pygame.K_MINUS:
				objects[chars.keys()[current_char]]["size"] -= 0.1

			#switches active character as desired, 1 is atlas, 2 is queen bee
			if event.key == pygame.K_1:
				current_char = 0
			if event.key == pygame.K_2:
				current_char = 1

	main_surface.fill(white)
	screen.fill((200,200,200))

	if recording:
		log.append(copy.deepcopy(objects))
	if playback:
		if frame>=len(log):
			playback = False
		else:
			objects = copy.deepcopy(log[frame])

	if objects["slideshow_visible"]:
		main_surface.blit(slideshow[objects["slide"]], pygame.rect.Rect(0,0,0,0))#(620,100, 0,0))

	for char in chars.keys():
		current_y = 750-(sprite_h* objects[char]["size"])/2

		display = images[char]["sprite"][objects[char]["mood"]]
		if objects[char]["flip"]:
			display = pygame.transform.flip(display, True, False)
		if objects[char]["angle"] != 0:
			display = pygame.transform.rotate(display, objects[char]["angle"])

		current_h = int(display.get_height() * objects[char]["size"])
		current_w = int(display.get_width() * objects[char]["size"])

		display = pygame.transform.smoothscale(display, ( current_w, current_h)) 
		current_x = objects[char]["pos"] - display.get_width()/2

		main_surface.blit(display, (current_x,current_y))

	if playback:
		pygame.image.save(main_surface, "frames/{0:03d}".format(frame) + ".png")

	stage_surface = pygame.transform.smoothscale(main_surface, (scrw_chunk*12,scrh_chunk*12))
	screen.blit(stage_surface,(scrw_chunk,scrh_chunk))
	screen.blit(font.render("FPS:" + str(int(clock.get_fps())), True, black),(0,0))
	screen.blit(font.render("Recording: " + str(recording), True, black), (0,20))
	screen.blit(font.render("Playback: " + str(playback), True, black), (0,40))
	pygame.display.flip()

	frame += 1

