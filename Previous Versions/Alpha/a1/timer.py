class Timer:
	#acts as a base for timed events such as bouncing and rotation
	def __init__(self, Max, Step):
		self.max = Max
		self.step = Step
		self.sign = 1
		self.counter = 0
		self.counting = False

	def start(self):
		self.counting = True

	def update(self):
		if self.counting:
			self.counter += self.step * self.sign
			if self.counter >= self.max:
				self.sign = -1
			elif self.counter <= 0:
				self.sign = 1
				self.counting = False
				self.counter = 0
			else:
				pass

class Bounce(Timer):
	#uses the timer parent to shrink the actor/object for the assigned duration
	def __init__(self, Max, Step)
		Timer.__init__(self, Max, Step)

	def get_scale(self):
		return (1.0 - (self.counter/100))

	def is_bouncing(self):
		return self.counting

class Rotate(Timer): #planned
	#uses the timer parent to rotate a character for the assigned duration/angle
	pass