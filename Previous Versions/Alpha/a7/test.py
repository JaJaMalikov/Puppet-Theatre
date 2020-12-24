#!/usr/bin/env python2

import pygame
import random
import caption
import listener
import imgset
import pygame.font
from pygame.locals import Color
import visible

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

class Stage(visible.Visible):
	def __init__(self, center, w, h, listener):
		visible.Visible.__init__(center, w, h, listener)

	def build(self):
		self.main_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32).convert_alpha()

class Camera(visible.Visible):
	#needs to be locked to the stage
	#needs to take a clip from images only if they collide with it
	#list objects by distance, check if collides with current camera, blit if true
	#draw stage to camera
	def __init__(self, center, w, h, listener, scale, zoom, cast, props):
		visible.Visible.__init__(self, center, w, h, listener, 1, scale, zoom)
		self.zoom = zoom
		self.cast = cast
		self.props = props
		self.subject = None
		self.cur_sub = 0

	def next_sub(self):
		self.cur_sub = (self.cur_sub + 1) % 10

	def prev_sub(self):
		self.cur_sub = (self.cur_sub - 1) % 10

	def follow_prop(self):
		self.subject = "prop"

	def follow_actor(self):
		self.subject = "actor"

	def follow_none(self):
		self.subject = None

	def build(self):
		focus_width = int(self.width * self.scale * self.data["zoom"])
		focus_height = int(self.height * self.scale * self.data["zoom"])
		self.main_surf = pygame.Surface((focus_width,focus_height), pygame.SRCALPHA, 32).convert_alpha()

	def update(self):
		if self.active:
			if self.subject == "prop":
				self.data["rect"].center = self.props[self.cur_sub].resize_rect().center

			if self.subject == "actor":
				self.data["rect"].center = self.actors[self.cur_sub].resize_rect().center

			if self.listener.get_key(pygame.K_PAGEUP):
				self.zoom_in()
				self.build()
			if self.listener.get_key(pygame.K_PAGEDOWN):
				self.zoom_out()
				self.build()

		self.handle_recording()

	def zoom_in(self):
		self.data["zoom"] += .05

	def zoom_out(self):
		self.data["zoom"] -= .05

	def capture(self, stage):
		#stage.blit(self.main_surf, self.resize_rect())
		self.main_surf.blit(stage, (0,0), self.resize_rect())


class Crew(visible.Visible):
	def __init__(self, center, w, h, listener, scale, zoom, cast, props):
		visible.Visible.__init__(self, center, w, h, listener, 1, scale, zoom)
		self.props = props
		self.cast = cast
		self.cameras = []
		for x in range(10):
			cam = Camera((int(1920/2),int(1080/2)), 1920,1080, listen, scale, 1, self.cast, self.props)
			cam.build()
			self.cameras.append(cam)
		self.data["current_cam"] = 0
		print(self.get_cam())

	def capture(self, stage):
		self.cameras[self.data["current_cam"]].capture(stage)

	def get_cam(self):
		return self.cameras[self.data["current_cam"]].get()

	def set_scale(self, scale):
		for cam in self.cameras:
			cam.set_scale(scale)

	def resize_rect(self):
		return self.cameras[self.data["current_cam"]].resize_rect()

	def update(self):

		#camera controls:
		#0 = 256
		if self.active:
			if not self.cameras[self.data["current_cam"]].active:
				self.cameras[self.data["current_cam"]].set_active()
			for key in range(256, 266):
				if self.listener.get_struck(key):
					print(key-256)
					self.cameras[self.data["current_cam"]].set_active()
					self.data["current_cam"] = key-256
					self.cameras[self.data["current_cam"]].set_active()

		for cam in self.cameras:
			cam.update()
		self.handle_recording()




if __name__ == '__main__':

	countdown = 1
	d_frame = 0
	frame = 0
	rendering = False
	timer = True
	clock = pygame.time.Clock()

	crew = Crew((int(1920/2),int(1080/2)), 1920,1080, listen, scale, 1, [], [])

	while timer:
		clock.tick(24)
		frame += 1
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				timer = False
			if event.type == pygame.KEYDOWN:

				if event.key == pygame.K_EQUALS:
					caps.set_active()
				if event.key == pygame.K_1:
					crew.set_active()
				if event.key == pygame.K_SLASH:
					scale = 1
					caps.set_scale(scale)
					crew.set_scale(scale)
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
					crew.set_scale(scale)

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
		crew.update()

		#for cur_cam in cameras:
		#	cur_cam.update()

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
		pygame.draw.rect(main, (200,0,0), crew.resize_rect(), 5)

		#screen.blit(fire.get(random.randrange(fire.len())), fire.get_pos())

		crew.capture(main)

		#screen.blit(pygame.transform.scale(main, (scr_w,scr_h)), (0,0))
		screen.blit(pygame.transform.scale(crew.get_cam(), (scr_w,scr_h)), (0,0))
		screen.blit(font.render("FPS:" + str(int(clock.get_fps())), True, Color("red")),(0,0))

		#if rendering:
		#	pygame.image.save(main, "G:/frames/{0:05d}".format(frame) + ".png")

		pygame.display.flip()

#name, scale, angle, pivot, offset, skin_color