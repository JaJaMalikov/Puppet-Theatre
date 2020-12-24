import pygame
from pygame.locals import Color
import listener
import imgset

class Manager:
	def __init__(self, width, height, framerate, listener):
		self.width = width
		self.height = height
		self.clock = pygame.time.Clock()
		self.font = pygame.font.Font('freesansbold.ttf', 20)
		self.running = True
		self.listener = listener
		self.framerate = framerate
		self.HUD = pygame.Surface((self.width, self.height), pygame.SRCALPHA,32).convert_alpha()
		self.hud_visible = False
		self.images = []
		self.animations = []
		for x in range(10):
			self.animations.append(imgset.Imageset("none", "current", 1))

	def importPNG(self, name):
		#try:
		img = pygame.image.load(name).convert_alpha()
		self.images.append(img)
		#except IOError:
		#	raise

	def importAnimation(self, name):
		#try:
		cur_anim = imgset.Imageset(name, "current", 1)
		cur_anim.load_images()
		self.animations.append(cur_anim)
		#except IOError:
		#	raise 

	def importObject(self, name, ID):
		#try:
		self.animations[ID+31994].change_set(name, "current", 1)
		#except IOError:
		#	raise 		

	def resize(self, size):
		self.width = size[0]
		self.height = size[1]
		self.HUD = pygame.Surface(size, pygame.SRCALPHA,32).convert_alpha()		

	def update(self):
		#clears out the HUD
		self.HUD.fill((0,0,0,0))

		################begin working code

		pos = 0
		for img in self.images:
			self.HUD.blit(img, (pos, 0))
			pos += img.get_width()

		for anim in self.animations:
			if anim.get_loaded():
				self.HUD.blit(anim.get(), (pos, 0))
				pos += anim.get().get_width()
				anim.next()
		#self.state = self.states[self.state].update()
		#self.states[self.state].draw(self.HUD)

		################End working code

		#sets the HUD to visible or invisible, a toggle
		if self.listener.get_struck(pygame.K_F11):
			self.hud_visible = not (self.hud_visible)

		keysdown = self.listener.get_all() 
		if keysdown != []:
			print(keysdown)


		#draws HUD IF visible
		if self.hud_visible:
			try:
				frames = "FPS:" + str(int(self.clock.get_fps()))
				fps_render = self.font.render(frames, True, Color("red"))
				self.HUD.blit(fps_render,(0,0))

				mouse = "M pos:" + str(self.listener.get_mouse_pos())
				mouse_render = self.font.render(mouse, True, Color("red"))
				self.HUD.blit(mouse_render,(0,20))
			except:
				pass

		#maintains framerate
		self.clock.tick(self.framerate)

	def draw(self, surface):
		#draws the HUD to the surface
		surface.blit(self.HUD, (0,0))

