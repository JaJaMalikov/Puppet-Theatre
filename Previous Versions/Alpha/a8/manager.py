import pygame
from pygame.locals import Color
import listener
from state import State

"""
ensure key commands are proccessed by non-update function
"""


class Main_menu(State):
	def __init__(self, width, height, listener, color):
		State.__init__(self, width, height, listener, color)
		self.Rend_button = Button(450, 100, self.listener, ((self.main_rect.center[0]), 300), (100,0,0), 45, "Renderer")
		self.Char_button = Button(450, 100, self.listener, ((self.main_rect.center[0]), 500), (100,0,0), 45, "Character Creator")

	def update(self):

		if self.listener.get_mouse_button(1):
			if self.Rend_button.clicked():
				return "rend"
			if self.Char_button.clicked():
				return "char"

		self.main_surface.fill(self.color)

		###magic happens here

		self.Rend_button.update()
		self.Char_button.update()

		self.Rend_button.draw(self.main_surface)
		self.Char_button.draw(self.main_surface)

		###magic ends here

		return "menu"

class Renderer(State):
	#state ID = 1
	def __init__(self, width, height, listener, color):
		State.__init__(self, width, height, listener, color)
		self.toolbar = ToolBar(self.width, 30, self.listener, (self.main_rect.center[0],15), (100,100,100), 20)

	def update(self):

		if self.listener.get_key(pygame.K_ESCAPE):
			return "menu"

		#substate updates
		self.toolbar.update()

		self.main_surface.fill(self.color)
		self.toolbar.draw(self.main_surface)
		return "rend"

class Char_creator(State):
	#state ID = 2
	def __init__(self, width, height, listener, color):
		State.__init__(self, width, height, listener, color)

	def update(self):
		if self.listener.get_key(pygame.K_ESCAPE):
			return "menu"

		self.main_surface.fill(self.color)
		return "char"

"""
substate prototypes
"""
class Substate:
	def __init__(self, width, height, listener, pos, color, text_size):
		self.width = width
		self.height = height
		self.listener = listener
		self.text_size = text_size
		self.main_surface = pygame.Surface( (self.width, self.height) , pygame.SRCALPHA, 32).convert_alpha()
		self.font = pygame.font.Font('freesansbold.ttf', self.text_size)
		self.main_rect = self.main_surface.get_rect()
		self.color = color
		self.pos = pos
		self.main_rect.center = self.pos

	def clicked(self):
		return self.collides(self.listener.get_mouse_pos()):

	def update(self):
		pass

	def draw(self, surf):
		surf.blit(self.main_surface, self.main_rect)

	def collides(self, pos):
		return self.main_rect.collidepoint(pos)

class Button(Substate):
	def __init__(self, width, height, listener, pos, color, text_size, name):
		Substate.__init__(self, width, height, listener, pos, color, text_size)
		self.name = name
		print(self.name)
		self.name_img = self.font.render(self.name, True, Color("black"))
		self.name_rect = self.name_img.get_rect()
		self.name_rect.center = (int(self.main_rect.w/2),int(self.main_rect.h/2))

	def update(self):
		self.main_surface.fill(self.color)
		self.main_surface.blit(self.name_img, self.name_rect)

class Menu(substate):
	def __init__(self, width, height, listener, pos, color, text_size):
		Substate.__init__(self, width, height, listener, pos, color, text_size)
		self.exit = Button(100,
					self.height-4, self.listener, 
					(52, int(self.height/2) ), 
					( 200,200,200 ), self.text_size, "exit")			

		def update(self):
			self.main_surface.fill(self.color)
			self.exit.update()
			self.exit.draw(self.main_surface)

class ToolBar(Substate):
	def __init__(self, width, height, listener, pos, color, text_size):
		Substate.__init__(self, width, height, listener, pos, color, text_size)
		self.file = Button(100, 
					self.height-4, self.listener, 
					(52, int(self.height/2) ), 
					( 200,200,200 ), self.text_size, "file")

	def update(self):
		self.main_surface.fill(self.color)

		self.file.update()
		if self.file.clicked():
			

		self.file.draw(self.main_surface)

class ScreenBar(Substate):
	def __init__(self, width, height, listener, text_size):
		Substate.__init__(self, width, height, listener, text_size)

class StatusBar(Substate):
	def __init__(self, width, height, listener, text_size):
		Substate.__init__(self, width, height, listener, text_size)

class CaptionBar(Substate):
	def __init__(self, width, height, listener, text_size):
		Substate.__init__(self, width, height, listener, text_size)

class ObjBar(Substate):
	def __init__(self, width, height, listener, text_size):
		Substate.__init__(self, width, height, listener, text_size)

class VaribleBar(Substate):
	def __init__(self, width, height, listener, text_size):
		Substate.__init__(self, width, height, listener, text_size)



class Manager:
	def __init__(self, width, height, framerate, listener):
		"""
		state manager
		get window size at all times
		return changes in window size to all states to reformat the sub states
		"""
		self.width = width
		self.height = height
		self.clock = pygame.time.Clock()
		self.font = pygame.font.Font('freesansbold.ttf', 20)
		self.running = True
		self.listener = listener
		self.framerate = framerate
		self.HUD = pygame.Surface((self.width, self.height), pygame.SRCALPHA,32).convert_alpha()
		self.hud_visible = False
		self.states = {}

		self.states["menu"] = Main_menu(self.width, self.height, self.listener, (150,150,150))
		self.states["rend"] = Renderer(self.width, self.height, self.listener, (150,150,150))
		self.states["char"] = Char_creator(self.width, self.height, self.listener, (150,10,10))
		self.state = "menu"

	def update(self):
		#clears out the HUD
		self.HUD.fill((0,0,0,0))

		################begin working code

		self.state = self.states[self.state].update()
		self.states[self.state].draw(self.HUD)

		################End working code

		#sets the HUD to visible or invisible, a toggle
		if self.listener.get_struck(pygame.K_F11):
			self.hud_visible = not (self.hud_visible)


		#draws HUD IF visible
		if self.hud_visible:
			frames = "FPS:" + str(int(self.clock.get_fps()))
			fps_render = self.font.render(frames, True, Color("red"))
			self.HUD.blit(fps_render,(0,0))

			mouse = "M pos:" + str(self.listener.get_mouse_pos())
			mouse_render = self.font.render(mouse, True, Color("red"))
			self.HUD.blit(mouse_render,(0,20))


		#maintains framerate
		self.clock.tick(self.framerate)

	def draw(self, surface):
		#draws the HUD to the surface
		surface.blit(self.HUD, (0,0))

	def get_run(self):
		#checks if program is running
		return self.running

	def kill(self):
		#kills the program, to be updates with calls to states for file saving
		self.running = False

