import pygame
import time
import os
import random
from collections import OrderedDict
from collections import deque
import json
import copy

###########################################################Object classes ##########################################

class game:
	"""
	
	load a script from JSON file,
	game.json -> name of game, icon location, size of screen, dir of resources, dir of gamesaves
	contains main menu object, scene object, game menu object
	game menu pauses scene object, displays current image as it runs from the scene call

	game menu.call(scene.run(gamesettings_array)) <- return save|dont save : cur state
	scene.call(game_menu(scene.settings)) <- return update : cur settings
	scene pauses main menu object, does not display main menu as it runs from the main menu call
	exiting game menu causes game menu call to return success (or failure if error happens) and changed settings


	"""

	def __init__(self, scriptname):


		#save script name for later use
		self.scriptname = scriptname
		#loads main script for setup, used to allow games to have multiple possible configurations
		self.script = json.loads(open(self.scriptname,"r").read())

		##############################################main window settings##################################
		#name of the window
		self.gamename = self.script["name"]
		#window icon, displayed in corner and on taskbar
		self.icon = pygame.image.load(self.script["icon"])
		#directory of resources such as scripts, maps, and images, icon also goes here
		self.resource_dir = self.script["res"]
		#exact directory of saves, can be set so that gamesaves are in user space
		self.saves_dir = self.script["saves"]
		#width and height of the window, NOT the play area or maps
		self.game_Width = self.script["width"]
		self.game_Height = self.script["height"]
		#framerate of game as a whole, NOTE: this is the max number of times PER SECOND that the game will actually update
		self.framerate = self.script["framerate"]

		#color that appears behind everything, can be used to set mood so it's scriptable
		self.background_colour = self.script["bg_color"]
		#primary display screen
		self.screen = pygame.display.set_mode((self.game_Width, self.game_Height))

		#settings up screen for first use
		pygame.display.set_caption(self.gamename)
		self.running = True

		##########################################add menu and scene objects################################
		self.scene = scene()
		##########################################end meny and scene objects############################

		#############################################tool objects#######################
		self.listener = key_listener()
		self.clock = pygame.time.Clock()


	def Run(self):
		while running:
			self.clock.tick(self.framerate)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
				if event.type == pygame.KEYDOWN:
					listener.set_keydown(event.key)
				if event.type == pygame.KEYUP:
					listener.set_keyup(event.key)

			self.screen.fill(self.background_colour)

			self.screen.blit(self.scene.get_surface(), self.scene.get_rect())

			pygame.display.flip()


class scene:
	def __init__(self, script):

		self.script = script

		self.feild_images = OrderedDict()
		self.feild_images["ground1"] = [] #array of pygame surfaces of len 6*n for first ground layer, non-solid
		self.feild_images["ground2"] = [] #array of pygame surfaces of len 6*n for second ground layer, non-solid, enhance ground1
		self.feild_images["solid"] = [] #array of pygame surfaces of len 6*n for colidable objects, image NOT sprite
		self.feild_images["roof1"] = [] #array of pygame surfaces of len 6*n for non-solid objects above mobs
		self.feild_images["roof2"] = [] #array of pygame surfaces of len 6*n for non-solid objects above mobs, enhance roof1

		self.ground1_sprites = pygame.sprite.Group()
		self.ground2_sprites = pygame.sprite.Group()
		self.solid_sprites = pygame.sprite.Group()
		self.roof1_sprites = pygame.sprite.Group()
		self.roof2_sprites = pygame.sprite.Group()

		self.feild_width = self.script["feild_width"]
		self.feild_height = self.script["feild_height"]
		self.tile_size = self.script["tile_size"]



		"""

		scene rect should center itself on player
		self.rect.set_center(self.player.get_center()) <<< probably easiest way

		needs sprite ID array
		needs solid sprite array
		needs composite of props as animated bg, faster than updating and blitting each sprite individually
		needs to contain all npcs in sprite group
		needs to contain all props in sprite group
		needs to contain event group
		needs to contain player

		should have script engine for dialog, either for NPCs or for props with events loaded

		needs mob group for moving objects
		should contain scripted events and detect when player activates events
		should also set the player position at runtime
		keylistener should be passed into scene for controlling player and dialog


		"""

	def update(self):
		self.rect.center = self.player.get_center()

class Entity(pygame.sprite.Sprite):
	def __init__(self, name, char_imgs, layer_colors, layers, width, height, x_pos, y_pos, frames, framerate, scale, angle):
		pygame.sprite.Sprite.__init__(self)
		self.data = OrderedDict()
		self.data["scale"] = scale
		self.data["angle"] = angle
		self.data["layer_colors"] = layer_colors
		self.data["char_imgs"] = char_imgs
		self.data["layers"] = layers
		self.data["rect"] = pygame.Rect(x_pos, y_pos, width, height)
		self.data["dir"] = 0
		self.data["frame"] = 0
		self.data["counter"] = 0
		self.data["cur_bounce"] = 1
		self.data["cur_frame"] = 0
		self.data["inventory"] = OrderedDict()

		"""
		where should potential inventory be stored? :/
		the self.data container means you can save to a JSON file simply by including a loader in the game class
		loader loades all details about all visited levels
		level list will be loaded from script, first it will check visited levels from loaded save
		then it will check anything not visited from game save
		current pos of player will be loaded from main save if svaed
		new game will load post and scene from main script file

		this is fun :3

		inventory
		"""

		self.bounce = bounce()
		self.name = name
		self.width = width
		self.height = height
		#self.ss = pygame.image.load("./" + name + ".png")
		self.frames = frames
		self.framerate = framerate
		self.ss = None
		self.composite()
		"""

		should contain event script, with instructions
		0 - default for start script, returns script lines/dialog/items/quests
		single script number -> no option list
		multiple script numbers -> option list

		"""

	def composite(self):
		self.ss = pygame.Surface([self.frames*self.width, self.height*4], pygame.SRCALPHA, 32).convert_alpha()
		color_sheet = pygame.Surface([self.frames*self.width, self.height*4], 32)
		color_sheet.set_colorkey((255,255,255)) #might not work without alpha channel? 
		layers = self.data["layers"]
		for layer in range(len(layers)):
			color_sheet.fill(self.data["layer_colors"][layer])
			color_sheet.blit(pygame.image.load("res/char_res/" + layers[layer] + "/" + str(self.data["char_imgs"][layer])+ ".png" ), (0,0))
			self.ss.blit(color_sheet, (0,0))


		"""

		open sprite sheets as layers, each with transparent body parts/clothing
		create surface with color according to provided key
		merge all colored layers onto main surface using key to make background transparent

		"""

	def get_rect(self):
		return self.data["rect"]

	def set_pos(self, x_pos, y_pos):
		self.data["rect"] = pygame.Rect(x_pos, y_pos, self.width, self.height)

	def get_image(self):
		return pygame.transform.rotozoom(self.ss.subsurface(pygame.Rect(self.data["frame"] * self.width, self.data["dir"] * self.height, self.width, self.height)), self.data["angle"], self.data["scale"])

	def next_frame(self):
		self.data["frame"] += 1
		if self.data["frame"] == self.frames:
			self.data["frame"] = 0

	def change_dir(self, dir):
		self.data["dir"] = dir

	def render_frame(self):
		self.bounce.update()
		#if self.bounce.is_bouncing():
		self.data["cur_bounce"] = self.bounce.get_scale()

		self.data["counter"] += 1
		if self.data["counter"] == self.framerate:
			self.data["counter"] = 0
			self.next_frame()

	def get_center(self):
		return self.rect.center

class prop(Entity):
	def __init__(self, name, char_imgs, layer_colors, layers, width, height, x_pos, y_pos, frames, framerate, solid, scale, angle):
		Entity.__init__(self, name, char_imgs, layer_colors, layers, width, height, x_pos, y_pos, frames, framerate, scale, angle)
		self.solid = solid


class Mob(Entity):
	def __init__(self, name, char_imgs, layer_colors, layers, width, height, x_pos, y_pos, frames, framerate, speed, scale, angle):
		Entity.__init__(self, name, char_imgs, layer_colors, layers, width, height, x_pos, y_pos, frames, framerate, scale, angle)
		self.speed = speed
	def move_up(self):
		self.data["dir"] = 2
		self.data["scale"] *= .95
		#self.data["rect"] = self.data["rect"].move(0,-self.speed)
		self.render_frame()
	def move_left(self):
		self.data["dir"] = 1
		self.data["rect"] = self.data["rect"].move(-self.speed,0)
		self.render_frame()
	def move_down(self):
		self.data["dir"] = 0
		self.data["scale"] *= 1.05
		#self.data["rect"] = self.data["rect"].move(0,self.speed)
		self.render_frame()
	def move_right(self):
		self.data["dir"] = 3
		self.data["rect"] = self.data["rect"].move(self.speed,0)
		self.render_frame()
	def be_still(self):
		self.data["frame"] = 0


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
class Player(Mob):
	def __init__(self, x_pos, y_pos, char_imgs, layer_colors, scale, angle):
		Mob.__init__(self, "player", char_imgs, layer_colors, ["body","eyes","fhair"],64,64,x_pos, y_pos,4, 2, 4, scale, angle)
	def input(self, listener):
		if listener.get_key(pygame.K_w):
			self.move_up()
		elif listener.get_key(pygame.K_a):
			self.move_left()
		elif listener.get_key(pygame.K_s):
			self.move_down()
		elif listener.get_key(pygame.K_d):
			self.move_right()
		else:
			self.be_still()

class NPC(Mob):
	def __init__(self, x_pos, y_pos, char_imgs, layer_colors, scale, angle):
		Mob.__init__(self, "npc", char_imgs, layer_colors, ["body","eyes","fhair"],64,64,x_pos,y_pos, 4,2,2, scale, angle)
		self.go = 0
	def update(self):
		self.bounce.update()
		#if self.bounce.is_bouncing():
		self.data["cur_bounce"] = self.bounce.get_scale()

		self.data["counter"] += 1
		if self.data["counter"] == self.framerate:
			self.data["counter"] = 0
			self.next_frame()

		if self.go == 0:
			self.move_up()
		elif self.go == 1:
			self.move_down()
		elif self.go == 2:
			self.move_left()
		elif self.go == 3:
			self.move_right()
		else:
			self.be_still()

	def random_walk(self):
		self.go = random.choice([0,1,2,3,4,4,4,4,4,4,4])

###########################################Utility classes #####################################################

class key_listener:
	"""
	retains static data on key states for continuous input
	"""
	def __init__(self):
		self.key_log = deque([])
		self.logging = False
		self.keymap = {}
		self.keymap[pygame.K_w] = False
		self.keymap[pygame.K_a] = False
		self.keymap[pygame.K_s] = False
		self.keymap[pygame.K_d] = False
	def set_keydown(self, key):
		print(key)
		if key == 96:
			self.logging = not self.logging
		self.keymap[key] = True
	def set_keyup(self, key):
		self.keymap[key] = False
	def get_key(self, key):
		return self.keymap[key]
	def get_state(self):
		return copy.deepcopy(self.keymap)
	def update(self):
		if self.logging:
			self.key_log.append(self.get_state())
		if not self.logging and len(self.key_log) > 0:
			self.keymap = self.key_log.popleft()


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
			#print(self.counter)
			#print(self.max)
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
	filelist = os.listdir(name)
	filelist.sort()
	for file in filelist:
		try:
			imageset.append(pygame.image.load(name + "/" + file))
		except:
			pass
	return imageset

#########################################################Main game loop

def rungame():
	background_colour = (255,255,255)
	(width, height) = (600, 600)
	pygame.init()
	screen = pygame.display.set_mode((width, height))
	pygame.display.set_caption('RPG game')
	pygame.display.set_icon(pygame.image.load("icon.png"))
	screen.fill(background_colour)
	pygame.display.flip()
	running = True

	clock = pygame.time.Clock()

	props = OrderedDict()
	#props["fire"] = prop("fire")

	dot = pygame.Surface((5,5))
	dot.fill((255,0,0))
	rotated_image = None
	rect = None
	frame = 0
	size = .8

	listener = key_listener()
	player = Player(200,200, [0,0,0], [(200,100,100),(100,100,200),(100,200,100)], 1,0)
	npc = NPC(300,300, [0,0,0], [(0,120,100),(80,100,255),(100,60,30)], 1,0)

	npc_w_t = 0

	while running:
		clock.tick(30)
		#player.update()
		frame += 1
		cur_time = frame#time.time()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				listener.set_keydown(event.key)
			if event.type == pygame.KEYUP:
				listener.set_keyup(event.key)

		listener.update()

		player.input(listener)

		npc_w_t += 1
		if npc_w_t == 16:
			npc_w_t = 0
			npc.random_walk()
		npc.update()

		screen.fill(background_colour)

		screen.blit(player.get_image(), player.get_rect())
		screen.blit(npc.get_image(), npc.get_rect())

		pygame.display.flip()


if __name__ == "__main__":
	rungame()
	#game = game("game.json")
	#game.run()
