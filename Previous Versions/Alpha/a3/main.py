#!/usr/bin/env python2

import pygame
import os
import random
import caption
import listener
import imgset
import visible
import pygame.font
from pygame.locals import Color

pygame.init()

font = pygame.font.Font('freesansbold.ttf', 12)

sm_scale = .65
scale = sm_scale * 1.0

a_w = 1920
a_h = 1080

w = int(a_w * scale)
h = int(a_h * scale)

scr_w = int(a_w * .8)
scr_h = int(a_h * .8)

screen = pygame.display.set_mode((scr_w,scr_h))
main = pygame.Surface((w,h), pygame.SRCALPHA, 32).convert_alpha()

script_file = open("./script", "r")
script = script_file.read()
script_file.close()

class slideshow(visible.Visible):
	def __init__(self, base, name, center, w, h, listener, scale):
		visible.Visible.__init__(self, center, w, h, listener, 1, scale)
		self.base_name = base
		self.name = name
		self.base = None
		self.imgset = None
		self.data["cur_slide"] = 0

	def update(self):
		if self.active:
			if self.listener.get_struck(pygame.K_LEFT):
				self.prev()
			if self.listener.get_struck(pygame.K_RIGHT):
				self.next()
		self.handle_recording()
		self.main_surf.blit(self.base, (0,0))
		self.main_surf.blit(self.imgset.get_index(self.data["cur_slide"]), (0,0))

	def next(self):
		self.data["cur_slide"] = (self.data["cur_slide"] + 1) % self.imgset.len()

	def prev(self):
		self.data["cur_slide"] = (self.data["cur_slide"] - 1) % self.imgset.len()

	def build(self):
		c_temp = pygame.image.load("res/" + self.base_name + ".png").convert_alpha()
		self.base = pygame.transform.smoothscale(c_temp, (int(c_temp.get_rect().w*scale),int(c_temp.get_rect().h*scale)))
		self.imgset = imgset.Imageset("res", self.name, self.scale)
		self.imgset.load_images()
		self.main_surf = self.imgset.get_index(0)

class speaker(visible.Visible):
	def __init__(self, name, center, w, h, listener, scale):
		visible.Visible.__init__(self, center, w, h , listener, 1, scale)
		self.name = name
		self.img_sets = {}
		self.build()
		self.data["pos"] = "left"
		self.data["emotion"] = "mild"
		self.data["mouth"] = "smile"

	def update(self):
		if self.active:
			#personalized keys
			if self.listener.get_struck(pygame.K_LEFT):
				self.data["pos"] = "right"
			if self.listener.get_struck(pygame.K_RIGHT):
				self.data["pos"] = "left"
			if self.listener.get_struck(pygame.K_q):
				self.data["mouth"] = "ah"
			if self.listener.get_struck(pygame.K_w):
				self.data["mouth"] = "ooh"
			if self.listener.get_struck(pygame.K_e):
				self.data["mouth"] = "sss"
			if self.listener.get_struck(pygame.K_r):
				self.data["mouth"] = "smile"
			if self.listener.get_struck(pygame.K_t):
				self.data["mouth"] = "frown"
			if self.listener.get_struck(pygame.K_y):
				self.data["mouth"] = "mhmm"
			if self.listener.get_struck(pygame.K_a):
				self.data["emotion"] = "furrow"
			if self.listener.get_struck(pygame.K_s):
				self.data["emotion"] = "mild"
			if self.listener.get_struck(pygame.K_d):
				self.data["emotion"] = "surprise"
			if self.listener.get_struck(pygame.K_f):
				self.data["emotion"] = "pixar"
			if self.listener.get_struck(pygame.K_g):
				self.data["emotion"] = "worried"

		self.handle_recording()
		#self.main_surf = self.imgset.get_index(self.data["cur_line"])
		self.main_surf = self.img_sets[self.data["pos"]][self.data["emotion"]].get_key(self.data["mouth"])

	def build(self):
		top_path = os.path.join("res", self.name)
		folders = os.listdir(top_path)
		torem = []
		for folder in folders:
			if not os.path.isdir(os.path.join(top_path, folder)):
				torem.append(folder)
		for folder in torem:
			folders.remove(folder)
		for path in folders:
			sub_path = os.path.join(top_path,path)
			self.img_sets[path] = {}
			subpaths = os.listdir(sub_path)
			torem = []
			for topath in subpaths:
				herp = os.path.join(sub_path, topath)
				if not os.path.isdir(herp):
					torem.append(topath)
			for topath in torem:
				subpaths.remove(topath)
			for emotion in subpaths:
				fin_path_set = os.path.join(sub_path, emotion)
				self.img_sets[path][emotion] = imgset.Imageset(sub_path, emotion, self.scale)
				self.img_sets[path][emotion].load_images()
				#for mouth in os.listdir(fin_path_set):
				#	img_name = os.path.join(fin_path_set, mouth)
				#	temp_img = pygame.image.load(img_name).convert_alpha()
				#	self.img_sets[path][emotion][mouth[:-4]] = temp_img
		#print(self.img_sets)

listen = listener.Key_listener()

vampire = speaker("sit", (1515,580), 807,1130, listen, scale) #needs to be centered at (1515,580)

caps = caption.Captions(40, script , a_w, int(a_h/13), (int(a_w/2),a_h-int(a_h/26)), "freesansbold", 70, listen, scale)

wall = pygame.transform.smoothscale(pygame.image.load("res/bg/0.png").convert_alpha(), (w,h))
fireplace = pygame.transform.smoothscale(pygame.image.load("res/bg/1.png").convert_alpha(), (w,h))
arm = pygame.transform.smoothscale(pygame.image.load("res/bg/2.png").convert_alpha(), (w,h))



slide = slideshow("board", "slides", (850/2+50,550/2+50) ,850, 550, listen, scale)
slide.build()

#dude = pygame.transform.smoothscale(pygame.image.load("temp.png").convert_alpha(), (int(800*scale),int(600*scale)) )
#dude = imgset.Imageset("res", "temp", scale)
#dude.load_images()
#dude.set_pos((1515,580))

#fireplace = pygame.image.load("res/bg/1.png").convert_alpha()
#arm = pygame.image.load("res/bg/2.png").convert_alpha()
fires = 1
fire = []
for x in range(fires):
	fire.append(imgset.Imageset("res", "fire", scale))
	fire[x].load_images()
	fire[x].set_pos((int((a_w/2)+270), int(a_h/15 * 10)-200))


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
				print(event.key)
				if event.key == pygame.K_1:
					caps.set_active()
				if event.key == pygame.K_2:
					vampire.set_active()
				if event.key == pygame.K_3:
					slide.set_active()
				if event.key == pygame.K_SLASH:
					scale = 1
					caps.set_scale(scale)
					vampire.set_scale(scale)
					slide.set_scale(scale)
					for x in range(fires):
						fire[x].set_scale(scale)
						fire[x].load_images()
						fire[x].reset()
					wall = pygame.transform.smoothscale(pygame.image.load("res/bg/0.png").convert_alpha(), (int(a_w*scale),int(a_h*scale)))
					fireplace = pygame.transform.smoothscale(pygame.image.load("res/bg/1.png").convert_alpha(), (int(a_w*scale),int(a_h*scale)))
					arm = pygame.transform.smoothscale(pygame.image.load("res/bg/2.png").convert_alpha(),(int(a_w*scale),int(a_h*scale)))

					main = pygame.Surface((int(a_w*scale),int(a_h*scale)), pygame.SRCALPHA, 32).convert_alpha()
					rendering = True
					frame = 0

				if event.key == pygame.K_PERIOD:
					scale = sm_scale * 1.0
					caps.set_scale(scale)
					vampire.set_scale(scale)
					slide.set_scale(scale)
					for x in range(fires):
						fire[x].set_scale(scale)
						fire[x].load_images()
						fire[x].reset()
					wall = pygame.transform.smoothscale(pygame.image.load("res/bg/0.png").convert_alpha(), (int(a_w*scale),int(a_h*scale)))
					fireplace = pygame.transform.smoothscale(pygame.image.load("res/bg/1.png").convert_alpha(), (int(a_w*scale),int(a_h*scale)))
					arm = pygame.transform.smoothscale(pygame.image.load("res/bg/2.png").convert_alpha(),(int(a_w*scale),int(a_h*scale)))

					main = pygame.Surface((int(a_w*scale),int(a_h*scale)), pygame.SRCALPHA, 32).convert_alpha()

				listen.set_keydown(event.key)
			if event.type == pygame.KEYUP:
				listen.set_keyup(event.key)


		screen.fill((1,8,85,255))
		main.fill((1,8,45,255))

		caps.update()
		vampire.update()
		slide.update()

		listen.clear_struck()

		"""countdown -= 1
		if countdown == 0:
			countdown = 2
			d_frame += 1
			if d_frame > friend[0].max():
				d_frame = 0
		for x in range(friends):
			main.blit(friend[x].get(d_frame), friend[x].get_pos())"""

		main.blit(wall,(0,0))
		for x in range(fires):
			main.blit(fire[x].get_index(frame%fire[x].len()), fire[x].get_pos())
		main.blit(fireplace, (0,0))
		slide.draw(main)
		vampire.draw(main)
		#main.blit(arm, (0,0))
		#main.blit(pygame.transform.rotozoom(dude.get_index(0), (frame%360), 1), dude.get_pos())
		#main.blit(dude, (1100*scale,350*scale))

		caps.draw(main)
		#screen.blit(fire.get(random.randrange(fire.len())), fire.get_pos())
		screen.blit(pygame.transform.scale(main, (scr_w,scr_h)), (0,0))
		screen.blit(font.render("FPS:" + str(int(clock.get_fps())), True, Color("red")),(0,0))

		if rendering:
			pygame.image.save(main, "G:/frames/{0:05d}".format(frame) + ".png")

		pygame.display.flip()

#name, scale, angle, pivot, offset, skin_color