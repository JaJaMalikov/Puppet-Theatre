#!/usr/bin/env python2

import pygame
import random
import caption
import listener
import imgset
import pygame.font
from pygame.locals import Color

pygame.init()

font = pygame.font.Font('freesansbold.ttf', 12)

scale = .4

a_w = 1920
a_h = 1080

w = int(a_w * scale)
h = int(a_h * scale)

scr_w = int(a_w * .8)
scr_h = int(a_h * .8)

screen = pygame.display.set_mode((scr_w,scr_h))
main = pygame.Surface((w,h), pygame.SRCALPHA, 32).convert_alpha()

script = """
MAXIMUM SPOOK

"""

listen = listener.Key_listener()
caps = caption.Captions(40, script , a_w, int(a_h/13), (int(a_w/2),a_h-int(a_h/26)), "freesansbold", 70, listen, scale)

fires = 1
fire = []
for x in range(fires):
	fire.append(imgset.Imageset("FPT", "fire", scale))
	fire[x].load_images()
	fire[x].set_pos((int((a_w/2)), int(a_h/15 * 10)))

friends = 2
friend = []
for x in range(friends):
	friend.append(imgset.Imageset("FPT", "dance", scale))
	friend[x].load_images()
	friend[x].set_pos((int((a_w/(friends+1)*(x+1))), int(a_h/15 * 6)))



if __name__ == '__main__':

	countdown = 1
	d_frame = 0
	frame = 0
	rendering = False
	timer = True
	clock = pygame.time.Clock()

	while timer:
		clock.tick(24)
		frame += 1
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				timer = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_EQUALS:
					caps.set_active()
				if event.key == pygame.K_SLASH:
					scale = 1
					caps.set_scale(scale)
					for x in range(fires):
						fire[x].set_scale(scale)
						fire[x].load_images()
						fire[x].reset()

					for x in range(friends):
						friend[x].set_scale(scale)
						friend[x].load_images()
						friend[x].reset()
					main = pygame.Surface((int(a_w*scale),int(a_h*scale)), pygame.SRCALPHA, 32).convert_alpha()
					rendering = True
					frame = 0

				if event.key == pygame.K_PERIOD:
					scale = .4
					caps.set_scale(scale)
					for x in range(fires):
						fire[x].set_scale(scale)
						fire[x].load_images()
						fire[x].reset()

					for x in range(friends):
						friend[x].set_scale(scale)
						friend[x].load_images()
						friend[x].reset()
					main = pygame.Surface((int(a_w*scale),int(a_h*scale)), pygame.SRCALPHA, 32).convert_alpha()

				listen.set_keydown(event.key)
			if event.type == pygame.KEYUP:
				listen.set_keyup(event.key)


		screen.fill((1,8,85,255))
		main.fill((1,8,45,255))

		caps.update()

		listen.clear_struck()

		countdown -= 1
		if countdown == 0:
			countdown = 2
			d_frame += 1
			if d_frame > friend[0].max():
				d_frame = 0
		for x in range(friends):
			main.blit(friend[x].get(d_frame), friend[x].get_pos())

		for x in range(fires):
			main.blit(fire[x].get(frame%fire[x].len()), fire[x].get_pos())

		caps.draw(main)
		#screen.blit(fire.get(random.randrange(fire.len())), fire.get_pos())
		screen.blit(pygame.transform.scale(main, (scr_w,scr_h)), (0,0))
		screen.blit(font.render("FPS:" + str(int(clock.get_fps())), True, Color("red")),(0,0))

		#if rendering:
		#	pygame.image.save(main, "G:/frames/{0:05d}".format(frame) + ".png")

		pygame.display.flip()

#name, scale, angle, pivot, offset, skin_color