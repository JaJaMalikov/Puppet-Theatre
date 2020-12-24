import copy

class Key_listener:
	#holds current key states
	def __init__(self):
		self.keymap = [False]*512
		self.struck = [False]*512

	def set_keydown(self, key):
		self.struck[key] = True
		self.keymap[key] = True

	def set_keyup(self, key):
		self.struck[key] = False
		self.keymap[key] = False

	def get_key(self, key):
		return self.keymap[key]

	def get_state(self):
		return copy.deepcopy(self.keymap)

	def get_struck(self, key):
		return self.struck[key]

	def clear_struck(self):
		self.struck = [False]*512