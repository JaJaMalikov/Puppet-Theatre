#!/usr/bin/env python2

import pygame
from pygame.locals import *
import pygame.gfxdraw
import pygame.font
import math
import time
import copy
import sys
import os


from pygame.locals import Color

pygame.init()

width = 1920
height = 1080

scrw_chunk = int(width/20)
scrh_chunk = int(height/20)

scrw = scrw_chunk*14
scrh = scrh_chunk*14

screen = pygame.display.set_mode((scrw,scrh),DOUBLEBUF|HWSURFACE)
main_surface = pygame.Surface((int(width/4),int(height/4)), pygame.SRCALPHA,32)
stage_surface = None
font = pygame.font.Font('freesansbold.ttf', 12)
clock = pygame.time.Clock()
frame = 0

pos_block = width/7
scale = .5

folders = ["mild", "furrow", "pixar", "surprise", "worried"]
imgs = ["ah", "sss", "mhmm", "smile", "ooh"]

char_imgs = {}



moods = {pygame.K_q:"mild",
		pygame.K_w:"furrow",
		pygame.K_e:"pixar",
		pygame.K_r:"surprise",
		pygame.K_t:"worried"}

mouth = {pygame.K_y:"ah",
		pygame.K_u:"ooh",
		pygame.K_i:"sss",
		pygame.K_o:"mhmm",
		pygame.K_p:"smile"}

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

slideshow_visible = True
slideshow = []
slide= 0
filelist = os.listdir("slides")
filelist.sort()
for file in filelist:
	try:
		slideshow.append(pygame.image.load("slides/" + file))
	except:
		pass

objects = {}
images = {}

objects["atlas"] = {}

images["atlas"] = {}

objects["slide"] = 0
objects["slideshow_visible"] = True

log = []
playback = False
recording = False


while True:
	clock.tick(30)

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
				objects[current_char]["mood"] = moods[event.key]

			if event.key in mouth:
				objects[current_char]["mouth"] = mouth[event.key]

			#zoom states, z = tiny, x = indicating, c = lecture, v = emphasis, b = pleading
			if event.key in sizes:
				objects[current_char]["size"] = sizes[event.key]

			#position states, asdfgh each yeild 1/7 position each
			if event.key in char_pos:
				objects[current_char]["pos"] = char_pos[event.key]

			if event.key in angles:
				objects[current_char]["angle"] = angles[event.key]


			#misc instructions, left bracket flips the current character, -= shrink and grow character
			if event.key == pygame.K_LEFTBRACKET:
				objects[current_char]["flip"] = not objects[current_char]["flip"]

			if event.key == pygame.K_EQUALS:
				objects[current_char]["size"] += 0.1
			if event.key == pygame.K_MINUS:
				objects[current_char]["size"] -= 0.1

			#switches active character as desired, 1 is atlas, 2 is queen bee
			if event.key == pygame.K_1:
				current_char = 0
			if event.key == pygame.K_2:
				current_char = 1

	main_surface.fill((255,255,255))
	screen.fill((200,200,200))

	if recording:
		log.append(copy.deepcopy(objects))
	if playback:
		if frame>=len(log):
			playback = False
		else:
			objects = copy.deepcopy(log[frame])

	if objects["slideshow_visible"]:
		main_surface.blit(slideshow[objects["slide"]], pygame.rect.Rect(50,50,400,400))#(620,100, 0,0))

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

	stage_surface = pygame.transform.smoothscale(main_surface, (scrw_chunk*6,scrh_chunk*6))
	screen.blit(stage_surface,(scrw_chunk,scrh_chunk))
	screen.blit(font.render("FPS:" + str(int(clock.get_fps())), True, black),(0,0))
	screen.blit(font.render("Recording: " + str(recording), True, black), (0,20))
	screen.blit(font.render("Playback: " + str(playback), True, black), (0,40))
	pygame.display.flip()

	frame += 1

