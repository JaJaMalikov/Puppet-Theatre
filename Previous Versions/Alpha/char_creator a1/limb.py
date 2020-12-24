#!/usr/bin/env python2

import pygame
import utils
import random
from pygame.locals import Color
import copy
import json
import os


class limb:
	def __init__(self, chars, name, scale, angle, pivot, offset, layer_colors):
		self.color_key = (255,255,255)
		self.angle = angle
		self.pivot = pygame.math.Vector2(pivot)
		self.offset = pygame.math.Vector2(offset)
		self.scale = scale
		self.layer_colors = layer_colors
		self.curr_layer = 0
		self.hor = False

		self.images = []
		#self.line_art = []


		file_list = []
		cur_path = "./res/" + chars[0] + "/" + name + "/"
		files = os.listdir(cur_path)
		for file in files:
			if file.endswith(".png"):
				if "_line" not in file:
					file_list.append(file[:-4])

		for file in file_list:
			paths = []
			for char in chars:
				paths.append("./res/" + char + "/" + name + "/" + file)

			self.images.append(self.composite_layers(paths, layer_colors))
			#self.line_art.append()

		self.rect = self.images[0].get_rect()
		self.fin_image = pygame.Surface([self.rect.w,self.rect.h], pygame.SRCALPHA, 32).convert_alpha()

		self.visible = True

	def composite_layers(self, names, colors):
		layers = []
		for name in range(len(names)):
			layers.append(self.render_layer(names[name],colors[name]))
		temp_rect = layers[0].get_rect()
		fin_image = pygame.Surface([temp_rect.w,temp_rect.h], pygame.SRCALPHA,32).convert_alpha()
		for layer in layers:
			fin_image.blit(layer,(0,0))
		return fin_image

	def render_layer(self, name, color):
		color_image = pygame.image.load(name + ".png").convert_alpha()

		return color_image

	def flip(self):
		self.hor = not self.hor

	def get_visible(self):
		return self.visible

	def set_visible(self, visible):
		self.visible = visible

	def set_angle(self, angle):
		self.angle = angle

	def add_angle(self, angle):
		self.angle += angle

	def next_layer(self):
		self.curr_layer += 1
		self.curr_layer = self.curr_layer % len(self.images)

	def prev_layer(self):
		self.curr_layer -= 1
		self.curr_layer = self.curr_layer % len(self.images)

	def get_rect(self):
		return self.rect

	def move_x(self, x_off):
		self.pivot[0] += x_off

	def move_y(self, y_off):
		self.pivot[1] += y_off

	def rotate(self):
		"""Rotate the surface around the pivot point.

		Args:
			surface (pygame.Surface): The surface that is to be rotated.
			angle (float): Rotate by this angle.
			pivot (tuple, list, pygame.math.Vector2): distance from upper left corner of the destination
			offset (pygame.math.Vector2): distance from center 0,0 being center -1,-1, being just to the upper left.
			scale (float): scale the image being rotated
		"""
		rotated_image = pygame.transform.rotozoom(self.fin_image, -self.angle, self.scale)  # Rotate the image.

		rotated_offset = self.offset.rotate(self.angle)  # Rotate the offset vector.
		# Add the offset vector to the center/pivot point to shift the rect.
		rect = rotated_image.get_rect(center=self.pivot+rotated_offset)
		return rotated_image, rect  # Return the rotated image and shifted rect.

	def blit_fore(self, info):
		self.fin_image.blit(info[0], info[1])

	def blit_rear(self, info):
		cur_image = pygame.Surface([self.rect.w,self.rect.h], pygame.SRCALPHA, 32).convert_alpha()
		cur_image.blit(info[0], info[1])
		cur_image.blit(self.fin_image, (0,0))
		self.fin_image = cur_image

	def render(self):
		self.fin_image.fill((0,0,0,0))# = pygame.Surface([self.rect.w,self.rect.h], pygame.SRCALPHA, 32).convert_alpha()

		#print(len(self.images))
		#print(len(self.layer_colors))
		"""
		for image in range(len(self.images[self.curr_layer])):
			new_image = pygame.Surface([self.rect.w,self.rect.h], 32)
			new_image.fill(self.layer_colors[0])
			new_image.blit(self.images[image][0], self.rect)
			new_image.set_colorkey(self.color_key)

			self.fin_image.blit(new_image, (0,0))
			self.fin_image.blit(self.images[image][1], (0,0))"""

		if self.hor:
			self.fin_image.blit(pygame.transform.flip(self.images[self.curr_layer], True, False),(0,0))
		else:
			self.fin_image.blit(self.images[self.curr_layer],(0,0))

def save_png(name, surface):
	pygame.image.save(surface, name + ".png")

def make_body(char, pos, mounts):
	layer_colors = [(255,207,179),(250,250,250)] # white

	body = {}

	for part in mounts[pos].keys():
		body[part] = limb(char, part, 1, 0.0, mounts[pos][part][0], mounts[pos][part][1], layer_colors)


	return body