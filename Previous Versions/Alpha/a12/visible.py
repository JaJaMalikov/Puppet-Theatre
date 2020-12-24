from itertools import chain

class Visible:
	def __init__(self, *groups):
		self.sprites = list(chain(*groups))

	def get(self):
		return self.sprites