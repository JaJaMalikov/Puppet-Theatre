#!/usr/bin/env python2

import pygame
import utils
import random
from pygame.locals import Color
import copy
import json
import os
from limb import *

pygame.init()

w = 750
h = 850
scr_w = w * 2
scr_h = h
size = 8

screen = pygame.display.set_mode((scr_w,h))
inter = pygame.Surface([1800,1800], pygame.SRCALPHA, 32).convert_alpha()

#char = "skelly"
pose = "fore"

selection = ["torso", "head", "eyes", "right_bicep", "right_forearm", "left_bicep", "left_forearm", "right_thigh", "right_calf", "left_thigh", "left_calf"]

fial = open("rigs/default.json", "r")
mounts = json.loads(fial.read())
fial.close()

poses = {"fore":[["f","head","eyes"],
["f","right_bicep","right_forearm"],
["f","left_bicep", "left_forearm"],
["f","right_thigh", "right_calf"],
["f","left_thigh", "left_calf"],
["f","torso", "head"],
["r","torso", "left_thigh"],
["r","torso", "right_thigh"],
["r","torso", "right_bicep"],
["f","torso", "left_bicep"]
],

"rear":[["f","right_bicep","right_forearm"],
["f","left_bicep", "left_forearm"],
["f","right_thigh", "right_calf"],
["f","left_thigh", "left_calf"],
["r","torso", "head"],
["f","torso", "right_thigh"],
["f","torso", "left_thigh"],
["f","torso", "right_bicep"],
["f","torso", "left_bicep"]]}




if __name__ == '__main__':
	#skin_color = (96,59,22) # black
	#skin_color = (100,71,49)
	#skin_color = (100,80,70)
	selected = 0

	current_frame = 0
	step_size = 0

	timer = 0
	angle = 0
	angle_timer = 0

	angle_default = open("angles/default.json", "r")
	angles = json.loads(angle_default.read())

	set_name = ""
	layers = "necromancer"

	editname = False
	edit_body = False

	#angle = random.randrange(360)

	#add ability to load/save to file by typing it in the program itself
	#add ability to choose character assets by comma seperated values, list order determines draw order
	#add saving feature
	#add loader
		
	body = make_body(layers.split(","), pose, mounts)
	font = pygame.font.Font('freesansbold.ttf', 20)

	clock = pygame.time.Clock()

	running = True
	while running:# < len(angles):
		clock.tick(30)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				if editname:
					if event.key == pygame.K_RETURN:
						editname = False
					elif event.key == pygame.K_BACKSPACE:
						set_name = set_name[:-1]
					else:
						set_name += str(chr(event.key))
				elif edit_body:
					if event.key == pygame.K_UP:
						body[selection[selected]].move_y(-step_size)
					if event.key == pygame.K_DOWN:
						body[selection[selected]].move_y(step_size)
					if event.key == pygame.K_LEFT:
						body[selection[selected]].move_x(-step_size)
					if event.key == pygame.K_RIGHT:
						body[selection[selected]].move_x(step_size)
					if event.key == pygame.K_RETURN:
						edit_body = False

				else:
					if event.key == pygame.K_INSERT:
						body[selection[selected]].next_layer()
					if event.key == pygame.K_DELETE:
						body[selection[selected]].prev_layer()
					if event.key == pygame.K_p:
						body[selection[selected]].flip()
					if event.key == pygame.K_b:
						edit_body = True
					if event.key == pygame.K_v:
						body[selection[selected]].set_visible( not (body[selection[selected]].get_visible()))
					if event.key == pygame.K_o:
						angle = open("angles/" + set_name + ".json", "r")
						angles = json.loads(angle.read())
						angle.close()
					if event.key == pygame.K_s:
						angle = open("angles/" + set_name + ".json", "w+")
						angle.write(json.dumps(angles))
						angle.close()
					if event.key == pygame.K_r:
						if not os.path.isdir(set_name):
							os.mkdir(set_name)
						save_png(set_name + "/" + str(current_frame), inter)
					if event.key == pygame.K_n:
						editname = True
					if event.key == pygame.K_PAGEUP:
						selected += 1
						if selected >= len(selection):
							selected = 0
					if event.key == pygame.K_PAGEDOWN:
						selected -= 1
						if selected < 0:
							selected = len(selection)-1
					if event.key == pygame.K_HOME:
						current_frame += 1
						if current_frame >= len(angles):
							angles.append(copy.deepcopy(angles[current_frame-1]))
					if event.key == pygame.K_END:
						current_frame -= 1
						if current_frame <0:
							current_frame = len(angles)-1
					if event.key == pygame.K_RIGHT:
						angles[current_frame][selection[selected]] += step_size
					if event.key == pygame.K_LEFT:
						angles[current_frame][selection[selected]] -= step_size
					if event.key == pygame.K_UP:
						step_size += 1
					if event.key == pygame.K_DOWN:
						step_size -= 1

		screen.fill((255,255,255, 255))
		inter.fill((0,0,0,0))


		if body != None:
			for key in body.keys():
				body[key].render()

			for key in body.keys():
				body[key].set_angle(angles[current_frame][key])

			for pair in poses[pose]:
				if pair[0] == "f":
					if body[pair[2]].get_visible():
						body[pair[1]].blit_fore(body[pair[2]].rotate())
				elif pair[0] == "r":
					if body[pair[2]].get_visible():
						body[pair[1]].blit_rear(body[pair[2]].rotate())

			#body.set_angle(angle)
			img, rect = body["torso"].rotate()

			#rect.center = inter.get_rect().center			

			inter.blit(img, rect)

			img = pygame.transform.smoothscale(inter, (w,h))
			t_rect = img.get_rect()
			t_rect.center = screen.get_rect().center

			screen.blit(img, t_rect)
			pygame.draw.rect(screen, (200,0,0), t_rect, 5)

		screen.blit(font.render("selected body part: " + selection[selected], True, Color("red")),(0,0))
		screen.blit(font.render("current frame: " + str(current_frame), True, Color("red")),(0,20))
		screen.blit(font.render("step size: " + str(step_size), True, Color("red")),(0,40))
		screen.blit(font.render("set name: " + set_name, True, Color("red")),(0,60))
		screen.blit(font.render("FPS:" + str(int(clock.get_fps())), True, Color("red")),(0,80))


		#ss.blit(img, (w*(timer%8),h*int(timer/8)))
		pygame.display.flip()



		#save_png("../FPT/dance/" + str(running), img)
		#running += 1


#name, scale, angle, pivot, offset, skin_color