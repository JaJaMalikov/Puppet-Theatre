import copy

class key_listener:
	def __init__(self):
		self.keymap = [False]*512
		self.struck = []
	def set_keydown(self, key):
		self.keymap[key] = True
	def set_keyup(self, key):
		self.keymap[key] = False
	def get_key(self, key):
		return self.keymap[key]
	def get_state(self):
		return copy.deepcopy(self.keymap)

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

class recorder:
	def __init__(self):
		self.record = []
		self.frame = 0
		self.is_recording = False
		self.is_playback = False

	def reset_playback(self):
		self.frame = 0

	def record(self):
		self.is_recording = True
		self.record = []
		self.reset_playback()

	def stop_recording(self):
		self.is_recording = False

	def stop_playback(self):
		self.is_playback = False

	def append(self):
		self.recording = True

	def get_recording(self):
		return self.is_recording

	def get_playback(self):
		return self.is_playback

	def update(self):
		if self.is_recording or self.is_playback:
			self.frame += 1

	def save_frame(self, frame):
		self.record.append(frame)

	def get_frame(self):
		return self.record[self.frame]

class compositor(self):
	def __init__(self, obj_file, stage_scale):
		"""
		takes in an object file, reads the data from it
		retrieves files and composites and colors them
		according to the file data
		stores frames, state names, and framerate
		scales it at load time to the required size
		to avoid needless slowdowns later
		"""
		self.scale = stage_scale
		self.filename = obj_file
		self.spritesheet = None
		self.portrait = None

	def load_file(self):
		open_file = open(self.filename)
		file_contents = open_file.read()
		open_file.close()
		self.data = json.loads(file_contents)
		"""
		
		"""
	def composite(self):

		#imports the actual image files and color keys
		#them or not according to the file
		#does so on an ordered loop, so one image
		#can be loaded without issue

	def change_scale(self, new_scale):
		self.scale = new_scale
		self.composite()

	def get_portrait(self):
		#returns the portrait if available and returns
		#the first available image if it is not

	def get_data(self):
		#returns the object data for states and frames

	def get_image(self, input_data):
		#return the currently requested image according
		#to the input data, which is formatted by
		#the parent object according to the requested
		#data from the object file
