import copy

class Record:
	#records data from parent object for later playback
	def __init__(self):
		self.record = []
		self.recording = False
		self.current_frame = 0
		self.play = False

	def append(self, frame):
		self.record.append(copy.deepcopy(frame))

	def next(self):
		self.current_frame += 1
		if self.current_frame >= len(self.record):
			self.current_frame = 0

	def prev(self):
		self.current_frame -= 1
		if self.current_frame < 0:
			self.current_frame = len(self.record)-1

	def get(self):
		return self.record[self.current_frame]

	def reset(self):
		self.current_frame = 0

	def start(self):
		self.reset()
		self.recording = True

	def pause(self):
		self.recording = False

	def resume(self):
		self.recording = True

	def clear(self):
		self.record = []

	def playback(self):
		self.play = True

	def stop(self):
		self.play = False

	def is_playing(self):
		return self.play

	def is_recording(self):
		return self.recording