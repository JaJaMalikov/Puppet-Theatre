import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from listener import Key_listener

import random
import sys
import os

import pywavefront

print(OpenGL.version.__version__)

#import OpenGL.GL.shaders

"""
stage is a large 3d objects with multiple layers, each drawn over the previous
such that movement of the camera generates paralax movement automatically


"""

vertices = (1,1)

class plane:
	def __init__(self, dirname):
		self.speed = .05
		self.dirname = dirname
		self.texture_list = []
		self.width = 0
		self.height = 0
		self.dist = 0.0
		self.angle = 0
		self.pos = [0,0,0]
		self.verts = [[-1.0,-1.0, 0.0],
						[ 0.0,-1.0, 0.0],
						[ 1.0,-1.0, 0.0],
						[ 1.0, 0.0, 0.0],
						[ 1.0, 1.0, 0.0],
						[ 0.0, 1.0, 0.0],
						[-1.0, 1.0, 0.0],
						[0.0, 0.0, 0.0]]

		self.coords = ((0.0,0.0),
						(0.5,0.0),
						(1.0,0.0),
						(1.0,0.5),
						(1.0,1.0),
						(0.5,1.0),
						(0.0,1.0),
						(0.0,0.5))

		self.load_textures()
		self.frame = 0

	def rotp(self):
		self.angle += self.speed * 100

	def rotn(self):
		self.angle += self.speed * -100

	def move_H(self, delta):
		self.pos[0] += delta * self.speed
		#for x in range(len(self.verts)):
		#	self.verts[x][0] += delta * self.speed
		#print(self.verts)

	def move_V(self, delta):
		self.pos[1] += delta * self.speed
		#for y in range(len(self.verts)):
		#	self.verts[y][1] += delta * self.speed

	def move_D(self, delta):
		self.pos[2] += delta * self.speed
		#self.dist = delta * self.speed
		#for z in range(len(self.verts)):
		#	self.verts[z][2] += self.dist

	def load_textures(self):
		names = os.listdir(self.dirname)
		for name in names:
			self.texture_list.append(self.load_texture(os.path.join(self.dirname,name)))

	def load_texture(self, name):
		textureSurface = pygame.image.load(name).convert_alpha()
		textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
		self.width = textureSurface.get_width()
		self.height = textureSurface.get_height()

		glEnable(GL_TEXTURE_2D)

		texid = glGenTextures(1)

		glBindTexture(GL_TEXTURE_2D, texid)
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height,
					 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		glEnable(GL_BLEND)
		glGenerateMipmap(GL_TEXTURE_2D)
		print(texid)
		return texid


	def draw_surf(self):
		glPushMatrix()

		glTranslatef(self.pos[0], self.pos[1] , self.pos[2])
		glRotatef(self.angle, 0, 0, 1)
		#self.angle = 0
		glBegin(GL_POLYGON)
		for x in range(len(self.verts)):
			glTexCoord2f(*self.coords[x])
			glVertex3f(*self.verts[x])

		glEnd()

		glPopMatrix()

	def draw_entity(self):
		glBindTexture(GL_TEXTURE_2D, self.texture_list[self.frame] )
		self.draw_surf()
		self.frame = (self.frame + 1) % len(self.texture_list)


pygame.init()
display = (800, 600)
screen = pygame.display.set_mode(
	display, pygame.DOUBLEBUF | pygame.OPENGL | pygame.OPENGLBLIT)

def_angle = 4


head = plane("pers")
fire = plane("fire")

entities = [head, fire]
default_order = [0,1]


gluPerspective(45, display[0] / display[1], 0.1, 50.0)
glTranslatef(0.0, 0.0, -10)
glClearColor(1,1,1,1)
#glEnable(GL_DEPTH_TEST)
listen = Key_listener()

clock = pygame.time.Clock()


frame = 0
while True:
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			listen.set_keydown(event.key)
		if event.type == pygame.KEYUP:
			listen.set_keyup(event.key)

	if listen.get_key(pygame.K_UP):
		head.move_V(1)
	if listen.get_key(pygame.K_DOWN):
		head.move_V(-1)
	if listen.get_key(pygame.K_RIGHT):
		head.move_H(1)
	if listen.get_key(pygame.K_LEFT):
		head.move_H(-1)
	if listen.get_key(pygame.K_PAGEUP):
		head.move_D(-1)
	if listen.get_key(pygame.K_PAGEDOWN):
		head.move_D(1)
	if listen.get_key(pygame.K_HOME):
		print("still down", frame)
		head.rotn()
	if listen.get_key(pygame.K_END):
		head.rotp()

	draw_order = [x for _, x in sorted(zip( entities , default_order), key=lambda x: x[0].pos[2] )]
	for x in draw_order:
		entities[x].draw_entity()
	#head.draw_entity()
	#fire.draw_entity()

	pygame.display.flip()
	#pygame.image.save(screen, "G:/frames/{0:05d}".format(frame) + ".png")
	frame += 1